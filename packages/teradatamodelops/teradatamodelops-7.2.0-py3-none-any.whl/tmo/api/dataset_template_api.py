from __future__ import absolute_import
from typing import Dict, List

from tmo.api.iterator_base_api import IteratorBaseApi


class DatasetTemplateApi(IteratorBaseApi):
    path = "/api/datasetTemplates"
    type = "DATASET_TEMPLATE"

    def _get_header_params(self):
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
            self.tmo_client.select_header_accept([
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]),
        ]

        return self.generate_params(header_vars, header_vals)

    def find_by_name_like(self, name: str, projection: str = None) -> List:
        """
        returns a list dataset template of a project by name

        Parameters:
           name (str): dataset name(string) to find
           projection (str): projection type

        Returns:
            (list): dataset template
        """
        query_vars = ["name", "projection"]
        query_vals = [name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByName",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def save(self, dataset_template: Dict[str, str]):
        """
        register a dataset template

        Parameters:
           dataset template (dict): dataset template to register

        Returns:
            (dict): dataset template
        """
        return self.tmo_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=dataset_template,
        )

    def render(self, id: str) -> Dict:
        """
        returns a rendered dataset template

        Parameters:
           id (str): dataset_template id

        Returns:
            (dict): rendered dataset template
        """
        return self.tmo_client.get_request(
            path=f"{self.path}/{id}/render",
            header_params=self._get_header_params(),
            query_params={},
        )
