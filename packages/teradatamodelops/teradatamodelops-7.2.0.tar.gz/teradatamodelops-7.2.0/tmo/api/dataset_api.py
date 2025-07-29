from __future__ import absolute_import
from typing import Dict, List

from tmo.api.iterator_base_api import IteratorBaseApi


class DatasetApi(IteratorBaseApi):
    path = "/api/datasets"
    type = "DATASET"

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
        returns a list of datasets matching the name

        Parameters:
           name (str): dataset name(string) to match
           projection (str): projection type

        Returns:
            (list): list of datasets
        """
        query_vars = ["name", "projection"]
        query_vals = [name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByName",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_dataset_template_id(
        self,
        dataset_template_id: str,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns a dataset of a project by name

        Parameters:
           dataset_template_id (str): dataset_template_id
           archived (bool): archived or not (default False)
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): datasets
        """
        query_vars = [
            "datasetTemplateId",
            "archived",
            "projection",
            "page",
            "size",
            "sort",
        ]
        query_vals = [dataset_template_id, archived, projection, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByDatasetTemplateId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def save(self, dataset: Dict[str, str]):
        """
        register a dataset

        Parameters:
           dataset (dict): dataset to register

        Returns:
            (dict): dataset
        """
        return self.tmo_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=dataset,
        )

    def render(self, id: str) -> Dict:
        """
        returns a rendered dataset

        Parameters:
           id (str): dataset id

        Returns:
            (dict): rendered dataset
        """

        return self.tmo_client.get_request(
            path=f"{self.path}/{id}/render",
            header_params=self._get_header_params(),
            query_params={},
        )
