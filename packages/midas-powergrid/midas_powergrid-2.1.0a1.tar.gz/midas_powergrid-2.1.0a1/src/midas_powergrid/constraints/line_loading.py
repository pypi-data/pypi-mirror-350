import numpy as np

from .base import Constraint


class ConstraintLineLoading(Constraint):
    def __init__(self, element):
        super().__init__(element)

    def check(self, time) -> bool:
        self._satisfied = True
        self.expected_value = self._element.max_percentage

        self.violated_value = self._element.grid.get_value(
            "res_line", self._element.index, "loading_percent"
        )
        if np.isnan(self.violated_value):
            # NaN occurs when LF fails or the line is not connected
            # It is assumed that there is no violation then
            self.violated_value = 0
        if self.violated_value > self.expected_value:
            self._satisfied = False

        return self._satisfied

    def handle_violation(self):
        self._element.in_service = False
