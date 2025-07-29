from abc import ABC, abstractmethod


class CanInputMixin(ABC):
    @abstractmethod
    def _to_input_config(self):
        pass


class CanOutputMixin(ABC):
    @abstractmethod
    def _to_output_config(self):
        pass
