from __future__ import annotations
from typing import Dict, cast
from instaui.components.component import Component
from instaui.runtime._app import new_scope
from instaui.vars.mixin_types.element_binding import ElementBindingMixin
from instaui.vars.types import TMaybeRef


class VIf(Component):
    def __init__(self, on: TMaybeRef[bool]):
        super().__init__("vif")
        self._on = cast(ElementBindingMixin, on)
        self.__scope_manager = new_scope(append_to_app=False)
        self.__scope = None

    def __enter__(self):
        self.__scope = self.__scope_manager.__enter__()
        return super().__enter__()

    def __exit__(self, *_) -> None:
        self.__scope_manager.__exit__(*_)
        return super().__exit__(*_)

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["props"] = {
            "on": self._on._to_element_binding_config(),
        }
        props: Dict = data["props"]

        props["scope"] = self.__scope

        if self._slot_manager.has_slot():
            props["items"] = self._slot_manager

        data.pop("slots", None)

        return data
