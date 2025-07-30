"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""

import logging
import os

from midas.scenario.upgrade_module import UpgradeModule
from midas.util.dict_util import set_default_bool

LOG = logging.getLogger(__name__)


class DatabaseModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="store",
            default_scope_name="database",
            default_sim_config_name="MidasStore",
            default_import_str="midas_store.simulator:MidasCSVStore",
            default_cmd_str=("%(python)s -m midas_store.simulator %(addr)s"),
            log=LOG,
        )
        self.default_filename = "midas_store.csv"
        self._filename = None
        self._path = None
        self._unique_filename = False
        self._keep_old_files = False

    def check_module_params(self, module_params):
        """Check module params for this upgrade."""

        module_params.setdefault(self.default_scope_name, dict())
        module_params.setdefault("filename", self.default_filename)
        module_params.setdefault("path", self.scenario.base.output_path)
        set_default_bool(module_params, "unique_filename", False)
        set_default_bool(module_params, "keep_old_files", False)

    def check_sim_params(self, module_params):
        self._filename = module_params["filename"]
        self._path = module_params["path"]
        self._unique_filename = module_params["unique_filename"]
        self._keep_old_files = module_params["keep_old_files"]

    def start_models(self):
        mod_key = "database"
        params = {
            "filename": self._filename,
            "path": self._path,
            "unique_filename": self._unique_filename,
            "keep_old_files": self._keep_old_files,
        }

        self.start_model(mod_key, "DatabaseCSV", params)

    def connect(self):
        pass

    def connect_to_db(self):
        pass
