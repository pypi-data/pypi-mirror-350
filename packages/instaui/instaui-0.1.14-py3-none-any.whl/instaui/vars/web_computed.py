from __future__ import annotations
import inspect
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Optional,
    Sequence,
    TypeVar,
)
from typing_extensions import ParamSpec

from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_app_slot, get_current_scope
from instaui.handlers import watch_handler

from instaui.vars.path_var import PathVar
from instaui.vars.mixin_types.py_binding import CanInputMixin, CanOutputMixin
from instaui.vars.mixin_types.element_binding import ElementBindingMixin
from instaui.vars.mixin_types.pathable import CanPathPropMixin
from instaui.vars.mixin_types.str_format_binding import StrFormatBindingMixin
from instaui.vars.mixin_types.observable import ObservableMixin
from instaui.vars.mixin_types.common_type import TObservableInput
from instaui._helper import observable_helper

_SYNC_TYPE = "sync"
_ASYNC_TYPE = "async"

P = ParamSpec("P")
R = TypeVar("R")


class WebComputed(
    Jsonable,
    PathVar,
    CanInputMixin,
    ObservableMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin[R],
    Generic[P, R],
):
    BIND_TYPE = "var"

    def __init__(
        self,
        func: Callable[P, R],
        inputs: Optional[Sequence[TObservableInput]] = None,
        extend_outputs: Optional[Sequence[CanOutputMixin]] = None,
        init_value: Optional[R] = None,
        evaluating: Optional[CanOutputMixin] = None,
        deep_compare_on_input: bool = False,
        debug_info: Optional[Dict] = None,
    ) -> None:
        scope = get_current_scope()

        self._sid = scope.id
        self._id = scope.generate_vars_id()
        get_current_scope().register_web_computed(self)

        self._inputs, self._is_slient_inputs, self._is_data = (
            observable_helper.analyze_observable_inputs(list(inputs or []))
        )
        self._outputs = [output._to_output_config() for output in extend_outputs or []]
        self._fn = func
        self._init_value = init_value
        self._evaluating = evaluating
        self._deep_compare_on_input = deep_compare_on_input

        if debug_info is not None:
            self.debug = debug_info

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._fn(*args, **kwargs)

    def _to_json_dict(self):
        data = super()._to_json_dict()

        app = get_app_slot()

        hkey = watch_handler.create_handler_key(
            page_path=app.page_path,
            handler=self._fn,
        )

        watch_handler.register_handler(hkey, self._fn, len(self._outputs) + 1)

        # if app.mode == "web":

        data["id"] = self._id
        data["sid"] = self._sid

        if self._inputs:
            data["inputs"] = self._inputs

        if self._outputs:
            data["outputs"] = self._outputs

        if sum(self._is_slient_inputs) > 0:
            data["slient"] = self._is_slient_inputs

        if sum(self._is_data) > 0:
            data["data"] = self._is_data

        data["fType"] = (
            _ASYNC_TYPE if inspect.iscoroutinefunction(self._fn) else _SYNC_TYPE
        )
        data["key"] = hkey
        if self._init_value is not None:
            data["init"] = self._init_value

        if self._evaluating:
            data["running"] = self._evaluating._to_output_config()

        if self._deep_compare_on_input is not False:
            data["deepEqOnInput"] = 1

        return data

        # return {}

    def __to_binding_config(self):
        return {
            "type": self.BIND_TYPE,
            "id": self._id,
            "sid": self._sid,
        }

    def _to_pathable_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_path_prop_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_input_config(self):
        return self.__to_binding_config()

    def _to_element_binding_config(self):
        return self.__to_binding_config()

    def _to_observable_config(self):
        return self.__to_binding_config()


def web_computed(
    *,
    inputs: Optional[Sequence] = None,
    extend_outputs: Optional[Sequence] = None,
    init_value: Optional[Any] = None,
    evaluating: Optional[Any] = None,
    deep_compare_on_input: bool = False,
    debug_info: Optional[Dict] = None,
):
    """
    Creates a computed property decorator for reactive programming with dependency tracking.

    This decorator factory wraps functions to create reactive computed properties that:
    - Automatically re-evaluate when dependencies (inputs) change
    - Cache results for performance optimization
    - Support both synchronous and asynchronous computation patterns

    Args:
        inputs (Optional[Sequence], optional): Collection of reactive sources that trigger recomputation
                                   when changed. These can be state objects or other computed properties.
        extend_outputs (Optional[Sequence], optional):  Additional outputs to notify when this computed value updates.
        init_value (Optional[Any], optional): Initial value to return before first successful evaluation.
        evaluating (Optional[Any], optional): Temporary value returned during asynchronous computation.

    # Example:
    .. code-block:: python
        from instaui import ui,html

        a = ui.state(0)

        @ui.computed(inputs=[a])
        def plus_one(a):
            return a + 1

        html.number(a)
        ui.label(plus_one)
    """

    def wrapper(func: Callable[P, R]):
        return WebComputed(
            func,
            inputs=inputs,
            extend_outputs=extend_outputs,
            init_value=init_value,
            evaluating=evaluating,
            deep_compare_on_input=deep_compare_on_input,
            debug_info=debug_info,
        )

    return wrapper


TComputed = WebComputed
