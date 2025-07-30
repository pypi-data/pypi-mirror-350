# -*- coding: utf-8 -*-
from time import sleep

from aiohttp import ClientSession
from rich.live import Live

from moex.design import CliDesigner
from moex.handlers import AVAILABLE as available_handlers
from moex.handlers import Handlers
from moex.templates import TemplatesRepository

__all__ = ("AsyncMoex", )


class AsyncMoex:
    """API interface for MoscowExchange
    """

    templates = TemplatesRepository()

    handlers = Handlers()
    for handler in available_handlers:
        handlers.register(handler.EXTENSION, handler)

    def __init__(self, output_format: str = ".json", **session_params):
        self._session = None
        self._session_params = session_params
        self.handler = self.handlers.create(output_format=output_format)

    async def __aenter__(self):
        self._session = ClientSession(**self._session_params)
        if len(self.templates) == 0:
            await self.templates.load_data(self._session)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(exc_type, exc_value, traceback)
        await self._session.close()

    def __repr__(self):
        """Return AsyncMoex representation

        Returns
        -------
        str
            AsyncMoex representation
        """
        try:
            return f"{self}(handler={self.handler}, templates={self.templates.ids})"
        except AttributeError:
            return f"{self}()"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    async def execute(self, url, **params):
        """Call requested uri

        Parameters
        ----------
        url : str
            Api url

        Returns
        -------
        Any
            Dataclass instance
        """
        return await self.handler.execute(session=self._session, url=url, **params)

    async def show_template_doc(self, template_id, interval: float = .123):
        """Print docs from official web site

        Parameters
        ----------
        template_id : int
            Template's identifier
        """
        await self.templates.show_template_doc(self._session, template_id, interval)

    def show_templates(self, interval: float = .123):
        """Print table with templates identifiers and addresses
        """
        doc_table = CliDesigner.get_table("ID", "URI TEMPLATE")

        with Live(doc_table, refresh_per_second=6):
            for template_id, template in self.templates:
                doc_table.add_row(
                    f"{CliDesigner.random_color()}{template_id}",
                    f"{CliDesigner.random_color()}{template.path}"
                    )
                sleep(interval)

    def find_template(self, search_pattern):
        """Find templates by pattern

        Parameters
        ----------
        search_pattern : str
            Regex or usual string

        Returns
        -------
        generator
            Templates generator
        """
        return self.templates.find_template_id(search_pattern)

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
        return self.templates.get_template(template_id)

    def render_url(self, template_id, **template_vars):
        """Render url with jinja

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        str
            Rendered url
        """
        return self.templates.render_template(template_id, **template_vars)
