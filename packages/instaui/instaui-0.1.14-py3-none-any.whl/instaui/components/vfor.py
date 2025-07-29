from __future__ import annotations
from typing import (
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
    Sequence,
    Generic,
    TypeVar,
    overload,
)
import pydantic

from instaui.components.component import Component
from instaui.vars.vfor_item import VForItem, VForDict, VForWithIndex
from instaui.runtime._app import get_app_slot, new_scope

from instaui.vars.mixin_types.element_binding import ElementBindingMixin

_T = TypeVar("_T")


class VFor(Component, Generic[_T]):
    def __init__(
        self,
        data: Union[Sequence[_T], ElementBindingMixin[List[_T]]],
        *,
        key: Union[Literal["item", "index"], str] = "index",
    ):
        """for loop component.

        Args:
            data (Union[Sequence[_T], ElementBindingMixin[List[_T]]]): data source.
            key (Union[Literal[&quot;item&quot;, &quot;index&quot;], str]]): key for each item. Defaults to 'index'.

        Examples:
        .. code-block:: python
            items = ui.state([1,2,3])

            with ui.vfor(items) as item:
                html.span(item)

            # object key
            items = ui.state([{"name": "Alice", "age": 20}, {"name": "Bob", "age": 30}])
            with ui.vfor(items, key=":item=>item.name") as item:
                html.span(item.name)
        """

        super().__init__("vfor")
        self._data = data
        self._key = key
        self._fid = get_app_slot().generate_vfor_id()
        self.__scope_manager = new_scope(append_to_app=False)
        self.__scope = None
        self._num = None
        self._transition_group_setting = None

    def __enter__(self) -> _T:
        self.__scope = self.__scope_manager.__enter__()
        super().__enter__()
        return VForItem(self).proxy  # type: ignore

    def __exit__(self, *_) -> None:
        self.__scope_manager.__exit__(*_)
        return super().__exit__(*_)

    def _set_num(self, num):
        self._num = num

    def transition_group(self, name="fade", tag: Optional[str] = None):
        self._transition_group_setting = {"name": name, "tag": tag}
        return self

    @property
    def current(self):
        return VForItem(self)

    def with_index(self):
        return VForWithIndex(self)

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["props"] = {"fid": self._fid}

        props: Dict = data["props"]
        if self._key is not None and self._key != "index":
            props["fkey"] = self._key

        if self._data is not None:
            if isinstance(self._data, ElementBindingMixin):
                props["bArray"] = self._data._to_element_binding_config()
            else:
                props["array"] = self._data

        if self._num is not None:
            props["num"] = self._num

        if self._transition_group_setting is not None:
            props["tsGroup"] = {
                k: v for k, v in self._transition_group_setting.items() if v is not None
            }

        props["scope"] = self.__scope

        if self._slot_manager.has_slot():
            props["items"] = self._slot_manager

        data.pop("slots", None)

        return data

    @overload
    @classmethod
    def range(cls, end: int) -> VFor[int]: ...

    @overload
    @classmethod
    def range(cls, end: ElementBindingMixin[int]) -> VFor[int]: ...

    @classmethod
    def range(cls, end: Union[int, ElementBindingMixin[int]]) -> VFor[int]:
        obj = cls(None)  # type: ignore

        num = (  # type: ignore
            end._to_element_binding_config()
            if isinstance(end, ElementBindingMixin)
            else end
        )

        obj._set_num(num)

        return obj  # type: ignore

    @classmethod
    def from_dict(
        cls, data: Union[Mapping, pydantic.BaseModel, ElementBindingMixin[Dict]]
    ):
        return VForDict(VFor(data))  # type: ignore
