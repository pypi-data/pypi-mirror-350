from __future__ import annotations

import typing
from instaui.components.component import Component
from instaui.runtime._app import new_scope

from instaui.vars.mixin_types.element_binding import ElementBindingMixin


class Match(Component):
    def __init__(self, on: ElementBindingMixin):
        super().__init__("match")
        self._on = on
        self._default_case = None

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["props"] = {
            "on": self._on._to_element_binding_config(),
        }
        props: typing.Dict = data["props"]

        props["case"] = [
            item
            for item in self._slot_manager.default._children
            if isinstance(item, Case)
        ]

        if self._default_case:
            props["default"] = self._default_case

        data.pop("slots", None)

        return data

    def case(self, value: typing.Any) -> Case:
        with self:
            case = Case(value)

        return case

    def default(self) -> DefaultCase:
        with self:
            self._default_case = DefaultCase()

        return self._default_case


class Case(Component):
    def __init__(self, value: typing.Any):
        super().__init__("case")
        self._value = value
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
            "value": self._value,
        }
        props = data["props"]

        props["scope"] = self.__scope

        if self._slot_manager.has_slot():
            props["items"] = self._slot_manager

        data.pop("slots", None)
        return data


class DefaultCase(Component):
    def __init__(self):
        super().__init__("default-case")

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
        data["props"] = {}
        props = data["props"]

        props["scope"] = self.__scope

        if self._slot_manager.has_slot():
            props["items"] = self._slot_manager

        data.pop("slots", None)
        return data
