"""This module contains the MIDAS powergrid upgrade."""

import json
import logging
import os
from importlib import import_module

import numpy as np
from midas.scenario.upgrade_module import UpgradeModule
from midas.util.dict_util import (
    set_default_bool,
    set_default_float,
)

from .analysis.grid import analyze_grid
from .meta import ATTRIBUTE_MAP

LOG = logging.getLogger(__name__)


class PowergridModule(UpgradeModule):
    """The MIDAS powergrid update module."""

    def __init__(self):
        super().__init__(
            module_name="powergrid",
            default_scope_name="midasmv",
            default_sim_config_name="Powergrid",
            default_import_str=(
                "midas_powergrid.simulator:PandapowerSimulator"
            ),
            default_cmd_str=(
                "%(python)s -m midas_powergrid.simulator %(addr)s"
            ),
            log=LOG,
        )

        self.models = {}
        for entity, data in ATTRIBUTE_MAP.items():
            self.models.setdefault(entity, [])
            for attrs in data.values():
                for attr in attrs:
                    self.models[entity].append(attr)

        self._double_actuator_values: bool = False

    def check_module_params(self, module_params: dict):
        """Check the module params for this upgrade."""

        set_default_bool(module_params, "plotting", False)
        module_params.setdefault(
            "plot_path",
            os.path.abspath(
                os.path.join(self.scenario.base.output_path, "plots")
            ),
        )
        set_default_bool(module_params, "save_grid_json", False)
        module_params.setdefault("constraints", [])
        set_default_float(module_params, "actuator_multiplier", 1.0)
        set_default_bool(module_params, "exclude_slack_bus", False)

    def check_sim_params(self, module_params: dict):
        """Check simulator params for a certain simulator."""

        self.sim_params.setdefault("gridfile", self.default_scope_name)
        self.sim_params.setdefault("grid_params", {})
        set_default_bool(
            self.sim_params, "plotting", module_params["plotting"]
        )
        self.sim_params.setdefault("plot_path", module_params["plot_path"])
        set_default_bool(
            self.sim_params, "save_grid_json", module_params["save_grid_json"]
        )
        self.sim_params.setdefault("constraints", module_params["constraints"])
        set_default_float(
            self.sim_params,
            "actuator_multiplier",
            module_params["actuator_multiplier"],
        )
        self.sim_params.setdefault("grid_mapping", {})
        set_default_bool(
            self.sim_params,
            "exclude_slack_bus",
            module_params["exclude_slack_bus"],
        )

    def start_models(self):
        """Start all models for this simulator.

        Since we want the grids to be able to be interconnected with
        each other, each grid model should have its own simulator.

        Parameters
        ----------
        sim_name : str
            The sim name, not to be confused with *sim_name* for
            mosaik's *sim_config*. **This** sim_name is the simulator
            key in the configuration yaml file.

        """
        model_key = self.scenario.generate_model_key(self)

        model_params = {
            "gridfile": self.sim_params["gridfile"],
            "pp_params": self.sim_params["grid_params"],
            "constraints": self.sim_params["constraints"],
            "include_slack_bus": not self.sim_params["exclude_slack_bus"],
        }

        self.start_model(model_key, "Grid", model_params)

        if ":" in self.default_import_str:
            mod, clazz = self.default_import_str.split(":")
        else:
            mod, clazz = self.default_import_str.rsplit(".", 1)
        mod = import_module(mod)

        sim_dummy = getattr(mod, clazz)()
        sim_dummy.init(self.sid, **self.sim_params)
        entities = sim_dummy.create(1, "Grid", **model_params)
        grid_obj = sim_dummy.models[entities[0]["eid"]].grid
        self.scenario.add_to_model_extra_data(
            model_key, self.sim_key, {"grid": grid_obj}
        )
        self.scenario.add_to_world_state("grid_json", grid_obj.to_json())
        self.scenario.add_to_world_state(
            "grid_dict", json.loads(grid_obj.to_json())
        )

        # Backwards compatibility
        # Only works for midasmv anyways
        self._double_actuator_values = model_params["pp_params"].get(
            "double_actuator_values", False
        )
        if self._double_actuator_values:
            self.sim_params["actuator_multiplier"] = 2.0

        for entity in entities[0]["children"]:
            eid = entity["eid"]
            parts = eid.split("-")
            child_key = f"{model_key}"
            for part in parts[1:]:
                child_key += f"_{part}"

            self.scenario.script.model_start.append(
                f"{child_key} = [e for e in {model_key}.children "
                f'if e.eid == "{eid}"][0]\n'
            )
            self.scenario.add_model(
                child_key,
                self.sim_key,
                f"{entity['type']}",
                {},
                f"{self.sid}.{eid}",
                f"{self.sid}.{entities[0]['eid']}",
            )

    def connect(self, *args):
        # Nothing to do so far
        # Maybe to other grids in the future?
        pass

    def connect_to_db(self):
        """Add connections to the database."""

        grid_key = self.scenario.generate_model_key(self)
        db_key = self.scenario.find_first_model("store", "database")[0]
        if db_key is None:
            LOG.warning(
                "Could not find DB key in scenario. No connection to DB "
                "possible."
            )
            return
        for key, entity in self.scenario.get_models(self.sim_key).items():
            if grid_key not in key:
                continue
            mod_key = key

            # We only want to connect those attributes that are present
            # in the grid. That's why we iterate over existing entities
            # and not simply use the models defined above.
            if entity["name"] in self.models:
                self.connect_entities(
                    mod_key,
                    db_key,
                    [a[0] for a in self.models[entity["name"]]],
                )

        additional_attrs: list[str | tuple[str, str]] = ["health"]

        if self.sim_params["save_grid_json"]:
            additional_attrs.append("grid_json")

        self.connect_entities(grid_key, db_key, additional_attrs)

    def get_sensors(self):
        models = self.scenario.get_models(self.sim_key)
        for model_key, config in models.items():
            if config["name"] in self.models:
                for attr in self.models[config["name"]]:
                    name, dtype, low, high = attr

                    if dtype == "bool":
                        space = _int_box()
                    elif dtype == "int":
                        space = _int_box(low, high)
                    else:
                        space = _float_box(low, high)

                    self.scenario.sensors.append(
                        {"uid": f"{config['full_id']}.{name}", "space": space}
                    )

        grid_key = self.scenario.generate_model_key(self)
        grid = self.scenario.get_model(grid_key)
        assert grid is not None
        self.scenario.sensors.append(
            {"uid": f"{grid['full_id']}.health", "space": _float_box(0, 1.2)}
        )
        # self.scenario.sensors.append(
        #     {
        #         "uid": f"{grid.full_id}.grid_json",
        #         "space": ("Box(low=0, high=1, shape=(), dtype=np.float32)"),
        #     }
        # )

    def get_actuators(self):
        grid_key = self.scenario.generate_model_key(self)
        grid = self.scenario.get_model(grid_key)
        if grid is None:
            msg = "Grid object is None. Something went wrong, sorry!"
            raise ValueError(msg)

        models = self.scenario.get_models(self.sim_key)
        for model_key, config in models.items():
            if config["name"] == "Trafo":
                self.scenario.actuators.append(
                    {
                        "uid": f"{config['full_id']}.delta_tap_pos",
                        "space": _int_box(-1, 1),
                    }
                )
                tmin = tmax = 0
                etype = ""
                try:
                    pp_grid = grid["extra_data"]["grid"]
                    _, etype, eidx = config["eid"].split("-")
                    try:
                        tmax = pp_grid.get_value(etype, int(eidx), "tap_max")
                        tmin = pp_grid.get_value(etype, int(eidx), "tap_min")
                        if np.isnan(tmin) or np.isnan(tmax):
                            raise KeyError(f"Trafo {etype} has no tmin/max")
                    except KeyError:
                        LOG.debug(
                            "No tap_min or tap_max found. Using maximum "
                            " integer values as limits."
                        )
                        tmin = np.iinfo(np.int32).min
                        tmax = np.iinfo(np.int32).max
                except Exception as err:
                    # print(err)
                    LOG.warning(
                        "Caught an error composing actuator information for "
                        f"{etype} with eid {config['eid']}: {type(err), err}. "
                        "Continuing with maximum integer values as limits.",
                        exc_info=err,
                    )
                    tmin = np.iinfo(np.int32).min
                    tmax = np.iinfo(np.int32).max
                self.scenario.actuators.append(
                    {
                        "uid": f"{config['full_id']}.tap_pos",
                        "space": _int_box(tmin, tmax),
                    }
                )
            if config["name"] == "Switch":
                self.scenario.actuators.append(
                    {
                        "uid": f"{config['full_id']}.closed",
                        "space": _int_box(0, 1),
                    }
                )
            if config["name"] in ("Load", "Sgen", "Storage"):
                q_min = 0
                p_min = 0
                etype = ""
                try:
                    pp_grid = grid["extra_data"]["grid"]
                    _, etype, eidx, _ = config["eid"].split("-")
                    try:
                        p_max = pp_grid.get_value(etype, int(eidx), "max_p_mw")
                        p_min = pp_grid.get_value(etype, int(eidx), "min_p_mw")
                    except KeyError:
                        LOG.debug(
                            "No max_p_mw or min_p_mw found, using p_mw as "
                            "p_max and set p_min to 0"
                        )
                        p_max = pp_grid.get_value(etype, int(eidx), "p_mw")

                    try:
                        q_max = pp_grid.get_value(
                            etype, int(eidx), "max_q_mvar"
                        )
                        q_min = pp_grid.get_value(
                            etype, int(eidx), "min_q_mvar"
                        )
                    except KeyError:
                        LOG.debug(
                            "No max_p_mw or min_p_mw found, using q_mvar as "
                            "q_max and set q_min to 0"
                        )
                        q_max = pp_grid.get_value(etype, int(eidx), "q_mvar")

                except Exception as err:
                    # print(err)
                    LOG.warning(
                        "Caught an error composing actuator information for "
                        f"{etype} with eid {config['eid']}: {type(err), err}. "
                        "Continuing with p_max=0.5, q_max=0.5, and "
                        "p_min=q_min=0.",
                        exc_info=err,
                    )
                    p_max = 0.5
                    q_max = 0.5

                p_max *= self.sim_params["actuator_multiplier"]
                q_max *= self.sim_params["actuator_multiplier"]

                if q_max < q_min:
                    q_min = q_max
                    q_max = 0

                if p_min < p_max:
                    self.scenario.actuators.append(
                        {
                            "uid": f"{config['full_id']}.p_mw",
                            "space": _float_box(p_min, p_max),
                        }
                    )
                if q_min < q_max:
                    self.scenario.actuators.append(
                        {
                            "uid": f"{config['full_id']}.q_mvar",
                            "space": _float_box(q_min, q_max),
                        }
                    )

    def analyze(self, name, data, output_folder, start, end, step_size, full):
        grid_sim_keys = [
            sim_key for sim_key in data.keys() if "Powergrid" in sim_key
        ]
        for sim_key in grid_sim_keys:
            grid_data = data[sim_key]
            if start > 0:
                grid_data = grid_data.iloc[start:]
            if end > 0:
                grid_data = grid_data.iloc[:end]

            analyze_grid(
                grid_data,
                step_size,
                f"{name}-{sim_key.replace('/', '')}",
                output_folder,
                full,
            )

    def download(self, *args):  # type: ignore[reportIncompatibleMethodOverride]
        # No downloads, suppress logging output
        pass


def _float_box(low=0.0, high=1.0):
    return f"Box(low={low}, high={high}, shape=(), dtype=np.float32)"


def _int_box(low=0, high=1):
    return f"Box(low={low}, high={high}, shape=(), dtype=np.int32)"
