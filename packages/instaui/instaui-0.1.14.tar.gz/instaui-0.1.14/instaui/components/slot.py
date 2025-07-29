from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Set
from instaui.common.jsonable import Jsonable
from instaui.runtime import get_slot_stacks, pop_slot
from instaui.runtime._app import get_app_slot
from instaui.vars.slot_prop import BindingSlotPropItem

if TYPE_CHECKING:
    from instaui.components.component import Component

_DEFAULT_SLOT_NAME = ":"


class SlotManager(Jsonable):
    def __init__(self) -> None:
        super().__init__()
        self._slots: Dict[str, Slot] = {}

    def get_slot(self, name: str) -> Slot:
        name = _DEFAULT_SLOT_NAME if name == "default" else name

        if name not in self._slots:
            self._slots[name] = Slot(name)

        return self._slots[name]

    @property
    def default(self):
        return self.get_slot(_DEFAULT_SLOT_NAME)

    def _to_json_dict(self):
        if (
            len(self._slots) == 1
            and _DEFAULT_SLOT_NAME in self._slots
            and (not self._slots[_DEFAULT_SLOT_NAME]._has_props_use())
        ):
            return self._slots[_DEFAULT_SLOT_NAME]._children

        return {name: slot._to_json_dict() for name, slot in self._slots.items()}

    def has_slot(self) -> bool:
        return len(self._slots) > 0


class Slot(Jsonable):
    def __init__(self, name: str) -> None:
        super().__init__()

        self._id: Optional[str] = None
        self._name = name
        self._children: List[Component] = []
        self._props_use_name: Set[str] = set()

    def _has_props_use(self):
        return len(self._props_use_name) > 0

    def props(self, name: str):
        if self._id is None:
            self._id = get_app_slot().generate_slot_id()

        self._props_use_name.add(name)
        return BindingSlotPropItem(self._id, name)

    def __enter__(self):
        get_slot_stacks().append(self)
        return self

    def __exit__(self, *_):
        pop_slot()

    def _to_json_dict(self):
        data = super()._to_json_dict()

        if self._children:
            data["items"] = self._children

        if self._props_use_name:
            data["props"] = {"id": self._id, "use": list(self._props_use_name)}

        return data
