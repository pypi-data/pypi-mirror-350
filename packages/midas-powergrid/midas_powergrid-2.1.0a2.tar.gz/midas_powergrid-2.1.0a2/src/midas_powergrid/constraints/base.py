from abc import ABC, abstractmethod
from typing import Optional

from ..elements.base import GridElement


class Constraint(ABC):
    def __init__(self, element: GridElement):
        self._element: GridElement = element
        self.expected_value: Optional[float] = None
        self.violated_value: Optional[float] = None

        self._satisfied: bool = True

    def set_violation_values(self, expected_value, violated_value):
        self.violated_value = violated_value
        self.expected_value = expected_value

    @abstractmethod
    def check(self, time) -> bool:
        pass

    @abstractmethod
    def handle_violation(self):
        pass
