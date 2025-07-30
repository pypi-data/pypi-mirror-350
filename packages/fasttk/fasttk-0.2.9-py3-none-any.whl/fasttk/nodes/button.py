
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from fasttk.base import Node, StylesManager
from fasttk.style import Style
from typing import Callable, Any

class Button(Node):
    
    _text_variable: tk.StringVar
    _buffer_text: str | None
    _image_url: str | None
    _image_ref: ImageTk.PhotoImage | None
    _command: Callable | None
    _available: bool

    def __init__(
        self,
        *,
        text: str | None = None,
        image: str | None = None,
        on_click: Callable[[], Any] | None = None,
        disabled: bool = False,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(
            tags=tags, ref=ref, type="button", style=style,
            predef_style={
                "cursor": "hand2"
            }
        )
        self._buffer_text = text or ""
        self._image_url = image
        self._image_ref = None
        self._command = on_click
        self._available = not disabled

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
            "button_default": "default",
            "label_width": "width"
        })
        style_args = self.__style_map__({
            "compound_anchor": "anchor",
            "background": "background",
            "foreground": "foreground",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "border_color": "bordercolor",
            "border_width": "borderwidth",
            "use_font": "font",
            "padding": "padding",
            "compound_mode": "compound",
            "relief": "relief"
        })
        args["style"] = StylesManager().use_style("TButton", style_args)
        if self._command: args["command"] = self._command
        if self._image_ref: args["image"] = self._image_ref
        self._widget_instance = ttk.Button(master, **args)
        self._text_variable = tk.StringVar(self._widget_instance, self._buffer_text)
        self._widget_instance.configure(textvariable=self._text_variable)
        if not self._available:
            self._widget_instance.state(["disabled"])
        del self._buffer_text
        

    @property
    def widget(self) -> ttk.Button:
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

