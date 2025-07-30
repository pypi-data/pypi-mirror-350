# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Singleton(type):
    """Class realized pattern singleton
    """
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        """Invoke

        Returns
        -------
        cls
            Class instance
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractHandler(metaclass=ABCMeta):
    """Abstract class for handlers
    """

    EXTENSION: str = ""
    MIME: str = ""

    def __repr__(self):
        """Return handler representation

        Returns
        -------
        str
            Handler's representation
        """
        return f"{self}(EXTENSION='{self.EXTENSION}', MIME='{self.MIME}')"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    @abstractmethod
    async def execute(self, session, url, **params):
        """Make async request

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Requested url

        Raises
        ------
        NotImplementedError
            Must overrided in nested class
        """
        raise NotImplementedError()

    def prepare_url(self, url):
        """Add extension to url

        Parameters
        ----------
        url : str
            Url

        Returns
        -------
        str
            Url with extension
        """
        return f"{url}{self.EXTENSION}"

    def valid_response(self, resp):
        """Check reponse's validity by mime

        Parameters
        ----------
        resp : aiohttp.client_reqrep.ClientResponse
            Response

        Returns
        -------
        bool
            Is valid response
        """
        return True if resp.content_type == self.MIME else False
