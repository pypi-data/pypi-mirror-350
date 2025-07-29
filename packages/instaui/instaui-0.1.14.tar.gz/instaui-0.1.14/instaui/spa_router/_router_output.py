from typing import List, Optional
from instaui.common.jsonable import Jsonable
from instaui.vars.mixin_types.py_binding import CanOutputMixin
from pydantic import BaseModel


class RouterOutput(Jsonable, CanOutputMixin):
    def __init__(self):
        self.type = "routeAct"

    def _to_output_config(self):
        return self._to_json_dict()

    def _to_json_dict(self):
        data = super()._to_json_dict()

        return data


class RouterMethod(BaseModel):
    fn: str
    args: Optional[List]
