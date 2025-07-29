from __future__ import absolute_import
from typing import List, Dict
from tmo.api_client import TmoClient

import abc


class BaseApi(object):
    path = ""
    json_type = "application/json"

    def __init__(self, tmo_client: TmoClient):
        self.tmo_client = tmo_client

    @abc.abstractmethod
    def _get_header_params(self):
        pass

    def generate_params(self, params: List[str], values: List[str]):
        """
        returns list of parameters and values as dictionary

        Parameters:
           params (List[str]): list of parameter names
           values (List[str]): list of parameter values

        Returns:
            (dict): generated parameters
        """

        # bools in python start with upper case when converted to strs. APIs expect lowercase
        api_values = [str(v).lower() if type(v) is bool else v for v in values]

        return dict(zip(params, api_values))

    def required_params(self, param_names: List[str], dict_obj: Dict[str, str]):
        """
        checks required parameters, raises exception if the required parameter is missing in the dictionary

        Parameters:
           param_names (List[str]): list of required parameter names
           dict_obj (Dict[str, str]): dictionary to check for required parameters
        """
        for param in param_names:
            if param not in dict_obj:
                raise ValueError("Missing required value " + str(param))

    def find_all(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns all entities

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all entities
        """
        header_params = self._get_header_params()

        query_vars = ["projection", "page", "size", "sort"]
        query_vals = [projection, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(self.path, header_params, query_params)

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns all entities by archived

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order e.g. name?asc / name?desc
           archived (bool): whether to return archived or unarchived entities

        Returns:
            (dict): all entities
        """
        header_params = self._get_header_params()

        query_vars = ["projection", "page", "size", "sort", "archived"]
        query_vals = [projection, page, size, sort, archived]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.path}/search/findByArchived", header_params, query_params
        )

    def find_by_id(self, id: str, projection: str = None):
        """
        returns the entity

        Parameters:
           id (str): entity id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): entity
        """
        header_params = self._get_header_params()

        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.path}/{id}", header_params, query_params
        )

    def archive(self, id: str):
        """
        archives the entity
        Parameters:
           id (str): entity id(uuid) to archive
        Returns:
            (dict): entity
        """
        header_params = self._get_header_params()

        return self.tmo_client.post_request(
            f"/api/archives/{self.type}/{id}", header_params, {}, {}
        )

    def unarchive(self, id: str):
        """
        unarchives the entity
        Parameters:
           id (str): entity id(uuid) to unarchive
        Returns:
            (dict): entity
        """
        header_params = self._get_header_params()

        return self.tmo_client.delete_request(
            f"/api/archives/{self.type}/{id}", header_params, {}, {}
        )
