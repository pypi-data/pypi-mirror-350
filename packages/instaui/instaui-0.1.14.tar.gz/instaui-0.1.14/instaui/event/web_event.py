import inspect
import typing
from typing_extensions import ParamSpec
from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_current_scope, get_app_slot
from instaui.vars.mixin_types.py_binding import CanInputMixin, CanOutputMixin
from instaui.handlers import event_handler
from .event_mixin import EventMixin

_SYNC_TYPE = "sync"
_ASYNC_TYPE = "async"

P = ParamSpec("P")
R = typing.TypeVar("R")
_T_input = typing.TypeVar("_T_input")
_T_output = typing.TypeVar("_T_output")


class WebEvent(Jsonable, EventMixin, typing.Generic[P, R]):
    def __init__(
        self,
        fn: typing.Callable[P, R],
        inputs: typing.Sequence[CanInputMixin],
        outputs: typing.Sequence[CanOutputMixin],
    ):
        self._inputs = inputs
        self._outputs = outputs
        self._fn = fn

        scope = get_current_scope()
        self._sid = scope.id

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._fn(*args, **kwargs)

    def copy_with_extends(self, extends: typing.Sequence[CanInputMixin]):
        return WebEvent(
            fn=self._fn,
            inputs=list(self._inputs) + list(extends),
            outputs=self._outputs,
        )

    def event_type(self):
        return "web"

    def _to_json_dict(self):
        app = get_app_slot()

        hkey = event_handler.create_handler_key(
            page_path=app.page_path, handler=self._fn
        )

        event_handler.register_event_handler(
            hkey, self._fn, self._outputs, self._inputs
        )

        data = {}
        data["type"] = self.event_type()
        data["fType"] = (
            _ASYNC_TYPE if inspect.iscoroutinefunction(self._fn) else _SYNC_TYPE
        )
        data["hKey"] = hkey
        data["sid"] = self._sid

        if self._inputs:
            data["bind"] = [
                binding._to_input_config()
                if isinstance(binding, CanInputMixin)
                else binding
                for binding in self._inputs
            ]

        if self._outputs:
            data["set"] = [ref._to_output_config() for ref in self._outputs]

        return data


def event(
    *,
    inputs: typing.Optional[typing.Sequence] = None,
    outputs: typing.Optional[typing.Sequence] = None,
):
    """
    Creates an event handler decorator for binding reactive logic to component events.

    Args:
        inputs (typing.Optional[typing.Sequence], optional): Reactive sources (state objects, computed properties)
                                   that should be accessible during event handling.
                                   These values will be passed to the decorated function
                                   when the event fires.
        outputs (typing.Optional[typing.Sequence], optional): Targets (state variables, UI elements) that should
                                    update when this handler executes. Used for coordinating
                                    interface updates after the event is processed.

    # Example:
    .. code-block:: python
        from instaui import ui, html

        a = ui.state(0)

        @ui.event(inputs=[a], outputs=[a])
        def plus_one(a):
            return a + 1

        html.button("click me").on_click(plus_one)
        html.paragraph(a)

    """

    def wrapper(func: typing.Callable[P, R]):
        return WebEvent(
            func,
            inputs or [],
            outputs=outputs or [],
        )

    return wrapper
