from typing import Dict, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


class ElementBindingMixin(ABC, Generic[T]):
    @abstractmethod
    def _to_element_binding_config(self) -> Dict:
        pass
