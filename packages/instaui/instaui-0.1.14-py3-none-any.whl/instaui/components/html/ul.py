from __future__ import annotations
from typing import List, Union
from instaui.components.element import Element
from .li import Li
from instaui.components.vfor import VFor

from instaui.vars.mixin_types.element_binding import ElementBindingMixin


class Ul(Element):
    def __init__(self):
        super().__init__("ul")

    @classmethod
    def from_list(cls, data: Union[List, ElementBindingMixin[List]]) -> Ul:
        with Ul() as ul:
            with VFor(data) as items:
                Li(items)

        return ul
