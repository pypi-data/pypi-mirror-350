
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, Component
from fasttk.style import Style
from typing import Callable, Any
from .scrollbar import Scrollbar

class Text(Node):

    _disabled: bool
    _bind_sbx: str | None
    _bind_sby: str | None
    _reset_modified: bool
    _on_change: Callable | None
    _on_select: Callable | None
    _last_select: str

    _widget_instance: tk.Text

    def __init__(
        self,
        *,
        tags: str = "",
        ref: str | None = None,
        disabled: bool = False,
        on_change: Callable[[str], Any] | None = None,
        on_select: Callable[[str], Any] | None = None,
        scrollbar_x: str | None = None,
        scrollbar_y: str | None = None,
        style: Style | None = None
    ):
        super().__init__(
            tags=tags, type="text", ref=ref, style=style,
            predef_style={
                "cursor": "xterm"
            }
        )
        self._on_change = on_change
        self._on_select = on_select
        self._disabled = disabled
        self._bind_sbx = scrollbar_x
        self._bind_sby = scrollbar_y
        self._reset_modified = False
        self._last_select = ""

    def __change_hook__(self, ev: tk.Event) -> None:
        if not self._reset_modified:
            self._on_change(self._widget_instance.get('1.0', 'end-1chars'))
            self._reset_modified = True
            self._widget_instance.edit_modified(False)
        else:
            self._reset_modified = False

    def __select_hook__(self, ev: tk.Event) -> None:
        indices = self._widget_instance.tag_ranges("sel")
        text = ""
        if indices:
            text = self._widget_instance.get(indices[0].string, indices[1].string)
        if text != self._last_select:
            self._last_select = text
            self._on_select(text)

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
            "scale_length": "length",
            "text_height": "height",
            "label_width": "width",
            "background": "background",
            "foreground": "foreground",
            "use_font": "font",
            "border_width": "borderwidth",
            "relief": "relief",
            "text_wrap": "wrap",
            "select_foreground": "selectforeground",
            "select_background": "selectbackground",
            "insert_color": "insertbackground",
            "insert_width": "insertwidth"
        })
        args["padx"] = self._normal_repr.padding[0]
        args["pady"] = self._normal_repr.padding[1]
        self._widget_instance = tk.Text(master, **args)
        if self._on_change:
            self._widget_instance.bind(
                "<<Modified>>", self.__change_hook__
            )
        if self._on_select:
            self._widget_instance.bind(
                "<<Selection>>", self.__select_hook__
            )
        if self._disabled:
            self._widget_instance.configure(state="disabled")

    def __bind__(self, component: Component):
        cnf = {}
        if self._bind_sbx:
            sb: Scrollbar | None = getattr(component, self._bind_sbx, None)
            if sb:
                sb._widget_instance.configure(command=self._widget_instance.xview)
                sb._set_horizontal()
                cnf["xscrollcommand"] = sb._widget_instance.set
        if self._bind_sby:
            sb: Scrollbar | None = getattr(component, self._bind_sby, None)
            if sb:
                sb._widget_instance.configure(command=self._widget_instance.yview)
                sb._set_vertical()
                cnf["yscrollcommand"] = sb._widget_instance.set
        self._widget_instance.configure(cnf)

    @property
    def widget(self) -> tk.Text:
        return self._widget_instance
    
    @property
    def text(self) -> str:
        return self._widget_instance.get('1.0', 'end-1chars')
    
    @text.setter
    def text(self, value: str) -> None:
        if self._disabled:
            self._widget_instance.configure(state="normal")
        self._widget_instance.delete("1.0", "end")
        size = len(value)
        index = 0
        while index < size:
            self._widget_instance.insert("end", value[index:index+128])
            index += 128
        if self._disabled:
            self._widget_instance.configure(state="disabled")