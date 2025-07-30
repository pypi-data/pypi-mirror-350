
import tkinter as tk
from fasttk.base import Node
from fasttk.style import Style

class Canvas(Node):

    _widget_instance: tk.Canvas

    def __init__(
        self,
        *,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, type="canvas", ref=ref, style=style)

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
            "background": "background",
            "relief": "relief",
            "border_width": "borderwidth"
        })
        self._widget_instance = tk.Canvas(master, **args)

    @property
    def widget(self) -> tk.Canvas:
        return self._widget_instance
