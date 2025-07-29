import logging

import pandapower as pp

from ..constraints.line_loading import ConstraintLineLoading
from .base import GridElement

LOG = logging.getLogger(__name__)


class PPLine(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "line"

    @staticmethod
    def res_pp_key() -> str:
        return "res_load"

    def __init__(self, index, grid, value=100):
        super().__init__(index, grid, LOG)

        self.in_service = True
        self.max_percentage = value

        self._constraints.append(ConstraintLineLoading(self))

    def step(self, time):
        old_state = self.in_service
        self.in_service = True
        self._check(time)
        self.set_value("in_service", self.in_service)
        if not old_state and self.in_service:
            self.grid.run_powerflow()
            self._check(time)
            self.set_value("in_service", self.in_service)
            self.grid.run_powerflow()

        if old_state != self.in_service:
            if not self.in_service:
                LOG.debug(f"At step {time}: Line {self.index} out of service.")
                try:
                    self.grid.run_powerflow()
                except pp.LoadflowNotConverged:
                    LOG.debug("Line disabled. PF still not converging.")
            else:
                LOG.debug(
                    f"At step {time}: Line {self.index} back in service."
                )
                try:
                    self.grid.run_powerflow()
                except pp.LoadflowNotConverged:
                    LOG.debug("Line re-enabled. PF not converging.")

        return old_state != self.in_service
