# -*- coding: utf-8 -*-
import re
from itertools import chain
from time import sleep
from types import MappingProxyType

from bs4 import BeautifulSoup
from rich.live import Live

from moex.data_classes import Template
from moex.design import CliDesigner
from moex.exceptions import TemplateRenderError
from moex.meta import Singleton
from moex.utils import raise_search_error

URL = "http://iss.moex.com"
API = "/iss/reference/"


class TemplatesRepository(metaclass=Singleton):
    """Templates Repository
    """
    def __init__(self, url=URL, api=API):
        """Init params

        Parameters
        ----------
        url : str, optional
            MOEX url, by default URL
        api : str, optional
            MOEX api, by default API
        """
        self.url = url
        self.uri = f"{url}{api}"
        self._data = {}

    def __repr__(self):
        """Return templates repository representation

        Returns
        -------
        str
            Templates repository representation
        """
        return f"{self}(ids={self.ids})"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    def __iter__(self):
        """Yield templates

        Yields
        ------
        generator
            Tuple of template id and template dataclass
        """
        for t_id, template in self._data.items():
            yield t_id, template

    def __len__(self):
        """Len method

        Returns
        -------
        int
            Number of templates
        """
        return len(self.ids)

    async def load_data(self, session):
        """Load uri templates from official web site

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        """
        if isinstance(self._data, MappingProxyType):
            return
        expr = re.compile(r"\[([A-Za-z0-9_]+)\]")
        async with session.get(self.uri) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            for block in soup.find_all("a"):
                _id = int(block["href"].split("/")[-1])
                path = f'{self.url}{block.text.replace("[", "{").replace("]", "}")}'
                path_variables = {*expr.findall(block.text)}
                self._data[_id] = Template(
                    id=_id, path=path, path_variables=path_variables
                    )
            self._data = MappingProxyType(self._data)

    @property
    def ids(self):
        """Return set of templates identifieres

        Returns
        -------
        set
            Templates identifieres
        """
        return {i for i, _ in self}

    @raise_search_error
    def get_template(self, template_id):
        """Get template by template identifier

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        Template
            Template dataclass
        """
        return self._data[template_id]

    def render_template(self, template_id, **template_vars):
        """Render template with jinja

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        str
            Rendered template
        """
        template = self.get_template(template_id)
        diff = template.path_variables.difference({*template_vars.keys()})
        if diff:
            raise TemplateRenderError(','.join(diff), template.path)
        return template.path.format(**template_vars)

    async def show_template_doc(self, session, template_id, interval):
        """Print docs from official web site https://iss.moex.com/iss/reference/<template_id>

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        template_id : int
            Template's identifier
        """
        doc_url = f"{self.uri}{template_id}"
        async with session.get(doc_url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            doc_table = CliDesigner.get_table(doc_url, show_lines=False)
            with Live(doc_table, refresh_per_second=4):
                for row in chain(*(
                    filter(
                        lambda txt: txt != "", map(
                            lambda block: block.text.strip(), soup.find_all(tag)
                            )
                        ) for tag in ("h1", "dl")
                    )
                ):
                    doc_table.add_row(f"{CliDesigner.random_color()}{row}")
                    sleep(interval)

    def find_template_id(self, pattern):
        """Find templates by pattern

        Parameters
        ----------
        search_pattern : str
            Regex or usual string

        Yields
        ------
        Template
            Dataclass
        """
        for _, template in self:
            if re.search(pattern, template.path):
                yield template
