
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, StylesManager
from fasttk.style import Style
from typing import Callable, Any

class Scale(Node):

    _variable: tk.DoubleVar
    _start_at: float
    _end_at: float
    _on_change: Callable
    _default: float
    _disabled: bool

    def __init__(
        self,
        *,
        start: float = 0.0,
        end: float = 1.0,
        tags: str = "",
        ref: str | None = None,
        default: float | None = None,
        disabled: bool = False,
        on_change: Callable[[float], Any] | None = None,
        style: Style | None = None
    ):
        super().__init__(
            tags=tags, type="scale", ref=ref, style=style,
            predef_style={
                "cursor": "hand2"
            }
        )
        self._start_at = start
        self._end_at = end
        self._on_change = on_change
        if not default: default = start
        self._default = default
        self._disabled = disabled

    def __change_hook__(self, value: str) -> None:
        self._on_change(float(value))

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
            "scale_length": "length"
        })
        st_args = self.__style_map__({
            "border_width": "borderwidth",
            "foreground": "background",
            "background": "troughcolor",
            "border_color": "bordercolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "scale_width": "arrowsize",
            "indicator_size": "sliderlength"
        })
        st_args[("normal", )]["gripcount"] = 0
        orient = self._normal_repr.bar_orientation
        args["style"] = StylesManager().use_style(
            "Vertical.TScale" if orient == "vertical" else "Horizontal.TScale",
            st_args
        )
        args["orient"] = orient
        args["from_"] = self._start_at
        args["to"] = self._end_at
        if self._on_change:
            args["command"] = self.__change_hook__
        self._widget_instance = ttk.Scale(master, **args)
        self._variable = tk.DoubleVar(self._widget_instance, self._default)
        self._widget_instance.configure(variable=self._variable)
        if self._disabled:
            self._widget_instance.state(["disabled"])
        del self._default

    @property
    def widget(self) -> ttk.Scrollbar:
        return self._widget_instance
    
    @property
    def value(self) -> float:
        return self._variable.get()
    
    @value.setter
    def value(self, value: float) -> None:
        self._variable.set(value)
        if self._on_change: self.__change_hook__(value)

    @property
    def disabled(self) -> bool:
        return self._disabled
    
    @disabled.setter
    def disabled(self, value: bool) -> None:
        if value != self._disabled:
            self._widget_instance.state(["disabled" if value else "!disabled"])
            self._disabled = value