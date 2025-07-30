
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, StylesManager
from fasttk.style import Style

class Scrollbar(Node):

    _v_style: str
    _h_style: str

    _widget_instance: ttk.Scrollbar

    def __init__(
        self,
        *,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, type="scrollbar", ref=ref, style=style)

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus"
        })
        st_args = self.__style_map__({
            "foreground": "background",
            "background": "troughcolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "border_color": "bordercolor",
            "indicator_size": "arrowsize",
            "indicator_foreground": "arrowcolor"
        })
        st_args[("normal", )]["gripcount"] = 0
        orient = self._normal_repr.bar_orientation
        s = StylesManager()
        self._v_style = s.use_style("Vertical.TScrollbar", st_args)
        self._h_style = s.use_style("Horizontal.TScrollbar", st_args)
        args["style"] = self._v_style if orient == "vertical" else self._h_style
        args["orient"] = orient
        self._widget_instance = ttk.Scrollbar(master, **args)

    def _set_horizontal(self) -> None:
        self._widget_instance.configure(orient="horizontal", style=self._h_style)

    def _set_vertical(self) -> None:
        self._widget_instance.configure(orient="vertical", style=self._v_style)

    @property
    def widget(self) -> ttk.Scrollbar:
        return self._widget_instance
