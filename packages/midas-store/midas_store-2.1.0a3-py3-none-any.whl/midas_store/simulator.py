import mosaik_api_v3
from midas.util.dict_util import bool_from_dict
from midas.util.logging import set_and_init_logger
from mosaik.exceptions import SimulationError
from mosaik_api_v3.types import (
    CreateResult,
    EntityId,
    Meta,
    ModelName,
    OutputData,
    OutputRequest,
    SimId,
)
from typing_extensions import override

from . import LOG
from .csv_model import CSVModel
from .meta import META


class MidasCSVStore(mosaik_api_v3.Simulator):
    """Simulator to store simulation results in a csv file."""

    def __init__(self) -> None:
        super().__init__(META)

        self.sid: SimId | None = None
        self.eid: EntityId = "Database-0"
        self.database: CSVModel | None = None

        self.filename: str | None = None
        self.step_size: int = 0
        self.current_size: int = 0
        self.saved_rows: int = 0
        self.finalized: bool = False
        self.keep_old_files: bool = True

    @override
    def init(
        self, sid: SimId, time_resolution: float = 1.0, **sim_params
    ) -> Meta:
        self.sid = sid
        self.step_size = sim_params.get("step_size", 900)

        return self.meta

    @override
    def create(
        self, num: int, model: ModelName, **model_params
    ) -> list[CreateResult]:
        if num > 1 or self.database is not None:
            errmsg = (
                "You should really not try to instantiate more than one "
                "database. If your need another database, create a new "
                "simulator as well."
            )
            raise ValueError(errmsg)

        self.database = CSVModel(
            model_params.get("filename", ""),
            path=model_params.get("path", None),
            unique_filename=bool_from_dict(
                model_params, "unique_filename", False
            ),
            keep_old_files=bool_from_dict(
                model_params, "keep_old_files", False
            ),
        )

        return [{"eid": self.eid, "type": model}]

    @override
    def step(self, time, inputs, max_advance=0):
        if self.database is None:
            msg = "Database is unexpectedly None. Can not proceed any further"
            raise SimulationError(msg)

        data = inputs.get(self.eid, {})

        if not data:
            LOG.info(
                "Did not receive any inputs. "
                "Did you connect anything to the store?"
            )

        for attr, src_ids in data.items():
            for src_id, val in src_ids.items():
                sid, eid = src_id.split(".")
                self.database.to_memory(sid, eid, attr, val)

        self.database.step()

        return time + self.step_size

    @override
    def get_data(self, outputs: OutputRequest) -> OutputData:
        return {}

    @override
    def finalize(self):
        LOG.info("Finalizing database.")
        if self.database is not None:
            self.database.finalize()


if __name__ == "__main__":
    set_and_init_logger(0, "store-logfile", "midas-store.log", replace=True)

    mosaik_api_v3.start_simulation(MidasCSVStore())
