
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, Component, StylesManager
from fasttk.style import Style

class Frame(Node):

    def __init__(
        self,
        *,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, ref=ref, type="frame", style=style)

    def add(self, *structs: Node | Component) -> "Frame":
        self.children.extend(structs)
        return self
    
    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "padding": "padding",
            "take_focus": "takefocus"
        })
        st_args = self.__style_map__({
            "background": "background",
            "border_color": "bordercolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "border_width": "borderwidth",
            "relief": "relief",
        })
        args["style"] = StylesManager().use_style("TFrame", st_args)
        self._widget_instance = ttk.Frame(master, **args)
        if self._normal_repr.container == "grid":
            for index, setting in self._normal_repr.row_config.items():
                self._widget_instance.rowconfigure(index, setting)
            for index, setting in self._normal_repr.column_config.items():
                self._widget_instance.columnconfigure(index, setting)

    @property
    def widget(self) -> ttk.Frame:
        return self._widget_instance

