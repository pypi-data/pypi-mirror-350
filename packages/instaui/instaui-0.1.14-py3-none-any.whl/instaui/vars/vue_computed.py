from __future__ import annotations
from typing import Any, Dict, Mapping, Optional, Union

from instaui.common.jsonable import Jsonable

from instaui.runtime._app import get_current_scope
from instaui.vars.path_var import PathVar
from instaui.vars.mixin_types.var_type import VarMixin
from instaui.vars.mixin_types.element_binding import ElementBindingMixin
from instaui.vars.mixin_types.py_binding import CanInputMixin
from instaui.vars.mixin_types.pathable import CanPathPropMixin
from instaui.vars.mixin_types.str_format_binding import StrFormatBindingMixin
from instaui.vars.mixin_types.observable import ObservableMixin


class VueComputed(
    Jsonable,
    PathVar,
    VarMixin,
    CanInputMixin,
    ObservableMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin,
):
    BIND_TYPE = "var"

    def __init__(
        self,
        fn_code: str,
        bindings: Optional[Mapping[str, Union[ElementBindingMixin, Any]]] = None,
    ) -> None:
        self.code = fn_code
        scope = get_current_scope()
        scope.register_vue_computed(self)

        self._sid = scope.id
        self._id = scope.generate_vars_id()

        if bindings:
            const_bind = []
            self.bind = {}

            for k, v in bindings.items():
                is_binding = isinstance(v, ElementBindingMixin)
                self.bind[k] = v._to_element_binding_config() if is_binding else v
                const_bind.append(int(not is_binding))

            if any(i == 1 for i in const_bind):
                self.const = const_bind

    def __to_binding_config(self):
        return {
            "type": self.BIND_TYPE,
            "id": self._id,
            "sid": self._sid,
        }

    def _to_input_config(self):
        return self.__to_binding_config()

    def _to_path_prop_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_element_binding_config(self):
        return self.__to_binding_config()

    def _to_pathable_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_observable_config(self):
        return self.__to_binding_config()

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["sid"] = self._sid
        data["id"] = self._id
        return data


TVueComputed = VueComputed
