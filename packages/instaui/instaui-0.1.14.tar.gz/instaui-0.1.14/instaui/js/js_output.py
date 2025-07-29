from instaui.common.jsonable import Jsonable
from instaui.vars.mixin_types.py_binding import CanOutputMixin


class JsOutput(Jsonable, CanOutputMixin):
    def __init__(self):
        self.type = "jsOutput"

    def _to_output_config(self):
        return self._to_json_dict()

    def _to_json_dict(self):
        data = super()._to_json_dict()

        return data
