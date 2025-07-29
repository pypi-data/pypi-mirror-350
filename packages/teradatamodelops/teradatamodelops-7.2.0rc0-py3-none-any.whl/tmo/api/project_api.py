from __future__ import absolute_import
from typing import Dict, List

from tmo.api.iterator_base_api import IteratorBaseApi


class ProjectApi(IteratorBaseApi):

    path = "/api/projects"
    type = "PROJECT"

    def _get_header_params(self):
        # The header for project id is required for the archive/unarchive method from base_api
        header_vars = [
            "AOA-Project-ID",
            "VMO-Project-ID",
            "Content-Type",
            "Accept",
        ]  # AOA-Project-ID kept for backwards compatibility
        header_vals = [
            self.tmo_client.project_id,
            self.tmo_client.project_id,
            self.json_type,
            self.json_type,
        ]

        return self.generate_params(header_vars, header_vals)

    def find_by_name_like(self, name: str, projection: str = None) -> List:
        """
        returns a list of projects matching the given name

        Parameters:
           name (str): project name to search by
           projection (str): projection type

        Returns:
            (list): list of projects
        """
        query_vars = ["name", "projection"]
        query_vals = [name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByName",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def save(self, project: Dict[str, str]):
        """
        create a project

        Parameters:
           project (dict): project to create

        Returns:
            (dict): project
        """
        header_vars = ["Accept"]
        header_vals = [self.json_type]
        header_params = self.generate_params(header_vars, header_vals)

        return self.tmo_client.post_request(
            path=self.path, header_params=header_params, query_params={}, body=project
        )

    def update(self, project: Dict[str, str]):
        """
        update a project

        Parameters:
           project (dict): project to update

        Returns:
            (dict): project
        """
        header_vars = ["Accept"]
        header_vals = [self.json_type]
        header_params = self.generate_params(header_vars, header_vals)

        return self.tmo_client.put_request(
            path=f"{self.path}/{self.tmo_client.project_id}",
            header_params=header_params,
            query_params={},
            body=project,
        )

    def is_archived(self, project_id: str):
        """
        returns the archived status of a project
        Parameters:
           project_id (str): project id to check archived status
        Returns:
            (bool)
        """
        project = self.find_by_id(project_id)

        return project["archived"]
