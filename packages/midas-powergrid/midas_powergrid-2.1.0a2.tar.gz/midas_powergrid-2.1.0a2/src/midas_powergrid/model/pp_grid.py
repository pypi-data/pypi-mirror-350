import logging
from importlib import import_module

import pandapower as pp
import pandapower.networks as pn
import simbench as sb

from ..custom import bhv, midaslv, midasmv

LOG = logging.getLogger(__name__)


class PPGrid:
    def __init__(self, grid_name, grid_params):
        self._grid = None
        self.plot_type: str = "cigre"
        self._numba = not grid_params.get("disable_numba", False)

        if grid_name == "midasmv":
            self._grid = midasmv.build_grid(**grid_params)
        elif grid_name == "midaslv":
            self._grid = midaslv.build_grid(**grid_params)
        elif grid_name == "bhv":
            self._grid = bhv.build_grid(**grid_params)
            self.plot_type = "other"
        elif grid_name == "cigre_hv":
            self._grid = pn.create_cigre_network_hv(**grid_params)
        elif grid_name == "cigre_mv":
            self._grid = pn.create_cigre_network_mv(**grid_params)
        elif grid_name == "cigre_lv":
            self._grid = pn.create_cigre_network_lv(**grid_params)
        elif grid_name in ("oberrhein", "mv_obverrhein"):
            self._grid = pn.mv_oberrhein()
        elif grid_name.endswith(".json"):
            self._grid = pp.from_json(grid_name)
            self.plot_type = "other"
        elif grid_name.endswith(".xlsx"):
            self._grid = pp.from_excel(grid_name)
        elif self._load_simbench(grid_name):
            self.plot_type = "simbench"
        elif "." in grid_name:
            if ":" in grid_name:
                mod, clazz = grid_name.split(":")
            else:
                mod, clazz = grid_name.rsplit(".", 1)
            mod = import_module(mod)
            self._grid = getattr(mod, clazz)()
            self.plot_type = "other"
        else:
            self._grid = getattr(pn, grid_name)()
            self.plot_type = "other"

    def set_value(self, etype, idx, attr, val):
        self._grid[etype].at[idx, attr] = val

    def run_powerflow(self):
        pp.runpp(self._grid, numba=self._numba)

    def get_value(self, etype, idx=None, attr=None):
        if idx is None and attr is None:
            return self._grid[etype]
        elif attr is None:
            return self._grid[etype].iloc[idx]
        elif idx is None:
            return self._grid[etype][attr]
        else:
            return self._grid[etype].at[idx, attr]

    def get_outputs(self):
        raise NotImplementedError

    def to_json(self) -> str:
        json_str = ""
        try:
            json_str = pp.to_json(self._grid)
        except Exception:
            LOG.exception("Failed to convert grid into json:")

        return json_str

    def _load_simbench(self, gridfile):
        """Try to load a simbench grid.

        Importing the simbench module is done here because that takes
        a few seconds to load, which are wasted if simbench is not used
        at all.

        """

        try:
            self._grid = sb.get_simbench_net(gridfile)
        except ValueError:
            return False

        return True

    def finalize(self):
        pass
