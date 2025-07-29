from __future__ import absolute_import
from typing import Dict

from tmo.api.iterator_base_api import IteratorBaseApi


class DatasetConnectionApi(IteratorBaseApi):
    path = "/api/datasetConnections"
    type = "DATASET_CONNECTION"

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        raise NotImplementedError("Archiving not supported for DatasetConnections")

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

    def save(self, dataset_connection: Dict[str, str]):
        """
        register a dataset connection

        Parameters:
           dataset connection (dict): dataset connection to register

        Returns:
            (dict): dataset template
        """

        return self.tmo_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=dataset_connection,
        )

    def validate(
        self, dataset_connection: Dict[str, str], encrypted_credentials: bool = False
    ):
        """
        validate a dataset connection

        Parameters:
           dataset connection (dict): dataset connection to validate
           encrypted_credentials (bool): flag to indicate if credentials are encrypted

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        dataset_connection["credentials"]["credsEncrypted"] = encrypted_credentials

        return self.tmo_client.post_request(
            path=f"{self.path}/validate",
            header_params=self._get_header_params(),
            query_params={},
            body=dataset_connection,
        )
