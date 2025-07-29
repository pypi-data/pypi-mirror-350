from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseDut(ABC):
    def __init__(self, **state):
        self.state: Dict[str, Any] = state

    def apply_voltage(self, v: float) -> None:
        self.state["v"] = v

    @abstractmethod
    def measure_current(self) -> float:
        ...
