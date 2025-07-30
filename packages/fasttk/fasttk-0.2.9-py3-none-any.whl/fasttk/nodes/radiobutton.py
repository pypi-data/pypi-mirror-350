
import json
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from fasttk.base import Node, StylesManager, Component
from fasttk.style import Style
from typing import Callable, Generic, TypeVar, Any

_T = TypeVar("_T")

class Radiobutton(Node, Generic[_T]):

    _text_variable: tk.StringVar
    _json_variable: tk.StringVar
    _buffer_text: str | None
    _image_url: str | None
    _image_ref: ImageTk.PhotoImage | None
    _value: str
    _available: bool
    _checked: bool
    _command: Callable | None
    _group: str

    def __init__(
        self,
        *,
        text: str | None = None,
        image: str | None = None,
        tags: str = "",
        ref: str | None = None,
        group: str = "default",
        value: _T = 0,
        checked: bool = False,
        disabled: bool = False,
        on_click: Callable[[], Any] | None = None,
        style: Style | None = None
    ):
        super().__init__(
            tags=tags, ref=ref, type="radiobutton", style=style,
            predef_style={
                "cursor": "hand2"
            }
        )
        self._buffer_text = text or ""
        self._image_url = image
        self._image_ref = None
        self._available = not disabled
        self._value = json.dumps(value)
        self._checked = checked
        self._command = on_click
        self._group = group

    def __build__(self, master: tk.Misc, component: Component, window) -> None:
        if self._image_url:
            self._image_ref = self.__load_image__(
                self._image_url,
                self._normal_repr.image_size,
                self._normal_repr.image_scale
            )
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
        })
        st_args = self.__style_map__({
            "relief": "relief",
            "use_font": "font",
            "padding": "padding",
            "label_width": "width",
            "light_color": "upperbordercolor",
            "dark_color": "lowerbordercolor",
            "border_width": "borderwidth",
            "foreground": "foreground",
            "background": "background",
            "label_underline": "underline",
            "compound_anchor": "anchor",
            "compound_mode": "compound",
            "label_wrap": "wraplength",
            "label_justify": "justify",
            "indicator_margin": "indicatormargin",
            "indicator_size": "indicatorsize",
            "indicator_foreground": "indicatorforeground",
            "indicator_background": "indicatorbackground",
        })
        args["command"] = self._command
        args["image"] = self._image_ref
        args["value"] = self._value
        args["style"] = StylesManager().use_style("TRadiobutton", st_args)
        self._widget_instance = ttk.Radiobutton(master, **args)

        self._text_variable = tk.StringVar(
            self._widget_instance, self._buffer_text
        )

        var_src = f"rb_{self._group}"
        json_var = component.__vtk_component_share__.get(var_src, None)
        if json_var is None:
            json_var = tk.StringVar(self._widget_instance, "false")
            component.__vtk_component_share__[var_src] = json_var
        self._json_variable = json_var

        self._widget_instance.configure(
            textvariable=self._text_variable,
            variable=self._json_variable
        )

        if self._checked:
            self._json_variable.set(self._value)
        if not self._available:
            self._widget_instance.state(["disabled"])
        
        del self._buffer_text
        del self._group
        

    @property
    def widget(self) -> ttk.Checkbutton:
        return self._widget_instance

    @property
    def text(self) -> str:
        return self._text_variable.get()
    
    @text.setter
    def text(self, value: str) -> None:
        self._text_variable.set(value)

    @property
    def image(self) -> ImageTk.PhotoImage | None:
        return self._image_ref
    
    @image.setter
    def image(self, url_or_image: str | ImageTk.PhotoImage) -> None:
        if isinstance(url_or_image, ImageTk.PhotoImage):
            self._image_url = None
            self._widget_instance.configure(image=url_or_image)
            return None
        if self._image_url == url_or_image:
            return None
        if not url_or_image:
            self._image_url = None
            self._widget_instance.configure(image=None)

        self._image_ref = self.__load_image__(
            url_or_image, self._normal_repr.image_size, self._normal_repr.image_scale
        )
        self._image_url = url_or_image
        self._widget_instance.configure(image=self._image_ref)

    @property
    def disabled(self) -> bool:
        return not self._available
    
    @disabled.setter
    def disabled(self, value: bool) -> None:
        state = not value
        if state != self._available:
            self._widget_instance.state(["!disabled"])\
            if state else self._widget_instance.state(["disabled"])
            self._available = state

    @property
    def value(self) -> _T:
        return json.loads(self._json_variable.get())

    @property
    def checked(self) -> bool:
        return self._checked
    
    @checked.setter
    def checked(self, value: bool) -> None:
        if self._checked != value:
            self._json_variable.set(self._value)
            self._checked = value

