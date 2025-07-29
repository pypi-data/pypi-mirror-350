import typing
from typing_extensions import Unpack
import pydantic
from instaui.components.element import Element
from instaui.vars.types import TMaybeRef
from instaui.vars.state import StateModel
from instaui.arco import component_types
from instaui.event.event_mixin import EventMixin
from ._utils import handle_props, try_setup_vmodel


class Radio(Element):
    def __init__(
        self,
        value: typing.Optional[TMaybeRef[typing.Union[str, int, bool, float]]] = None,
        **kwargs: Unpack[component_types.TRadio],
    ):
        super().__init__("a-radio")

        self.props({"value": value})
        self.props(handle_props(kwargs))  # type: ignore

    def on_change(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "change",
            handler,
            extends=extends,
        )
        return self


class RadioOption(StateModel):
    label: str
    value: typing.Union[str, int]
    disabled: bool = pydantic.Field(default=False)
