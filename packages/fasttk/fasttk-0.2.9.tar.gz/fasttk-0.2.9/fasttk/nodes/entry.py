
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, StylesManager, Component
from fasttk.style import Style
from typing import Callable
from .scrollbar import Scrollbar

class Entry(Node):
    
    _text_variable: tk.StringVar
    _disabled: bool
    _readonly: bool
    _text_buffer: str
    _on_change: Callable | None
    _bind_sb: str | None

    def __init__(
        self,
        *,
        text: str = "",
        tags: str = "",
        ref: str | None = None,
        scrollbar: str | None = None,
        readonly: bool = False,
        disabled: bool = False,
        on_change: Callable[[str], None] | None = None,
        style: Style | None = None
    ):
        super().__init__(
            tags=tags, type="entry", ref=ref, style=style,
            predef_style={
                "cursor": "xterm"
            }
        )
        self._text_buffer = text
        self._readonly = readonly
        self._disabled = disabled
        self._on_change = on_change
        self._bind_sb = scrollbar

    def __change_hook__(self, *neglect) -> None:
        if self._on_change:
            self._on_change(self._text_variable.get())

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "use_font": "font",
            "cursor": "cursor",
            "take_focus": "takefocus",
            "label_justify": "justify",
            "entry_show": "show",
            "entry_width": "width"
        })
        st_args = self.__style_map__({
            "foreground": "foreground",
            "background": "fieldbackground",
            "padding": "padding",
            "relief": "relief",
            "insert_width": "insertwidth",
            "insert_color": "insertcolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "border_color": "bordercolor",
            "border_width": "borderwidth",
            "select_foreground": "selectforeground",
            "select_background": "selectbackground"
        })
        args["style"] = StylesManager().use_style("TEntry", st_args)
        self._widget_instance = ttk.Entry(master, **args)
        self._text_variable = tk.StringVar(
            self._widget_instance, self._text_buffer
        )
        self._text_variable.trace_add('write', self.__change_hook__)
        self._widget_instance.configure(textvariable=self._text_variable)
        if self._disabled:
            self._widget_instance.state(["disabled"])
        if self._readonly:
            self._widget_instance.state(["readonly"])
        del self._text_buffer

    def __bind__(self, component: Component) -> None:
        if not self._bind_sb:
            return None
        sb: Scrollbar | None = getattr(component, self._bind_sb, None)
        if not sb:
            return None
        sb._widget_instance.configure(command=self._widget_instance.xview)
        sb._set_horizontal()
        self.widget.configure(xscrollcommand=sb._widget_instance.set)


    @property
    def widget(self) -> ttk.Entry:
        return self._widget_instance

    @property
    def text(self) -> str:
        return self._text_variable.get()
    
    @text.setter
    def text(self, value: str) -> None:
        return self._text_variable.set(value)

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

