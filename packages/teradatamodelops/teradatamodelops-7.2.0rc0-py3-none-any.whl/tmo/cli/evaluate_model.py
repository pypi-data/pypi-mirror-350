from .base_model import BaseModel
from ..context.model_context import ModelContext, DatasetInfo
import json
import os
import importlib
import logging
import shutil
import sys

ARTIFACTS_PATH = "./artifacts"
MODELS_PATH = "./models"


class EvaluateModel(BaseModel):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def evaluate_model_local(
        self, model_id: str, rendered_dataset: dict, base_path: str
    ):

        base_path = (
            self.repo_manager.model_catalog_path
            if base_path is None
            else os.path.join(base_path, "")
        )
        model_definitions_path = f"{base_path}model_definitions/"

        if not os.path.exists(model_definitions_path):
            raise ValueError(f"model directory {model_definitions_path} does not exist")

        model_artefacts_path = f".artefacts/{model_id}"
        model_evaluation_path = f"{model_artefacts_path}/evaluation"

        if not os.path.exists(f"{model_artefacts_path}/output"):
            raise ValueError("You must run training before trying to run evaluation.")

        if os.path.exists(model_evaluation_path):
            self.logger.debug(
                f"Cleaning local model evaluation path: {model_evaluation_path}"
            )
            shutil.rmtree(model_evaluation_path)

        os.makedirs(f"{model_evaluation_path}/output")

        try:
            self.__cleanup()

            os.makedirs(ARTIFACTS_PATH)

            os.symlink(
                f"../{model_artefacts_path}/output/",
                f"./{ARTIFACTS_PATH}/input",
                target_is_directory=True,
            )
            os.symlink(
                f"../{model_artefacts_path}/evaluation/output/",
                f"./{ARTIFACTS_PATH}/output",
                target_is_directory=True,
            )

            model_dir = model_definitions_path + BaseModel.get_model_folder(
                model_definitions_path, model_id
            )

            with open(f"{model_dir}/model.json", "r") as f:
                model_definition = json.load(f)

            with open(f"{model_dir}/config.json", "r") as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            cli_model_kargs = self._BaseModel__get_model_varargs(model_id)

            context = ModelContext(
                dataset_info=DatasetInfo.from_dict(rendered_dataset),
                hyperparams=model_conf["hyperParameters"],
                artifact_input_path="artifacts/input",
                artifact_output_path="artifacts/output",
                **cli_model_kargs,
            )

            engine = self._BaseModel__get_engine(model_definition, "evaluation")
            if engine == "python":
                sys.path.append(model_dir)
                if os.path.isfile(f"{model_dir}/model_modules/evaluation.py"):
                    evaluation = importlib.import_module(
                        ".evaluation", package="model_modules"
                    )
                else:
                    logging.debug(
                        "No evaluation.py found. Using scoring.py -> evaluate"
                    )
                    evaluation = importlib.import_module(
                        ".scoring", package="model_modules"
                    )

                evaluation.evaluate(
                    context=context,
                    data_conf=rendered_dataset,
                    model_conf=model_conf,
                    **cli_model_kargs,
                )

            elif engine == "sql":
                self.__evaluate_sql(
                    context, model_dir, rendered_dataset, model_conf, **cli_model_kargs
                )

            elif engine == "R":
                self._BaseModel__run_r_model(
                    model_id, model_dir, rendered_dataset, "evaluate"
                )

            else:
                raise Exception(f"Unsupported language: {model_definition['language']}")

            if os.path.exists(f"{model_artefacts_path}/evaluation/output/"):
                self.logger.info(
                    "Artefacts can be found in:"
                    f" {model_artefacts_path}/evaluation/output/"
                )
            else:
                self.logger.info(f"Artefacts can be found in: {model_artefacts_path}")

            if os.path.exists(f"{model_artefacts_path}/evaluation/output/metrics.json"):
                self.logger.info(
                    "Evaluation metrics can be found in:"
                    f" {model_artefacts_path}/evaluation/output/metrics.json"
                )

            if os.path.exists(f"{model_artefacts_path}/evaluation.json"):
                self.logger.info(
                    "Evaluation metrics can be found in:"
                    f" {model_artefacts_path}/evaluation.json"
                )

            self.__cleanup()
        except ModuleNotFoundError:
            model_dir = model_definitions_path + BaseModel.get_model_folder(
                model_definitions_path, model_id
            )
            self.__cleanup()
            self.logger.error(
                "Missing required python module, try running following command first:"
            )
            self.logger.error(
                f"pip install -r {model_dir}/model_modules/requirements.txt"
            )
            raise
        except:
            self.__cleanup()
            self.logger.exception("Exception running model code")
            raise

    def __cleanup(self):
        if os.path.exists(ARTIFACTS_PATH):
            shutil.rmtree(ARTIFACTS_PATH)
        try:
            os.remove(MODELS_PATH)
        except FileNotFoundError:
            self.logger.debug(
                f"Nothing to remove, folder '{MODELS_PATH}' does not exists."
            )

    def __evaluate_sql(self, context, model_dir, data_conf, model_conf, **kwargs):
        from tmo.util import tmo_create_context
        from teradataml import remove_context, DataFrame

        self.logger.info("Starting evaluation...")

        tmo_create_context()

        sql_file = f"{model_dir}/model_modules/evaluation.sql"
        jinja_ctx = {
            "context": context,
            "data_conf": data_conf,
            "model_conf": model_conf,
            "model_table": kwargs.get("model_table"),
            "model_version": kwargs.get("model_version"),
            "model_id": kwargs.get("model_id"),
        }

        self._BaseModel__execute_sql_script(sql_file, jinja_ctx)

        self.logger.info("Finished evaluation")

        stats = DataFrame(data_conf["metrics_table"]).to_pandas(all_rows=True)
        metrics = dict(zip(stats.key, stats.value))

        with open("models/evaluation.json", "w+") as f:
            json.dump(metrics, f)

        self.logger.info("Saved metrics")

        remove_context()
