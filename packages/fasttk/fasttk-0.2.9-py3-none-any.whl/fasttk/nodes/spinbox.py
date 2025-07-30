
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, StylesManager, Component
from fasttk.style import Style
from typing import Callable, Any, Literal
from .scrollbar import Scrollbar

class Spinbox(Node):

    _variable: tk.StringVar
    _start_at: float
    _end_at: float
    _increment: float
    _values: list[str]
    _bind_index: int
    _on_change: Callable
    _on_spin: Callable
    _default: str
    _disabled: bool
    _readonly: bool
    _bind_sb: str | None

    _index_map: dict[str, int]
    _last_event: int

    _widget_instance: ttk.Spinbox

    def __init__(
        self,
        *,
        default: float | str | None = None,
        start: float = 0.0,
        end: float = 100.0,
        increment: float = 1.0,
        values: list[str] | None = None,
        tags: str = "",
        ref: str | None = None,
        readonly: bool = False,
        disabled: bool = False,
        scrollbar: str | None = None,
        on_change: Callable[[str | float], Any] | None = None,
        on_spin: Callable[[Literal["increase", "decrease"], str | float], Any] | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, type="spinbox", ref=ref, style=style)
        self._start_at = start
        self._end_at = end
        self._increment = increment

        self._values = values
        self._on_change = on_change
        self._on_spin = on_spin
        
        if default is None:
            default = self._values[0] if self._values else self._start_at
        self._default = default

        self._bind_index = -1
        if self._values:
            self._index_map = {
                value: index for index, value in enumerate(self._values)
            }
            self._bind_index = self._index_map.get(self._default, -1)
        
        self._readonly = readonly
        self._disabled = disabled
        self._bind_sb = scrollbar
        self._last_event = 0

    def __change_hook__(self, x, y, z) -> None:
        value = self._variable.get()
        if not self._values:
            value = float(value)
        else:
            self._bind_index = self._index_map.get(value, -1)
        if self._last_event > 0:
            self._on_spin("increase", value)
        elif self._last_event < 0:
            self._on_spin("decrease", value)
        if self._on_change:
            self._on_change(value)
        self._last_event = 0
    
    def __inc_hook__(self, ev: tk.Event) -> None:
        self._last_event = 1

    def __dec_hook__(self, ev: tk.Event) -> None:
        self._last_event = -1

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "use_font": "font",
            "spinbox_wrap": "wrap",
            "take_focus": "takefocus",
        })
        st_args = self.__style_map__({
            "foreground": "foreground",
            "background": "fieldbackground",
            "padding": "padding",
            "border_color": "bordercolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "indicator_size": "arrowsize",
            "select_foreground": "selectforeground",
            "select_background": "selectbackground",
            "insert_color": "insertcolor",
            "insert_width": "insertwidth",
            "indicator_foreground": "arrowcolor",
            "indicator_background": "background"
        })
        args["style"] = StylesManager().use_style("TSpinbox", st_args)
        if self._values:
            args["values"] = self._values
        else:
            args["from_"] = self._start_at
            args["to"] = self._end_at
            args["increment"] = self._increment
        self._widget_instance = ttk.Spinbox(master, **args)
        if self._on_spin:
            self._widget_instance.bind("<<Increment>>", self.__inc_hook__)
            self._widget_instance.bind("<<Decrement>>", self.__dec_hook__)
        self._variable = tk.StringVar(self._widget_instance, self._default)
        if self._on_change or self._on_spin:
            self._variable.trace_add("write", self.__change_hook__)
        self._widget_instance.configure(textvariable=self._variable)
        if self._disabled:
            self._widget_instance.state(["disabled"])
        if self._readonly:
            self._widget_instance.state(["readonly"])
        del self._default

    def __bind__(self, component: Component):
        if not self._bind_sb:
            return None
        sb: Scrollbar | None = getattr(component, self._bind_sb, None)
        if not sb:
            return None
        sb._widget_instance.configure(command=self._widget_instance.xview)
        sb._set_horizontal()
        self.widget.configure(xscrollcommand=sb._widget_instance.set)

    @property
    def widget(self) -> ttk.Spinbox:
        return self._widget_instance
    
    @property
    def current_value(self) -> float | str:
        value = self._variable.get()
        return value if self.values else float(value)
    
    @current_value.setter
    def current_value(self, value: float | str) -> None:
        if self._values:
            self._variable.set(value)
            self._bind_index = self._index_map.get(value, -1)
        else:
            self._variable.set(str(value))
        if self._on_change: self.__change_hook__(value)

    @property
    def current_index(self) -> int:
        return self._bind_index
    
    @current_index.setter
    def current_index(self, index: int) -> None:
        if self._values:
            if index >= len(self._values) or index < 0:
                return None
            self._variable.set(self._values[index])
            self._bind_index = index

    @property
    def values(self) -> list[str] | None:
        if self.values:
            return None
        return self._values
    
    @values.setter
    def values(self, replace: list[str]) -> None:
        if self._values:
            self._values = replace.copy()
            self._widget_instance.configure(values=self._values)
            self._index_map = {value: index for index, value in enumerate(self._values)}
            self._bind_index = self._index_map.get(self._variable.get(), -1)

    @property
    def disabled(self) -> bool:
        return self._disabled
    
    @disabled.setter
    def disabled(self, value: bool) -> None:
        if value != self._disabled:
            self._widget_instance.state(["disabled" if value else "!disabled"])
            self._disabled = value
    
    @property
    def readonly(self) -> bool:
        return self._readonly
    
    @readonly.setter
    def readonly(self, value: bool) -> None:
        if value != self._readonly:
            self._widget_instance.state(["readonly" if value else "!readonly"])
            self._readonly = value