from __future__ import absolute_import
from typing import Dict

from tmo.api.iterator_base_api import IteratorBaseApi


class TrainedModelApi(IteratorBaseApi):

    path = "/api/trainedModels"
    type = "TRAINED_MODEL"

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

    def find_dataset(self, trained_model_id: str, projection: str = None):
        """
        returns dataset of a trained model

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type

        Returns:
            (dict): dataset
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/{trained_model_id}/dataset",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_events(self, trained_model_id: str, projection: str = None):
        """
        returns trained model events

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type

        Returns:
            (dict): events of trained model
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/{trained_model_id}/events",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_model_id(self, model_id: str, projection: str = None):
        """
        returns a trained models by model id

        Parameters:
           model_id (str): model id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): trained models
        """
        query_vars = ["modelId", "projection"]
        query_vals = [model_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByModelId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_model_id_and_status(
        self, model_id: str, status: str, projection: str = None
    ):
        """
        returns a trained models by model id

        Parameters:
           model_id (str): model id(uuid) to find
           status (str): model status
           projection (str): projection type

        Returns:
            (dict): trained models
        """
        query_vars = ["modelId", "status", "projection"]
        query_vals = [model_id, status, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByModelIdAndStatus",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def evaluate(self, trained_model_id: str, evaluation_request: Dict[str, str]):
        """
        evaluate a model

        Parameters:
           trained_model_id (str): trained model id(uuid) to evaluate
           evaluation_request (dict): request to evaluate trained model

        Returns:
            (dict): job
        """
        self.required_params(["datasetId"], evaluation_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{trained_model_id}/evaluate",
            header_params=self._get_header_params(),
            query_params={},
            body=evaluation_request,
        )

    def approve(self, trained_model_id: str, comments: str):
        """
        approve a trained model
        :param trained_model_id:  model version
        :param comments: approval comments
        :return:
        """
        approve_request = dict()
        approve_request["comments"] = comments

        return self.tmo_client.post_request(
            path=f"{self.path}/{trained_model_id}/approve",
            header_params=self._get_header_params(),
            query_params={},
            body=approve_request,
        )

    def reject(self, trained_model_id: str, comments: str):
        """
        reject a trained model
        :param trained_model_id:  model version
        :param comments: approval comments
        :return:
        """
        reject_request = dict()
        reject_request["comments"] = comments

        return self.tmo_client.post_request(
            path=f"{self.path}/{trained_model_id}/reject",
            header_params=self._get_header_params(),
            query_params={},
            body=reject_request,
        )

    def deploy(self, trained_model_id: str, deploy_request: dict):
        """
        deploy a trained model
        :param trained_model_id:  model version
        :param deploy_request: deployment request
        :return:
        """
        self.required_params(["engineType"], deploy_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{trained_model_id}/deploy",
            header_params=self._get_header_params(),
            query_params={},
            body=deploy_request,
        )

    def retire(self, trained_model_id: str, retire_request: dict):
        """
        retire a trained model
        :param trained_model_id:  model version
        :param retire_request: retire request
        :return:
        """
        self.required_params(["deploymentId"], retire_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{trained_model_id}/retire",
            header_params=self._get_header_params(),
            query_params={},
            body=retire_request,
        )
