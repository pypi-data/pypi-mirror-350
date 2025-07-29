from tmo.cli.base_model import BaseModel
from tmo.context.model_context import ModelContext, DatasetInfo
import shutil
import os
import json
import logging
import importlib
import sys
import subprocess

ARTIFACTS_PATH = "./artifacts"
MODELS_PATH = "./models"


class TrainModel(BaseModel):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def train_model_local(self, model_id: str, rendered_dataset: dict, base_path: str):

        base_path = (
            self.repo_manager.model_catalog_path
            if base_path is None
            else os.path.join(base_path, "")
        )
        model_definitions_path = f"{base_path}model_definitions/"

        if not os.path.exists(model_definitions_path):
            raise ValueError(f"model directory {model_definitions_path} does not exist")

        model_artefacts_path = f".artefacts/{model_id}/"
        model_artefacts_abs_path = os.path.abspath(f".artefacts/{model_id}/")
        model_artefacts_output_path = f".artefacts/{model_id}/output/"
        if os.path.exists(model_artefacts_path):
            self.logger.debug(
                f"Cleaning local model artefact path: {model_artefacts_path}"
            )
            shutil.rmtree(model_artefacts_path)

        os.makedirs(model_artefacts_output_path)

        try:
            if os.path.exists(ARTIFACTS_PATH):
                os.remove(ARTIFACTS_PATH)

            if os.name == "nt":
                subprocess.run(
                    [
                        "cmd",
                        "/c",
                        "mklink",
                        "/J",
                        "artifacts",
                        model_artefacts_abs_path,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            else:
                os.symlink(
                    model_artefacts_path, ARTIFACTS_PATH, target_is_directory=True
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
                artifact_output_path="artifacts/output",
                **cli_model_kargs,
            )

            engine = self._BaseModel__get_engine(model_definition, "training")
            if engine == "python":
                sys.path.append(model_dir)
                training = importlib.import_module(".training", package="model_modules")
                training.train(
                    context=context,
                    data_conf=rendered_dataset,
                    model_conf=model_conf,
                    **cli_model_kargs,
                )

            elif engine == "sql":
                self.__train_sql(
                    context, model_dir, rendered_dataset, model_conf, **cli_model_kargs
                )

            elif engine == "R":
                self._BaseModel__run_r_model(
                    model_id, model_dir, rendered_dataset, "train"
                )

            else:
                raise Exception(f"Unsupported engine: {engine}")

            self.logger.info(
                f"Artefacts can be found in: {model_artefacts_output_path}"
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
            os.remove(ARTIFACTS_PATH)
        if os.path.exists(MODELS_PATH):
            os.remove(MODELS_PATH)

    def __train_sql(self, context, model_dir, data_conf, model_conf, **kwargs):
        from tmo.util import tmo_create_context
        from teradataml import remove_context

        self.logger.info("Starting training...")

        tmo_create_context()

        sql_file = f"{model_dir}/model_modules/training.sql"
        jinja_ctx = {
            "context": context,
            "data_conf": data_conf,
            "model_conf": model_conf,
            "model_table": kwargs.get("model_table"),
            "model_version": kwargs.get("model_version"),
            "model_id": kwargs.get("model_id"),
        }

        self._BaseModel__execute_sql_script(sql_file, jinja_ctx)

        remove_context()

        self.logger.info("Finished training")

        self.logger.info("Saved trained model")

        remove_context()
