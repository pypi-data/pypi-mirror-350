
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from fasttk.base import Node, StylesManager, Component
from fasttk.style import Style
from typing import Callable, Any, Self, Literal, TypeAlias, overload, Iterable
from .scrollbar import Scrollbar
from ..style import Style, StyleRepr, _anchor_mapping


ANCHOR: TypeAlias = Literal[
    "top-left", "top", "top-right",
    "left", "center", "right",
    "bottom-left", "bottom", "bottom-right"
]


class TreeviewItem:
    
    _id: str
    _treeview: "Treeview"

    def __init__(self, iid: str, bind: "Treeview", image):
        self._treeview = bind
        self._id = iid
        self._image = image

    def move(
        self,
        parent: "TreeviewItem | None" = None,
        index: int | None = None
    ) -> None:
        use_index = "end" if index is None else index
        self._treeview._widget_instance.move(
            self._id, parent._id, use_index
        )

    def detach(self) -> None:
        self._treeview._widget_instance.detach(self._id)

    def delete(self) -> None:
        self._treeview._widget_instance.delete(self._id)
        self._treeview._item_map.pop(self._id)

    def children(self) -> list["TreeviewItem"]:
        item_names = self._treeview._widget_instance.get_children(self._id)
        items = [self._treeview._item_map[name] for name in item_names]
        return items

    def focus(self) -> None:
        self._treeview._widget_instance.focus(self._id)

    def select(self) -> None:
        self._treeview._widget_instance.selection_add(self._id)

    def cancel(self) -> None:
        self._treeview._widget_instance.selection_remove(self._id)

    @property
    def name(self) -> str:
        return self._treeview._widget_instance.item(self._id, "text")
    
    @name.setter
    def name(self, value: str) -> None:
        self._treeview._widget_instance.item(self._id, text=value)

    @overload
    def tags(self) -> list[str]:
        ...

    @overload
    def tags(self, new_tags: list[str]) -> None:
        ...

    def tags(self, new_tags: list[str] | None = None) -> list[str] | None:
        if new_tags:
            self._treeview._widget_instance.item(self._id, tags=new_tags)
        else:
            _tags = self._treeview._widget_instance.item(self._id, "tags")
            return _tags or []

    def items(self) -> dict[str, Any]:
        return self._treeview._widget_instance.set(self._id)

    def __getitem__(self, column_id: str) -> str:
        return self._treeview._widget_instance.set(self._id, column_id)
    
    def __setitem__(self, column_id: str, value: str) -> None:
        return self._treeview._widget_instance.set(self._id, column_id, value)

    def __repr__(self) -> str:
        values = self._treeview._widget_instance.set(self._id)
        return f"TreeviewItem<{self._id}>{values}"


class TreeviewColumn:
    
    _heading: str
    _id: str
    _width: int | None
    _min_width: int | None
    _stretch: bool
    _item_anchor: str
    _head_anchor: str
    _index: int
    _bind_tv: "Treeview"
    _on_click: Callable
    _ref: str | None
    _image: ImageTk.PhotoImage | None
    _image_src: str | None
    _image_size: tuple[int, int] | None
    _visible: bool

    def __init__(
        self,
        id: str = "#0",
        *,
        ref: str | None = None,
        heading: str | None = None,
        image: tuple[str, int, int] | str | None = None,
        width: int | None = None,
        min_width: int | None = None,
        stretch: bool = True,
        item_anchor: ANCHOR = "center",
        heading_anchor: ANCHOR = "center",
        on_click: Callable[["TreeviewColumn"], Any] | None = None,
        visible: bool = True
    ):
        self._id = id
        self._heading = heading or id
        self._width = width
        self._min_width = min_width
        self._stretch = stretch
        self._item_anchor = item_anchor
        self._head_anchor = heading_anchor
        self._on_click = on_click
        self._ref = ref
        self._image = None
        self._image_src = None
        self._image_size = None
        if isinstance(image, tuple):
            self._image_src = image[0]
            self._image_size = (image[1], image[2])
        elif isinstance(image, str):
            self._image_src = image
        self._visible = True if id == "#0" else visible
    

    def __click_hook__(self) -> None:
        if self._on_click:
            self._on_click(self)

    def _bind_treeview(self, tv: "Treeview", idx: int) -> None:
        self._index = idx
        self._bind_tv = tv

    def _column_args(self) -> dict[str, Any]:
        args = {}
        args["anchor"] = _anchor_mapping.get(self._item_anchor, "center")
        if self._min_width: args["minwidth"] = self._min_width
        if self._width: args["width"] = self._width
        args["stretch"] = self._stretch
        return args
    
    def _heading_args(self) -> dict[str, Any]:
        if self._image_src and not self._image:
            photo = Image.open(self._image_src)
            if self._image_size:
                photo = photo.resize(self._image_size)
            self._image = ImageTk.PhotoImage(photo)
        args = {}
        args["text"] = self._heading
        args["anchor"] = _anchor_mapping.get(self._item_anchor, "center")
        args["command"] = self.__click_hook__
        if self._image: args["image"] = self._image
        return args


    @property
    def id(self) -> str:
        return self._id

    @property
    def heading(self) -> str:
        return self._heading
    
    @heading.setter
    def heading(self, value: str) -> None:
        if value != self._heading:
            self._bind_tv._widget_instance.heading(self._id, text=value)
            self._heading = value

    @property
    def image(self) -> ImageTk.PhotoImage | None:
        return self._image
    
    @image.setter
    def image(self, src: tuple[str, int, int] | str | None) -> None:
        if src is None:
            self._bind_tv._widget_instance.heading(self._id, image="")
            return None
        if isinstance(src, tuple):
            path = src[0]
            size = src[1, 2]
        elif isinstance(src, str):
            path = src
            size = None
        if path == self._image_src and size == self._image_size:
            return None
        image = Image.open(path)
        if size:
            image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        self._bind_tv._widget_instance.heading(self._id, image=photo)
        self._image = photo

    @property
    def visible(self) -> bool:
        return self._visible
    
    @visible.setter
    def visible(self, value: bool) -> None:
        if self._id == "#0":
            return None
        if value != self._visible:
            self._visible = value
            self._bind_tv._update_visible()


class Treeview(Node):

    _bind_sbx: str | None
    _bind_sby: str | None
    _on_select: Callable
    _on_open: Callable
    _on_close: Callable
    _columns: list[TreeviewColumn]
    _column_names: tuple[str, ...]
    _item_map: dict[str, TreeviewItem]
    _item_tags: set[str]
    _tag_images: dict[str, ImageTk.PhotoImage]
    _disabled: bool

    _widget_instance: ttk.Treeview

    def __init__(
        self,
        *,
        tags: str = "",
        ref: str | None = None,
        scrollbar_x: str | None = None,
        scrollbar_y: str | None = None,
        on_select: Callable[[list[TreeviewItem]], Any] | None = None,
        on_open: Callable[[TreeviewItem], Any] | None = None,
        on_close: Callable[[TreeviewItem], Any] | None = None,
        disabled: bool = False,
        style: Style | None = None
    ):
        super().__init__(tags=tags, type="treeview", ref=ref, style=style)
        self._columns = []
        self._on_select = on_select
        self._on_open = on_open
        self._on_close = on_close
        self._bind_sbx = scrollbar_x
        self._bind_sby = scrollbar_y
        self._item_map = {}
        self._item_tags = set()
        self._disabled = disabled
        self._tag_images = {}

    def __select_hook__(self, ev):
        if not self._disabled and self._on_select:
            self._on_select(self.selection)

    def __open_hook__(self, ev):
        if self._on_open:
            self._on_open(self.focus)

    def __close_hook__(self, ev):
        if self._on_close:
            self._on_close(self.focus)

    def set_columns(self, *columns: TreeviewColumn) -> Self:
        names = []
        for index, column in enumerate(columns):
            if (column_name := column._id) != "#0":
                names.append(column_name)
            self._columns.append(column)
            column._bind_treeview(self, index)
        self._column_names = tuple(names)
        return self

    def insert(
        self,
        parent: TreeviewItem | None = None,
        index: int | None = None,
        *,
        name: str | None = None,
        tags: list[str] | None = None,
        values: tuple[str, ...] | None = None,
        image: tuple[str, int, int] | str | None = None,
        open: bool = False
    ) -> TreeviewItem:
        parent_str = parent._id if parent else ""
        use_index = "end" if index is None else index
        use_image = None
        size = None
        path = None
        if isinstance(image, tuple):
            path = image[0]
            size = (image[1], image[2])
        elif isinstance(image, str):
            path = image[0]
        if path:
            photo = Image.open(path)
            if size:
                photo = photo.resize(size)
            use_image = ImageTk.PhotoImage(photo)
        new_id = self._widget_instance.insert(
            parent_str, use_index, text=name or "_", values=values, open=open,
            tags=tags, image=use_image
        )
        item = TreeviewItem(new_id, self, use_image)
        self._item_map[new_id] = item
        return item

    def children(self) -> list[TreeviewItem]:
        item_names = self._widget_instance.get_children()
        items = [self._item_map[name] for name in item_names]
        return items


    def add_tag(
        self,
        tag: str,
        style: Style,
        *,
        image: str | None = None
    ) -> None:
        if tag in self._item_tags:
            return None
        style_repr = StyleRepr(style, {})
        if image:
            data = Image.open(image)
            width, height = style_repr.image_size
            if width and height:
                width *= style_repr.image_scale
                height *= style_repr.image_scale
                data = data.resize((width, height))
            image_data = ImageTk.PhotoImage(data)
        else:
            image_data = None
            
        options = style_repr.props_map({
            "background": "background",
            "foreground": "foreground",
            "use_font": "font"
        })
        if image_data:
            options["image"] = image_data
            self._tag_images[tag] = image_data
        self._widget_instance.tag_configure(tag, **options)
        self._item_tags.add(tag)

    def remove_tag(self, tag: str) -> None:
        if tag not in self._item_tags:
            return None
        for item in self._item_map.values():
            current_tags = item.tags()
            try:
                index = current_tags.index(tag)
            except ValueError:
                index = -1
            if index >= 0:
                current_tags.pop(index)
        self._item_tags.remove(tag)
        self._tag_images.pop(tag)


    def _update_visible(self) -> None:
        display = []
        for column in self._columns:
            if column._visible:
                display.append(column._id)
        display.pop(0)
        self._widget_instance.configure(displaycolumns=display)


    def __build__(self, master: tk.Misc, component, window) -> None:
        # build treeview widget
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
            "treeview_show": "show",
            "treeview_height": "height",
            "treeview_select": "selectmode"
        })
        st_args = self.__style_map__({
            "padding": "padding",
            "foreground": "foreground",
            "background": "background",
            "field_background": "fieldbackground",
            "use_font": "font",
            "treeview_indent": "indent",
            "treeview_row_height": "rowheight",
            "light_color": "lightcolor",
            "dark_color": "darkcolor",
            "border_color": "bordercolor",
            "relief": "relief"
        })
        head_args = self.__style_map__({
            "heading_use_font": "font",
            "heading_background": "background",
            "heading_foreground": "foreground",
            "heading_border_color": "bordercolor",
            "heading_relief": "relief"
        })
        item_args = self.__style_map__({
            "item_padding": "padding",
            "indicator_margin": "indicatormargins",
            "indicator_size": "indicatorsize"
        })
        cell_args = self.__style_map__({
            "cell_padding": "padding"
        })

        args["columns"] = self._column_names
        args["style"] = StylesManager().use_style(
            "Treeview", st_args,
            Heading=head_args,
            Item=item_args,
            Cell=cell_args
        )
        self._widget_instance = ttk.Treeview(master, **args)
        del self._column_names

        # setup columns
        for column in self._columns:
            self._widget_instance.heading(column._id, **column._heading_args())
            self._widget_instance.column(column._id, **column._column_args())
        
        # bind events
        self._widget_instance.bind("<<TreeviewSelect>>", self.__select_hook__)
        self._widget_instance.bind("<<TreeviewOpen>>", self.__open_hook__)
        self._widget_instance.bind("<<TreeviewClose>>", self.__close_hook__)

        if self._disabled:
            self._widget_instance.state(["disabled"])

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

    def __vtk_set_ref__(self, obj: object):
        for column in self._columns:
            if column._ref:
                setattr(obj, column._ref, column)
        super().__vtk_set_ref__(obj)


    @property
    def widget(self) -> ttk.Treeview:
        return self._widget_instance
    
    @property
    def disabled(self) -> bool:
        return self._disabled
    
    @disabled.setter
    def disabled(self, value: bool) -> None:
        if value != self._disabled:
            self._widget_instance.state(["disabled" if value else "!disabled"])
            self._disabled = value

    @property
    def selection(self) -> list[TreeviewItem]:
        return [
            self._item_map[item_name]
            for item_name in self._widget_instance.selection()
        ]

    @selection.setter
    def selection(self, items: Iterable[TreeviewItem]) -> None:
        self._widget_instance.selection_set(*(item._id for item in items))

    @property
    def focus(self) -> TreeviewItem | None:
        value = self._widget_instance.focus()
        return self._item_map[value] if value else None

    @focus.setter
    def focus(self, item: TreeviewItem) -> None:
        self._widget_instance.focus(item._id)
