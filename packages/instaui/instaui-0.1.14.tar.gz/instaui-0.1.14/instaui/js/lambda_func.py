from typing import Dict
from instaui.common.jsonable import Jsonable
from instaui.vars.mixin_types.element_binding import ElementBindingMixin


class LambdaFunc(Jsonable, ElementBindingMixin):
    def __init__(
        self, code: str, *, bindings: Dict[str, ElementBindingMixin], computed=False
    ):
        self.code = code
        self.type = "js"
        self._bindings = bindings
        self._computed = computed

    def _to_binding_config(self) -> Dict:
        return self._to_json_dict()

    def _to_js_binding_config(self):
        return self._to_json_dict()

    def _to_element_binding_config(self):
        return self._to_json_dict()

    def _to_json_dict(self):
        data = super()._to_json_dict()

        if self._bindings:
            data["bind"] = {
                k: v._to_element_binding_config() for k, v in self._bindings.items()
            }

        if self._computed is True:
            data["ext"] = ["cpt"]

        return data
