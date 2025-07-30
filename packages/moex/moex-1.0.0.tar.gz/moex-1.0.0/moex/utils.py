# -*- coding: utf-8 -*-
from functools import wraps

from moex.exceptions import TemplateSearchError


def raise_search_error(func):
    """Decorate funcion

    Parameters
    ----------
    func : function
        Wrapped function

    Returns
    -------
    function
        Function wrapper

    Raises
    ------
    TemplateSearchError
        _description_
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Raise error if didn't find template's id in repository

        Returns
        -------
        Anu
            Function result

        Raises
        ------
        TemplateSearchError
            Template's id doesn't exist
        """
        try:
            return func(*args, **kwargs)
        except KeyError as exc:
            raise TemplateSearchError(exc) from exc
    return wrapper


def pack_in_dao(func):
    """Decorate funcion

    Parameters
    ----------
    func : function
        Wrapped function

    Returns
    -------
    function
        Function wrapper
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Pack function result in dataclass

        Returns
        -------
        Any
            Dataclass
        """
        return args[0].DAO(await func(*args, **kwargs))
    return wrapper


def prepare_url(func):
    """Decorate funcion

    Parameters
    ----------
    func : function
        Wrapped function

    Returns
    -------
    function
        Function wrapper
    """
    @wraps(func)
    async def wrapper(self, session, url, **params):
        """Prepare url for handler and call it

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Requested url

        Returns
        -------
        Any
            Dataclass
        """
        url = self.prepare_url(url)
        return await func(self, session, url, **params)
    return wrapper
