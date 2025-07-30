
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from fasttk.base import Node, StylesManager
from fasttk.style import Style

class Label(Node):

    _widget_instance: ttk.Label

    _text_variable: tk.StringVar
    _buffer_text: str | None
    _image_url: str | None
    _image_ref: ImageTk.PhotoImage | None

    def __init__(
        self,
        *,
        text: str | None = None,
        image: str | None = None,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, ref=ref, type="label", style=style)
        self._buffer_text = text or ""
        self._image_url = image
        self._image_ref = None

    def __build__(self, master: tk.Misc, component, window) -> None:
        if self._image_url:
            self._image_ref = self.__load_image__(
                self._image_url,
                self._normal_repr.image_size,
                self._normal_repr.image_scale
            )
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus"
        })
        st_args = self.__style_map__({
            "relief": "relief",
            "use_font": "font",
            "padding": "padding",
            "label_width": "width",
            "border_color": "bordercolor",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "border_width": "borderwidth",
            "foreground": "foreground",
            "background": "background",
            "label_underline": "underline",
            "compound_anchor": "anchor",
            "compound_mode": "compound",
            "label_wrap": "wraplength",
            "label_justify": "justify"
        })
        args["image"] = self._image_ref
        args["style"] = StylesManager().use_style("TLabel", st_args)
        self._widget_instance = ttk.Label(master, **args)
        self._text_variable = tk.StringVar(self._widget_instance, self._buffer_text)
        self._widget_instance.configure(textvariable=self._text_variable)
        del self._buffer_text


    @property
    def widget(self) -> ttk.Label:
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
            self._image_ref = url_or_image
            return None
        if not url_or_image:
            self._image_url = None
            self._widget_instance.configure(image="")
            return None
        if self._image_url == url_or_image:
            return None

        self._image_ref = self.__load_image__(
            url_or_image, self._normal_repr.image_size, self._normal_repr.image_scale
        )
        self._image_url = url_or_image
        self._widget_instance.configure(image=self._image_ref)
