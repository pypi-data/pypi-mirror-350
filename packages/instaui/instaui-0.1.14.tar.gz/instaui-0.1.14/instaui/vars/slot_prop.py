from __future__ import annotations
from typing import (
    Dict,
)
from instaui.common.jsonable import Jsonable

from instaui.vars.path_var import PathVar

from .mixin_types.py_binding import CanInputMixin
from .mixin_types.element_binding import ElementBindingMixin
from .mixin_types.pathable import CanPathPropMixin


class BindingSlotPropItem(
    Jsonable,
    PathVar,
    ElementBindingMixin,
    CanInputMixin,
    CanPathPropMixin,
):
    def __init__(self, slot_id: str, name: str) -> None:
        super().__init__()
        self.name = name
        self._id = slot_id

    def _to_element_binding_config(self):
        return self._to_binding_config()

    def _to_input_config(self):
        return self._to_binding_config()

    def _to_path_prop_binding_config(self) -> Dict:
        return self._to_binding_config()

    def _to_pathable_binding_config(self) -> Dict:
        return self._to_binding_config()

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["type"] = "sp"
        data["id"] = self._id

        return data

    def _to_binding_config(self) -> Dict:
        return self._to_json_dict()
