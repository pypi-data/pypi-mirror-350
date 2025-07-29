import yaml
import os


class BaseTask(object):

    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def __get_task_varargs(self):
        return {"project_id": self.__get_project_id(), "job_id": "cli"}

    def __get_project_id(self):
        self.repo_manager.repo_config_rename(self.repo_manager.base_path)
        path = os.path.join(self.repo_manager.base_path, ".tmo/config.yaml")
        with open(path, "r") as handle:
            return yaml.safe_load(handle)["project_id"]
