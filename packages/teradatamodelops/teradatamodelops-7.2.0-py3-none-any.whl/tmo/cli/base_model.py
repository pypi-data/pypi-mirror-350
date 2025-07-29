import logging
import json
import yaml
import os
from jinja2 import Template


class BaseModel(object):

    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    @staticmethod
    def get_model_ids(model_path, rtn_val=False):
        catalog = {}
        index = 0
        model_ids = "Use one of the following models\n"

        for model_folder in os.listdir(model_path):
            if os.path.exists(model_path + model_folder + "/model.json"):
                with open(model_path + model_folder + "/model.json", "r") as f:
                    model_definition = json.load(f)
                    catalog[index] = model_definition
                    index += 1

        for key in catalog:
            model_ids += "{1}: {0}\n".format(catalog[key]["id"], catalog[key]["name"])

        if rtn_val:
            return catalog

        raise ValueError(model_ids)

    @staticmethod
    def get_model_folders(model_path, rtn_val=False):
        catalog = {}
        index = 0
        model_ids = "Use one of the following models\n"

        for model_folder in os.listdir(model_path):
            if os.path.exists(model_path + model_folder + "/model.json"):
                with open(model_path + model_folder + "/model.json", "r") as f:
                    model_definition = json.load(f)
                    catalog[index] = model_definition
                    index += 1

        for key in catalog:
            model_ids += "{1}: {0}\n".format(model_folder, catalog[key]["name"])

        if rtn_val:
            return catalog

        raise ValueError(model_ids)

    @staticmethod
    def get_model_folder(model_path: str, model_id: str):
        for model_folder in os.listdir(model_path):
            if os.path.exists(model_path + model_folder + "/model.json"):
                with open(model_path + model_folder + "/model.json", "r") as f:
                    model_definition = json.load(f)
                    if model_definition["id"] == model_id:
                        return model_folder

        raise ValueError("Could not find model path for model_id: {}".format(model_id))

    def __get_model_varargs(self, model_id):
        return {
            "model_id": model_id,
            "model_version": "cli",
            "model_table": "vmo_models_cli",
            "project_id": self.__get_project_id(),
            "job_id": "cli",
        }

    def __get_project_id(self):
        self.repo_manager.repo_config_rename(self.repo_manager.base_path)
        path = os.path.join(self.repo_manager.base_path, ".tmo/config.yaml")
        with open(path, "r") as handle:
            return yaml.safe_load(handle)["project_id"]

    def __template_sql_script(self, filename, jinja_ctx):
        with open(filename) as f:
            template = Template(f.read(), autoescape=True)

        return template.render(jinja_ctx)

    def __execute_sql_script(self, filename, jinja_ctx):
        from ..util.connections import execute_sql

        script = self.__template_sql_script(filename, jinja_ctx)

        stms = script.split(";")

        for stm in stms:
            stm = stm.strip()
            if stm:
                logging.info("Executing statement: {}".format(stm))

                try:
                    execute_sql(stm)
                except Exception as e:
                    if stm.startswith("DROP"):
                        logging.warning("Ignoring DROP statement exception")
                    else:
                        raise e

    def __get_engine(self, model_definition, mode):
        if "automation" in model_definition:

            if (
                mode in model_definition["automation"]
                and "engine" in model_definition["automation"][mode]
            ):
                return model_definition["automation"][mode]["engine"]

            # legacy
            if "trainingEngine" in model_definition["automation"]:
                return model_definition["automation"]["trainingEngine"]

        return model_definition["language"]

    def __run_r_model(self, model_id, model_dir, data_conf, mode):
        import tempfile
        import subprocess

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(json.dumps(data_conf).encode())

        pkg_path, _ = os.path.split(__file__)
        cmd = (
            f"{pkg_path}/run_model.R"
            f" {model_id} {self.__get_project_id()} {mode} {fp.name} {model_dir}"
        )
        subprocess.check_call(cmd, shell=True)
