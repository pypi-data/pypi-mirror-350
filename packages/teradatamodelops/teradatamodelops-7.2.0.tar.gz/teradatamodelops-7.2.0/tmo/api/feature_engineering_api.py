from __future__ import absolute_import
from typing import Dict, List

from tmo.api.iterator_base_api import IteratorBaseApi


class FeatureEngineeringApi(IteratorBaseApi):

    path = "/api/featureEngineeringTasks"
    type = "FEATURE_ENGINEERING"

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

    def import_task(self, import_request: Dict[str, str]):
        """
        import a feature engineering task

        Parameters:
            import_request (dict): request to import model version

        Returns:
            (dict): job
        """
        self.required_params(
            ["artefactImportId", "name", "description", "language", "functionName"],
            import_request,
        )

        return self.tmo_client.post_request(
            path=f"{self.path}/import",
            header_params=self._get_header_params(),
            query_params={},
            body=import_request,
        )

    def run(self, task_id: str, run_request: Dict[str, str]):
        """
        run feature engineering task

        Parameters:
            task_id (str): model id(uuid)
            run_request (dict): request to import model version

        Returns:
            (dict): job
        """
        self.required_params(["automation", "datasetConnectionId"], run_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{task_id}/run",
            header_params=self._get_header_params(),
            query_params={},
            body=run_request,
        )

    def approve(self, task_id: str, comments: str):
        """
        approve a feature engineering task
        :param task_id:  task id
        :param comments: approval comments
        :return:
        """

        approve_request = dict()
        approve_request["comments"] = comments

        return self.tmo_client.post_request(
            path=f"{self.path}/{task_id}/approve",
            header_params=self._get_header_params(),
            query_params={},
            body=approve_request,
        )

    def reject(self, task_id: str, comments: str):
        """
        reject a feature engineering task
        :param task_id:  task id
        :param comments: approval comments
        :return:
        """

        reject_request = dict()
        reject_request["comments"] = comments

        return self.tmo_client.post_request(
            path=f"{self.path}/{task_id}/approve",
            header_params=self._get_header_params(),
            query_params={},
            body=reject_request,
        )

    def deploy(self, task_id: str, deploy_request: dict):
        """
        deploy a trained model
        :param task_id:  fe task id
        :param deploy_request: deployment request
        :return:
        """
        self.required_params(["engineType"], deploy_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{task_id}/deploy",
            header_params=self._get_header_params(),
            query_params={},
            body=deploy_request,
        )

    def retire(self, task_id: str, retire_request: dict):
        """
        retire a trained model
        :param task_id:  fe task id
        :param retire_request: retire request
        :return:
        """
        self.required_params(["deploymentId"], retire_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{task_id}/retire",
            header_params=self._get_header_params(),
            query_params={},
            body=retire_request,
        )
