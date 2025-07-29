from __future__ import annotations
from typing import Literal, TypeVar


_T_Value = TypeVar("_T_Value")
_T_Output_Value = TypeVar("_T_Output_Value", covariant=True)
_T_VAR_TYPE = Literal["ref", "computed", "webComputed"]
_T_Bindable_Type = Literal["ref", "computed", "js", "webComputed", "vforItem"]
