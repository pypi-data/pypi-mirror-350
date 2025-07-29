import typing
from instaui.common.jsonable import Jsonable
from instaui.vars.mixin_types.observable import ObservableMixin
from .event_mixin import EventMixin


class VueEvent(Jsonable, EventMixin):
    """
    Create an event object that can be bound to a UI component's event listener.

    This function generates a callable event handler with optional contextual bindings.
    The event logic is defined via a code string, which can reference bound variables.

    Args:
        code (str): A string containing the executable logic for the event handler.
                    Typically contains a function body or expression that utilizes bound variables.
        bindings (typing.Optional[typing.Dict[str, typing.Any]], optional): A dictionary mapping variable names to values that should be available in the
            event handler's context. If None, no additional bindings are created.. Defaults to None.

    Example:
    .. code-block:: python
        a = ui.state(1)

        event = ui.vue_event(bindings={"a": a}, code=r'''()=> { a.value +=1}''')

        html.span(a)
        html.button("plus").on("click", event)
    """

    def __init__(
        self,
        *,
        code: str,
        bindings: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        self.code = code
        self._bindings = bindings

        if bindings:
            bindData = [
                int(not isinstance(v, ObservableMixin)) for v in bindings.values()
            ]

            if sum(bindData) > 0:
                self.bindData = bindData

            self.bind = {
                k: typing.cast(ObservableMixin, v)._to_observable_config()
                if isinstance(v, ObservableMixin)
                else v
                for k, v in bindings.items()
            }

    def copy_with_extends(self, extends: typing.Dict):
        raise NotImplementedError("VueEvent does not support extends")

    def event_type(self):
        return "vue"

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["type"] = self.event_type()
        return data


vue_event = VueEvent
