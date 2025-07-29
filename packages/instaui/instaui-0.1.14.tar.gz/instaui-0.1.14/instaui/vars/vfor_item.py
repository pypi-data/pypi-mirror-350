from __future__ import annotations
from typing import Dict, Generic, Tuple, TypeVar, TYPE_CHECKING, Union, cast
from contextlib import contextmanager

from instaui.common.jsonable import Jsonable
from instaui.vars.mixin_types.element_binding import ElementBindingMixin
from instaui.vars.mixin_types.py_binding import CanInputMixin, CanOutputMixin
from instaui.vars.mixin_types.pathable import CanPathPropMixin
from instaui.vars.mixin_types.str_format_binding import StrFormatBindingMixin
from instaui.vars.mixin_types.observable import ObservableMixin
from instaui.vars.path_var import PathVar

if TYPE_CHECKING:
    from instaui.components.vfor import VFor

_T = TypeVar("_T")


class VForItemProxy(
    PathVar,
    CanInputMixin,
    ObservableMixin,
    CanOutputMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin,
    Jsonable,
    Generic[_T],
):
    def __init__(self, vfor_item: VForItem[_T]):
        self._vfor_item = vfor_item

    def __getattr__(self, name: str):
        return self._vfor_item[name]

    def __getitem__(self, name):
        return super().__getattribute__("_vfor_item")[name]

    def _to_element_binding_config(self) -> Dict:
        return super().__getattribute__("_vfor_item")._to_element_binding_config()

    def _to_input_config(self):
        return super().__getattribute__("_vfor_item")._to_input_config()

    def _to_path_prop_binding_config(self) -> Dict:
        return super().__getattribute__("_vfor_item")._to_path_prop_binding_config()

    def _to_output_config(self):
        return super().__getattribute__("_vfor_item")._to_output_config()

    def _to_str_format_binding(self, order: int) -> Tuple[str, str]:
        return super().__getattribute__("_vfor_item")._to_str_format_binding(order)

    def _to_pathable_binding_config(self) -> Dict:
        return super().__getattribute__("_vfor_item")._to_pathable_binding_config()

    def _to_observable_config(self):
        return super().__getattribute__("_vfor_item")._to_observable_config()

    def _to_json_dict(self):
        return super().__getattribute__("_vfor_item")._to_json_dict()


class VForItem(
    PathVar,
    CanInputMixin,
    ObservableMixin,
    CanOutputMixin,
    CanPathPropMixin,
    ElementBindingMixin[_T],
    StrFormatBindingMixin,
    Generic[_T],
):
    VAR_Type = "vf"

    def __init__(self, vfor: VFor):
        super().__init__()
        self._vfor = vfor

    @property
    def dict_key(self):
        return self._vfor.current[1]

    @property
    def dict_value(self):
        return self._vfor.current[0]

    @property
    def proxy(self):
        return cast(_T, VForItemProxy(self))

    def _to_binding_config(self) -> Union[Jsonable, Dict]:
        return self._to_json_dict()

    def _to_element_binding_config(self):
        return self._to_json_dict()

    def _to_input_config(self):
        return self._to_json_dict()

    def _to_output_config(self):
        return self._to_json_dict()

    def _to_path_prop_binding_config(self) -> Dict:
        return self._to_json_dict()

    def _to_pathable_binding_config(self) -> Dict:
        return self._to_json_dict()

    def _to_observable_config(self):
        return self._to_json_dict()

    def _to_json_dict(self):
        data: Dict = {
            "type": self.VAR_Type,
            "fid": self._vfor._fid,
        }

        return data


class VForIndex(
    CanInputMixin,
    CanPathPropMixin,
    ElementBindingMixin,
    StrFormatBindingMixin,
):
    def __init__(self, vfor: VFor):
        super().__init__()
        self._vfor = vfor

    def _to_element_binding_config(self):
        return self._to_json_dict()

    def _to_input_config(self):
        return self._to_json_dict()

    def _to_path_prop_binding_config(self) -> Dict:
        return self._to_json_dict()

    def _to_json_dict(self):
        return {
            "type": "vf-i",
            "fid": self._vfor._fid,
        }


class VForDict(
    CanInputMixin,
    CanOutputMixin,
    StrFormatBindingMixin,
    ElementBindingMixin,
    Jsonable,
):
    def __init__(self, vfor: VFor):
        self._vfor = vfor

    @property
    def dict_key(self):
        return self._vfor.current[1]

    @property
    def dict_value(self):
        return self._vfor.current[0]

    @contextmanager
    def with_index(self):
        self.__enter__()
        yield self, cast(int, VForIndex(self._vfor))

    def __enter__(self):
        self._vfor.__enter__()
        return self

    def __exit__(self, *_) -> None:
        return self._vfor.__exit__(*_)

    def _to_element_binding_config(self) -> Dict:
        return self.dict_value._to_element_binding_config()

    def _to_input_config(self):
        return self.dict_value._to_input_config()

    def _to_output_config(self):
        return self.dict_value._to_output_config()

    def _to_json_dict(self):
        return self.dict_value._to_json_dict()


class VForWithIndex(Generic[_T]):
    def __init__(self, vfor: VFor[_T]):
        self._vfor = vfor

    def __enter__(self):
        self._vfor.__enter__()
        return cast(_T, self._vfor.current.proxy), cast(int, VForIndex(self._vfor))

    def __exit__(self, *_) -> None:
        return self._vfor.__exit__(*_)


TVForItem = VForItem
TVForIndex = VForIndex
