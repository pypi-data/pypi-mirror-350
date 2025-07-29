
import json
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from fasttk.base import Node, StylesManager
from fasttk.style import Style
from typing import Callable, Generic, TypeVar, Any

_T = TypeVar("_T")

class Checkbutton(Node, Generic[_T]):

    _text_variable: tk.StringVar
    _json_variable: tk.StringVar
    _buffer_text: str | None
    _image_url: str | None
    _image_ref: ImageTk.PhotoImage | None
    _on_value: str
    _off_value: str
    _available: bool
    _checked: bool
    _command: Callable | None

    def __init__(
        self,
        *,
        text: str | None = None,
        image: str | None = None,
        tags: str = "",
        ref: str | None = None,
        on_value: _T = True,
        off_value: _T = False,
        checked: bool = False,
        disabled: bool = False,
        on_click: Callable[[], Any] | None = None,
        style: Style | None = None
    ):
        super().__init__(
            tags=tags, ref=ref, type="checkbutton", style=style,
            predef_style={
                "cursor": "hand2"
            }
        )
        self._buffer_text = text or ""
        self._image_url = image
        self._image_ref = None
        self._available = not disabled
        self._on_value = json.dumps(on_value)
        self._off_value = json.dumps(off_value)
        self._checked = checked
        self._command = on_click

    def __build__(self, master: tk.Misc, component, window) -> None:
        if self._image_url:
            self._image_ref = self.__load_image__(
                self._image_url,
                self._normal_repr.image_size,
                self._normal_repr.image_scale
            )
        args = self._normal_repr.props_map({
            "compound_mode": "compound",
            "cursor": "cursor",
            "label_underline": "underline",
            "take_focus": "takefocus",
            "label_width": "width"
        })
        st_args = self.__style_map__({
            "compound_anchor": "anchor",
            "background": "background",
            "foreground": "foreground",
            "use_font": "font",
            "padding": "padding",
            "compound_mode": "compound",
            "relief": "indicatorrelief",
            "indicator_foreground": "indicatorforeground",
            "indicator_background": "indicatorbackground",
            "indicator_margin": "indicatormargin",
            "indicator_size": "indicatorsize",
            "light_color": "upperbordercolor",
            "dark_color": "lowerbordercolor"
        })
        args["command"] = self._command
        args["image"] = self._image_ref
        args["onvalue"] = self._on_value
        args["offvalue"] = self._off_value
        args["style"] = StylesManager().use_style("TCheckbutton", st_args)
        self._widget_instance = ttk.Checkbutton(master, **args)
        self._text_variable = tk.StringVar(
            self._widget_instance, self._buffer_text
        )
        self._json_variable = tk.StringVar(self._widget_instance, "false")
        self._widget_instance.configure(
            textvariable=self._text_variable,
            variable=self._json_variable
        )
        self._json_variable.set(
            self._on_value if self._checked else self._off_value
        )
        if not self._available:
            self._widget_instance.state(["disabled"])
        del self._buffer_text
        

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
            self._json_variable.set(
                self._on_value if value else self._off_value
            )
            self._checked = value
