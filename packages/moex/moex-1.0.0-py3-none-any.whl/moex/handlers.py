# -*- coding: utf-8 -*-
from moex.data_classes import CSV, HTML, JSON, XML
from moex.exceptions import HandlersSearchError
from moex.meta import AbstractHandler, Singleton
from moex.utils import pack_in_dao, prepare_url


class JSONHandler(AbstractHandler):
    """Handler for JSON format
    """
    DAO = JSON
    EXTENSION = ".json"
    MIME = "application/json"

    @pack_in_dao
    @prepare_url
    async def execute(self, session, url, **params):
        """Make async request

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Requested url

        Returns
        -------
        JSON
            Data object
        """
        async with session.get(url, params=params) as resp:
            if self.valid_response(resp):
                return await resp.json()


class XMLHandler(AbstractHandler):
    """Handler for XML format
    """
    DAO = XML
    EXTENSION = ".xml"
    MIME = "application/xml"

    @pack_in_dao
    @prepare_url
    async def execute(self, session, url, **params):
        """Make async request

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Requested url

        Returns
        -------
        XML
            Data object
        """
        async with session.get(url, params=params) as resp:
            if self.valid_response(resp):
                return (
                    await resp.content.read()
                    ).decode(resp.get_encoding())


class CSVHandler(AbstractHandler):
    """Handler for CSV format
    """
    DAO = CSV
    EXTENSION = ".csv"
    MIME = "text/csv"

    @pack_in_dao
    @prepare_url
    async def execute(self, session, url, **params):
        """Make async request

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Requested url

        Returns
        -------
        CSV
            Data object
        """
        async with session.get(url, params=params) as resp:
            if self.valid_response(resp):
                return (
                    await resp.content.read()
                    ).decode(resp.get_encoding())


class HTMLHandler(AbstractHandler):
    """Handler for HTML format
    """
    DAO = HTML
    EXTENSION = ".html"
    MIME = "text/html"

    @pack_in_dao
    @prepare_url
    async def execute(self, session, url, **params):
        """Make async request

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Requested url

        Returns
        -------
        HTML
            Data object
        """
        async with session.get(url, params=params) as resp:
            if self.valid_response(resp):
                return await resp.text()


AVAILABLE = (JSONHandler, XMLHandler, CSVHandler, HTMLHandler)


class Handlers(metaclass=Singleton):
    """Factory for creating handlers
    """

    def __init__(self):
        """Init data
        """
        self._data = {}

    def __repr__(self):
        """Return handlers representation

        Returns
        -------
        str
            Handlers representation
        """
        return f"{self}(formats={self.formats})"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    def __iter__(self):
        """Yield handlers

        Yields
        ------
        generator
            Tuple of format and class handler
        """
        for fmt, obj in self._data.items():
            yield fmt, obj

    @property
    def formats(self):
        """Return handlers formats

        Returns
        -------
        set
            Acceptable formats
        """
        return {k for k, _ in self}

    def register(self, output_format, handler):
        """Register handler

        Parameters
        ----------
        output_format : str
            Handler's format
        handler : MetaHandler
            Handler's class
        """
        self._data[output_format] = handler

    def create(self, output_format):
        """Create handler instance

        Parameters
        ----------
        output_format : str
            Handler's format

        Returns
        -------
        MetaHandler
            Handler instance

        Raises
        ------
        HandlersSearchError
            Requested format doesn't supported
        """
        try:
            return self._data[output_format]()
        except KeyError as e:
            raise HandlersSearchError(output_format, self.formats) from e
