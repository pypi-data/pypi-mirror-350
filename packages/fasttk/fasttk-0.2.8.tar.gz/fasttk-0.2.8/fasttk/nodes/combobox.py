
import tkinter as tk
from tkinter import ttk
from fasttk.tools import FontDescriptor
from fasttk.base import Node, StylesManager, Component
from fasttk.style import Style
from typing import Callable, Any
from .scrollbar import Scrollbar

class Combobox(Node):

    _text_variable: tk.StringVar
    _values: list[str]
    _readonly: bool
    _disabled: bool
    _text_buffer: str
    _on_change: Callable
    _on_select: Callable
    _bind_index: int
    _values_map: dict[str, int]
    _bind_sb: str

    def __init__(
        self,
        *,
        default: str = "",
        values: list[str] = [],
        on_change: Callable[[str], Any] | None = None,
        on_select: Callable[[str], Any] | None = None,
        readonly: bool = False,
        disabled: bool = False,
        scrollbar: str | None = None,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, ref=ref, type="combobox", style=style)
        self._values = values.copy()
        self._readonly = readonly
        self._disabled = disabled
        self._text_buffer = default
        self._on_change = on_change
        self._on_select = on_select
        self._bind_index = -1
        self._bind_sb = scrollbar
        self._values_map = {value: index for index, value in enumerate(values)}
    
    def __select_hook__(self, e: tk.Event):
        if self._on_select:
            self._on_select(self._text_variable.get())

    def __change_hook__(self, x, y, z):
        text = self._text_variable.get()
        self._bind_index = self._values_map.get(text, -1)
        if self._on_change:
            self._on_change(text)

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
            "combobox_height": "height",
            "entry_width": "width",
            "label_justify": "justify",
            "use_font": "font"
        })
        st_args = self.__style_map__({
            "background": "fieldbackground",
            "foreground": "foreground",
            "indicator_background": "background",
            "indicator_foreground": "arrowcolor",
            "indicator_size": "arrowsize",
            "padding": "padding",
            "border_color": "bordercolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "select_foreground": "selectforeground",
            "select_background": "selectbackground",
            "insert_width": "insertwidth",
            "insert_color": "insertcolor"
        })
        combo_args = self._normal_repr.props_map({
            "use_font": "font",
            "foreground": "foreground",
            "background": "background",
            "select_foreground": "selectforeground",
            "select_background": "selectbackground"
        })
        args["values"] = self._values
        args["style"] = StylesManager().use_style("TCombobox", st_args)
        self._widget_instance = ttk.Combobox(master, **args)
        self._text_variable = tk.StringVar(
            self._widget_instance, self._text_buffer
        )
        self._widget_instance.configure(textvariable=self._text_variable)
        self._widget_instance.bind("<<ComboboxSelected>>", self.__select_hook__)
        self._text_variable.trace_add("write", self.__change_hook__)
        if self._disabled:
            self._widget_instance.state(["disabled"])
        if self._readonly:
            self._widget_instance.state(["readonly"])
        popdown = self._widget_instance.tk.call(
            "ttk::combobox::PopdownWindow", self._widget_instance._w
        ) + ".f.l"
        if font := combo_args.get("font", None):
            combo_args["font"] = FontDescriptor(font)
        for option, value in combo_args.items():
            self._widget_instance.tk.call(
                popdown, "configure", f"-{option}", value
            )
        del self._text_buffer

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
    def widget(self) -> ttk.Combobox:
        return self._widget_instance

    @property
    def current_value(self) -> str:
        return self._text_variable.get()
    
    @current_value.setter
    def current_value(self, value: str) -> None:
        self._text_variable.set(value)
        self._bind_index = self._values_map.get(value, -1)

    @property
    def current_index(self) -> int:
        return self._bind_index

    @current_index.setter
    def current_index(self, index: int) -> None:
        if index >= len(self._values) or index < 0:
            return None
        self._bind_index = index
        self._text_variable.set(self._values[index])

    @property
    def values(self) -> list[str]:
        return self._values

    @values.setter
    def values(self, values: list[str]) -> None:
        self._values = values.copy()
        self._widget_instance.configure(values=self._values)
        self._values_map = {value: index for index, value in enumerate(self._values)}
        self._bind_index = self._values_map.get(self._text_variable.get(), -1)

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

