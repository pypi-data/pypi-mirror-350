import json
import os
import shutil
import logging
import yaml

from pathlib import Path
from git import Repo
from .train_model import TrainModel
from .evaluate_model import EvaluateModel
from .score_model import ScoreModel

MODEL_JSON = "model.json"


class RepoManager(object):

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = logging.getLogger(__name__)

    def add_model(
        self,
        model_id: str,
        model_name: str,
        model_desc: str,
        template: str,
        base_path: str = None,
    ):

        base_path = self.base_path if base_path is None else base_path
        model_path = os.path.join(base_path, "model_definitions")

        if not os.path.isdir(model_path):
            raise ValueError(f"model directory {model_path} does not exist")

        with open(os.path.join(template, MODEL_JSON), "r") as f:
            model = json.load(f)
            model["source_model_id"] = model["id"]
            model["id"] = model_id
            model["name"] = model_name
            model["description"] = model_desc

            name_path = model_name.strip().lower().replace(" ", "_")

            target_path = os.path.join(model_path, name_path)
            if os.path.isdir(target_path):
                raise ValueError(
                    f"Model path {name_path} already exists, please try another model"
                    " name"
                )

            shutil.copytree(template, target_path)

            with open(os.path.join(target_path, MODEL_JSON), "w") as t:
                json.dump(model, t, indent=4)

    def add_task(self, task: str, base_path: str = None):

        base_path = self.base_path if base_path is None else base_path
        task_path = os.path.join(base_path, "feature_engineering")

        if not os.path.exists(task_path):
            os.makedirs(task_path)

        for item in os.listdir(task):
            s = os.path.join(task, item)
            d = os.path.join(task_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    @staticmethod
    def clone_repository(url, path, branch: str = "master"):
        repo = Repo.clone_from(url, path)
        repo.git.checkout(branch)

    def get_templates(self, source_path: str = None):

        source_path = (
            self.base_path if source_path is None else os.path.join(source_path, "")
        )
        model_path = os.path.join(source_path, "model_definitions")

        # if no models / not models repo, return empty.
        if not os.path.isdir(model_path):
            return {}

        templates = {}

        for model in os.listdir(model_path):
            model_metadata_dir = os.path.join(model_path, model)
            model_metadata_file = os.path.join(model_metadata_dir, MODEL_JSON)
            if os.path.isfile(model_metadata_file):
                with open(model_metadata_file, "r") as f:
                    model_metadata = json.load(f)
                    if model_metadata["language"] not in templates:
                        templates[model_metadata["language"]] = {}
                    templates[model_metadata["language"]][model_metadata["id"]] = [
                        model_metadata["name"],
                        model_metadata_dir,
                    ]

        return templates

    def get_task(self, source_path: str = None):

        source_path = (
            self.base_path if source_path is None else os.path.join(source_path, "")
        )
        task_path = os.path.join(source_path, "feature_engineering")

        # if no task / not models repo, return empty
        if not os.path.isdir(task_path):
            return ""

        # Check for the existence of 'task.py' and 'requirements.txt'
        required_files = ["task.py", "requirements.txt"]
        existing_files = os.listdir(task_path)
        for file in required_files:
            if file not in existing_files:
                return ""

        return task_path

    def init_model_directory(self, path: str = None):
        logging.info("Creating model directory")
        if path is None:
            path = os.path.join(os.path.abspath(os.getcwd()), "")

        self.logger.info("Creating model definitions")

        src = os.path.join(os.path.split(__file__)[0], "") + "metadata_files"
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name) and not os.path.exists(
                os.path.join(path, file_name)
            ):
                shutil.copy(full_file_name, path)

        Path(f"{path}model_definitions/").mkdir(parents=True, exist_ok=True)

        self.logger.info(f"model directory initialized at {path}")

    def read_repo_config(self):
        self.repo_config_rename()
        path = os.path.join(self.base_path, ".tmo/config.yaml")
        if os.path.exists(path):
            with open(path, "r") as handle:
                return yaml.safe_load(handle)

        self.logger.warning("ModelOps repo config doesn't exist")
        return None

    def write_repo_config(self, config, path=None):
        path = path if path else self.base_path
        config_dir = os.path.join(path, ".tmo")
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        config_file = f"{config_dir}/config.yaml"

        with open(config_file, "w+") as f:
            yaml.dump(config, f, default_flow_style=False)

    def repo_config_exists(self, repo_path=None):
        path = repo_path if repo_path else self.base_path
        return Path(os.path.join(path, ".tmo")).is_file()

    def repo_config_rename(self, repo_path=None):
        path = repo_path if repo_path else self.base_path
        if Path(os.path.join(path, ".aoa")).is_file():
            os.rename(os.path.join(path, ".aoa"), os.path.join(path, ".tmo"))

    def train(self, model_id: str, data_conf: dict):
        trainer = TrainModel(self)
        trainer.train_model_local(
            model_id=model_id, rendered_dataset=data_conf, base_path=self.base_path
        )

    def evaluate(self, model_id: str, data_conf: dict):
        evaluator = EvaluateModel(self)
        evaluator.evaluate_model_local(
            model_id=model_id, rendered_dataset=data_conf, base_path=self.base_path
        )

    def batch_score_model_local(self, model_id: str, data_conf: dict):
        scorer = ScoreModel(self)
        scorer.batch_score_model_local(
            model_id=model_id, rendered_dataset=data_conf, base_path=self.base_path
        )
