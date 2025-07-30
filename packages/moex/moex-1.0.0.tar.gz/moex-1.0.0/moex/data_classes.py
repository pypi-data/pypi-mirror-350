# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict, FrozenSet
from xml.etree import ElementTree

from pandas import DataFrame, read_html


@dataclass
class Template:
    """Data class for template
    """
    id: int
    path: str
    path_variables: FrozenSet


@dataclass
class JSON:
    """Data class wrapper for JSONHandler
    """
    raw: Dict

    def to_df(self, filter_key=None):
        """Convert dict to dataframe

        Parameters
        ----------
        filter_key : str, optional
            Key from dict for select, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            Converted dataframe
        """
        if self.raw is None:
            return
        if filter_key is None:
            raw_keys = [*self.raw.keys()]
            if raw_keys:
                filter_key = raw_keys[0]
        if filter_key is None or filter_key not in self.raw:
            return
        raw_filtered = self.raw[filter_key]
        raw_filtered_data = raw_filtered.get("data", None)
        raw_filtered_columns = raw_filtered.get("columns", None)
        if raw_filtered_data is None or raw_filtered_columns is None:
            return
        return DataFrame(raw_filtered_data, columns=raw_filtered_columns)


@dataclass
class XML:
    """Data class wrapper for XMLHandler
    """
    raw: str

    def to_tree(self):
        """Convert html text to xml tree

        Returns
        -------
        xml.etree.ElementTree.Element
            XML Tree
        """
        if self.raw:
            return ElementTree.fromstring(self.raw)


@dataclass
class CSV:
    """Data class wrapper for CSVHandler
    """
    raw: str


@dataclass
class HTML:
    """Data class wrapper for HTMLHandler
    """
    raw: str

    def to_df(self):
        """Convert html text to dataframe

        Returns
        -------
        pandas.core.frame.DataFrame
            Converted dataframe
        """
        if self.raw:
            df, *_ = read_html(self.raw)
            return df
