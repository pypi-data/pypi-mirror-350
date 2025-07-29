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


class ScoreModel(BaseModel):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def batch_score_model_local(
        self, model_id: str = None, rendered_dataset: dict = None, base_path: str = None
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

        if not os.path.exists(f"{model_artefacts_path}/output"):
            raise ValueError("You must run training before trying to run scoring.")

        try:
            self.__cleanup()

            os.makedirs(ARTIFACTS_PATH)

            os.symlink(
                f"../{model_artefacts_path}/output/",
                f"{ARTIFACTS_PATH}/input",
                target_is_directory=True,
            )
            os.symlink(
                "../{}/output/".format(model_artefacts_path),
                f"{ARTIFACTS_PATH}/output",
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

            engine = self._BaseModel__get_engine(model_definition, "deployment")
            if engine == "python" or engine == "pyspark":
                sys.path.append(model_dir)
                scoring = importlib.import_module(".scoring", package="model_modules")

                scoring.score(
                    context=context,
                    data_conf=rendered_dataset,
                    model_conf=model_conf,
                    **cli_model_kargs,
                )

            elif engine == "sql":
                raise Exception("not supported")

            elif engine == "R":
                self._BaseModel__run_r_model(
                    model_id, model_dir, rendered_dataset, "score.batch"
                )

            else:
                raise Exception(f"Unsupported language: {model_definition['language']}")

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
