import runpy
import types
import inspect
from tmo.context.model_context import ModelContext, DatasetInfo
from tmo.cli.base_task import BaseTask
import shutil
import os
import logging
import subprocess


class RunTask(BaseTask):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def run_task_local(self, base_path: str, func: str = None):

        base_path = os.path.join(base_path, "")
        task_path = base_path + "feature_engineering/"

        if not os.path.exists(task_path):
            raise ValueError(
                "feature engineering task directory {0} does not exist".format(
                    task_path
                )
            )

        task_artefacts_path = ".artefacts/FE/"
        task_artefacts_abs_path = os.path.abspath(".artefacts/FE/")
        task_artefacts_output_path = ".artefacts/FE/output/"
        if os.path.exists(task_artefacts_path):
            self.logger.debug(
                "Cleaning local model artefact path: {}".format(task_artefacts_path)
            )
            shutil.rmtree(task_artefacts_path)

        os.makedirs(task_artefacts_output_path)

        try:
            if os.path.exists("./artifacts"):
                os.remove("./artifacts")

            if os.name == "nt":
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", "artifacts", task_artefacts_abs_path],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            else:
                os.symlink(task_artefacts_path, "./artifacts", target_is_directory=True)

            cli_task_kargs = self._BaseTask__get_task_varargs()

            context = ModelContext(
                artifact_output_path="artifacts/output",
                dataset_info=DatasetInfo.from_dict({}),
                hyperparams={},
                **cli_task_kargs,
            )

            task_file_path = os.path.join(task_path, "task.py")
            if not os.path.exists(task_file_path):
                raise ValueError(f"Task file {task_file_path} does not exist")

            task_module = runpy.run_path(task_file_path)

            if not func:
                function_names = [
                    name
                    for name, value in task_module.items()
                    if isinstance(value, types.FunctionType)
                    and inspect.getfile(value) == task_file_path
                ]
                func = self.__input_select(
                    "function", function_names, "Available functions:"
                )

            print("")

            if func in task_module and isinstance(
                task_module[func], types.FunctionType
            ):
                self.logger.info("Loading and executing task code")
                task_module[func](context=context)
            else:
                raise ValueError(f"{func} function not found in task.py")

            self.logger.info(
                "Artefacts can be found in: {}".format(task_artefacts_output_path)
            )
            self.__cleanup()
            return func
        except ModuleNotFoundError:
            self.__cleanup()
            self.logger.error(
                "Missing required python module, try running following command first:"
            )
            self.logger.error("pip install -r {}requirements.txt".format(task_path))
            raise
        except:
            self.__cleanup()
            self.logger.exception("Exception running feature engineering task code")
            raise

    def __cleanup(self):
        if os.path.exists("./artifacts"):
            os.remove("./artifacts")

    def __print_underscored(self, message):
        print(message)
        print("-" * len(message))

    def __input_select(self, name, values, label="", default=None):
        if len(values) == 0:
            return

        if label != "":
            self.__print_underscored(label)

        for ix, item in enumerate(values):
            default_text = " (default)" if default and default == item else ""
            print("[{}] {}".format(ix, item) + default_text)

        tmp_index = (
            input(
                "Select {} by index (or leave blank for the default one): ".format(name)
            )
            if default
            else input("Select {} by index: ".format(name))
        )

        if default and default in values and tmp_index == "":
            tmp_index = values.index(default)
        elif (tmp_index == "" and not default) or (
            not tmp_index.isnumeric() or int(tmp_index) >= len(values)
        ):
            print(
                "Wrong selection, please try again by selecting the index number on the"
                " first column."
            )
            print("You may cancel at anytime by pressing Ctrl+C.")
            print("")
            return self.__input_select(name, values, label, default)

        return values[int(tmp_index)]
