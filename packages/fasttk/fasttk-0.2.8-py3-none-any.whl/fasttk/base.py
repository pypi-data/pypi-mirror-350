
import tkinter as tk
from typing import Any
from tkinter import ttk
from PIL import ImageTk, Image
from uuid import uuid4 as random_uuid, UUID
from abc import ABC, abstractmethod
from fasttk.style import Style, StyleRepr
from fasttk.tools import Props, Selector

# States Priority Map

_states_map: dict[str, int] = {
    "normal": 0,
    "pressed": 1,
    "!pressed": 2,
    "disabled": 3,
    "!disabled": 4,
    "focus": 5,
    "!focus": 6,
    "active": 7,
    "!active": 8,
    "selected": 9,
    "!selected": 10,
    "background": 11,
    "!background": 12,
    "readonly": 13,
    "!readonly": 14,
    "alternate": 15,
    "!alternate": 16,
    "invalid": 17,
    "!invalid": 18
}

_states_set: set[str] = set(_states_map.keys())

class StylesManager:
    _instance: "StylesManager"
    _inited: bool

    _style_db: ttk.Style
    _identifier: int
    
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
            cls._instance._inited = False
        return cls._instance
    
    def __init__(self):
        if not self._inited:
            self._inited = True
            self._style_db = ttk.Style()
            self._identifier = 1000

    def get_identifier(self) -> str:
        value = str(self._identifier)
        result = ""
        for digit in value:
            result += chr(ord('A') + ord(digit) - 48)
        self._identifier += 1
        return result

    def single_config(
        self,
        name: str,
        options: dict[str, Any],
        states: dict[tuple[str, ...], dict[str, Any]]
    ) -> None:
        self._style_db.configure(name, None, **options)
        builds: dict[str, list[tuple[Any, ...]]] = {}
        for state, styles in states.items():
            for option_name, value in styles.items():
                if not (option_spec := builds.get(option_name, [])):
                    builds[option_name] = option_spec
                option_spec.append((state, value))
        for specs in builds.values():
            specs.sort(
                key=lambda tp: len(tp[0]),
                reverse=True
            )
        builds = {
            option: [
                (*states, value) for states, value in specs
            ] for option, specs in builds.items()
        }
        self._style_db.map(name, None, **builds)

    def use_style(
        self, 
        src: str,
        style_args: dict[tuple[str, ...], dict[str, Any]],
        **subclasses: dict[tuple[str, ...], dict[str, Any]],
    ) -> str:
        st_args = style_args.copy()
        options = st_args.pop(("normal", ))
        style_name = f"{self.get_identifier()}.{src}"
        self.single_config(style_name, options, st_args)
        for cls, states in subclasses.items():
            opts = states.pop(("normal", ))
            self.single_config(f"{style_name}.{cls}", opts, states)
        return style_name

    def _reset(self):
        pass

# == Base Node & Component Definitions ==

class Component(ABC):

    __vtk_component_name__: str
    __vtk_component_uuid__: UUID
    __vtk_bind_window__: tk.Toplevel
    __vtk_bind_master__: tk.Misc
    __vtk_bind_pcp__: "Component"
    __vtk_object_ref__: str | None
    __vtk_setup_props__: Props
    __vtk_component_styles__: list[Style]
    __vtk_component_node__: "Node"
    __vtk_component_share__: dict[str, Any]

    def __init__(
        self,
        *,
        props: Props = Props(),
        ref: str | None = None
    ):
        super().__init__()
        self.__vtk_component_share__ = {}
        self.__vtk_component_uuid__ = random_uuid()
        _instance_map[self.__vtk_component_uuid__] = self
        self.__vtk_object_ref__ = ref
        self.__vtk_setup_props__ = props

    # Step 1
    def __vtk_build__(self) -> None:
        self.setup(
            *self.__vtk_setup_props__._args,
            **self.__vtk_setup_props__._kwargs
        )
        self.__vtk_component_node__ = self.struct()
        styles = self.styles()
        self.__vtk_component_styles__ = []
        for style in styles:
            if isinstance(style, (list, tuple)):
                self.__vtk_component_styles__.extend(style)
            elif isinstance(style, dict):
                self.__vtk_component_styles__.append(style)
        self.__vtk_component_node__.__vtk_build__()

    # Step 2
    def __vtk_set_ref__(self, obj: object) -> None:
        if self.__vtk_object_ref__:
            setattr(obj, self.__vtk_object_ref__, self)
        self.__vtk_component_node__.__vtk_set_ref__(self)

    # Step 3
    def __vtk_apply_styles__(self) -> None:
        styles = self.__vtk_component_styles__ or []
        struct = self.__vtk_component_node__

        # styles post process
        for style in styles:
            if (states := style.get("_states", None)) is None:
                states = ("normal", )
                style["_states"] = states
            elif isinstance(states, str):
                style["_states"] = (states, )
            elif isinstance(states, tuple):
                temp: list[str] = []
                for state in states:
                    if state in _states_set:
                        temp.append(state)
                temp.sort(key=lambda v: _states_map[v])
                style["_states"] = tuple(temp) if temp else ("normal", )
            else:
                style["_states"] = ("normal", )
        
        struct.__vtk_apply_style__(styles)

    # Step 4
    def __vtk_repr_styles__(self, parent_style: Style) -> None:
        self.__vtk_component_node__.__vtk_repr_styles__(parent_style)
    
    # Step 5
    def __vtk_build_widgets__(
        self,
        master: tk.Misc,
        parent: "Component",
        window: tk.Toplevel
    ) -> None:
        self.__vtk_bind_window__ = window
        self.__vtk_bind_master__ = master
        self.__vtk_bind_pcp__ = parent
        self.__vtk_component_node__.__vtk_build_widgets__(master, self, window)

    # Step 6
    def __vtk_cross_binding__(self) -> None:
        self.__vtk_component_node__.__vtk_cross_binding__(self)

    # Step 7
    def __vtk_mount_hook__(self) -> None:
        self.__vtk_component_node__._widget_instance.bind(
            "<Destroy>", self.__destroy_hook__
        )
        self.on_mount()
        self.__vtk_component_node__.__vtk_mount_hook__()


    def __destroy_hook__(self, event: tk.Event) -> None:
        if event.widget._w == self.__vtk_component_node__._widget_instance._w:
            self.on_destroy()


    def __init_subclass__(cls):
        cls.__vtk_component_name__ = cls.__module__ + '.' + cls.__name__
        _component_map[cls.__vtk_component_name__] = cls

    @property
    def window(self) -> tk.Toplevel:
        return self.__vtk_bind_window__

    @property
    def parent_misc(self) -> tk.Misc:
        return self.__vtk_bind_master__

    @property
    def parent_component(self) -> "Component":
        return self.__vtk_bind_pcp__

    def setup(self, *args: Any, **kwargs: Any) -> None:
        pass

    def on_mount(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass
    
    def destroy(self) -> None:
        _instance_map.pop(self.__vtk_component_uuid__, None)
        if hasattr(self, "__vtk_component_node__"):
            self.__vtk_component_node__._widget_instance.destroy()

    @abstractmethod
    def styles(self) -> list[Style | list[Style]]:
        ...

    @abstractmethod
    def struct(self) -> "Node":
        ...

_component_map: dict[str, type[Component]] = {}
_instance_map: dict[UUID, Component] = {}
_constructed_images: dict[str, Image.Image] = {}
_constructed_tk_images: dict[str, ImageTk.PhotoImage] = {}

class Node(ABC):
    _widget_instance: ttk.Widget
    _bind_master: tk.Misc
    _bind_window: tk.Toplevel
    _inline_style: Style | None
    _use_styles: dict[tuple[str, ...], Style]
    _style_repr_map: dict[tuple[str, ...], StyleRepr]
    _normal_repr: StyleRepr
    _node_tags: set[str]
    _node_type: str
    _node_ref: str | None
    _children: list["Node | Component"]

    def __init__(
        self,
        *,
        tags: str,
        type: str,
        ref: str | None,
        style: Style | None,
        predef_style: Style = {}
    ):
        super().__init__()
        self._node_type = type
        self._inline_style = style
        self._use_styles = { ("normal", ): predef_style.copy() }
        self._style_repr_map = {}
        self._node_tags = set([tag for tag in tags.split()])
        self._node_ref = ref
        self._children = []
    
    def __vtk_build__(self) -> None:
        for child in self._children:
            child.__vtk_build__()

    def __vtk_set_ref__(self, obj: object) -> None:
        if self._node_ref:
            setattr(obj, self._node_ref, self)
        for child in self._children:
            child.__vtk_set_ref__(obj)

    def __vtk_apply_style__(self, styles: list[Style]) -> None:
        for style in styles:
            selector = style.get("_selector", "")
            if not selector: continue
            selector = Selector(selector)

            if selector.check(self._node_type, self._node_tags):
                states = style["_states"]
                if (state_style := self._use_styles.get(states, None)) is None:
                    state_style = {}
                    self._use_styles[states] = state_style
                state_style.update(style)
        for item in self._children:
            if isinstance(item, Node):
                item.__vtk_apply_style__(styles)
            else:
                item.__vtk_apply_styles__()

    def __vtk_repr_styles__(self, parent_style: Style) -> None:
        normal_style = self._use_styles[("normal", )]
        normal_style.update(self._inline_style or {})
        for state, style in self._use_styles.items():
            updated = normal_style.copy()
            updated.update(style)
            self._style_repr_map[state] = StyleRepr(updated, parent_style)
        self._normal_repr = self._style_repr_map[("normal", )]
        for child in self._children:
            child.__vtk_repr_styles__(normal_style)

    def __vtk_build_widgets__(
        self,
        master: tk.Misc,
        component: Component,
        window: tk.Toplevel
    ) -> None:
        self._bind_master = master
        self._bind_window = window
        self.__build__(master, component, window)
        self.__layout_widget__()
        setattr(self._widget_instance, "node", self)
        for child in self._children:
            child.__vtk_build_widgets__(
                self._widget_instance, component, window
            )
    
    def __vtk_mount_hook__(self) -> None:
        for child in self._children:
            child.__vtk_mount_hook__()

    def __vtk_cross_binding__(self, component: Component) -> None:
        self.__bind__(component)
        for child in self._children:
            if isinstance(child, Component):
                child.__vtk_cross_binding__()
            else:
                child.__vtk_cross_binding__(component)


    def __style_map__(self, name_mapping: dict[str, str]) -> dict[tuple[str, ...], dict[str, Any]]:
        result = {}
        for state, st_repr in self._style_repr_map.items():
            result[state] = st_repr.props_map(name_mapping)
        return result

    def __layout_widget__(self) -> None:
        normal_style = self._style_repr_map[("normal", )]
        if normal_style.layout == "pack":
            args = normal_style.props_map({
                "margin_x": "padx",
                "margin_y": "pady",
                "pack_anchor": "anchor",
                "pack_fill": "fill",
                "pack_side": "side",
                "pack_expand": "expand"
            })
            self._widget_instance.pack(args)
        elif normal_style.layout == "grid":
            args = normal_style.props_map({
                "margin_x": "padx",
                "margin_y": "pady",
                "stick": "sticky"
            })
            args["row"], args["rowspan"] = normal_style.row_spec
            args["column"], args["columnspan"] = normal_style.column_spec
            self._widget_instance.grid(args)
        else:
            args = normal_style.props_map({
                "x": "x",
                "y": "y",
                "rel_x": "relx",
                "rel_y": "rely",
                "rel_height": "relheight",
                "rel_width": "relwidth",
                "height": "height",
                "width": "width"
            })
            self._widget_instance.place(args)

    def __load_image__(self, path: str, size: tuple[int, int], scale: float) -> ImageTk.PhotoImage:
        tk_repr = f"{path},{size[0]}x{size[1]},{scale}"
        if not (tk_img := _constructed_tk_images.get(tk_repr, None)):
            if not (raw_image := _constructed_images.get(path, None)):
                raw_image = Image.open(path)
                _constructed_images[path] = raw_image
            
            height = size[1] or raw_image.height
            width = size[0] or raw_image.width
            height = int(height * scale)
            width = int(width * scale)

            tk_img = ImageTk.PhotoImage(raw_image.resize((width, height)))
            _constructed_tk_images[tk_repr] = tk_img
        return tk_img

    @abstractmethod
    def __build__(
        self,
        master: tk.Misc,
        component: Component,
        window: tk.Toplevel
    ) -> None:
        ...
    
    def __bind__(self, component: Component) -> None:
        pass

    @property
    def master(self) -> tk.Misc:
        return self._bind_master
    
    @property
    def window(self) -> tk.Toplevel:
        return self._bind_window

    @property
    def children(self) -> list["Node | Component"]:
        return self._children


def _remove_all_components() -> None:
    StylesManager()._reset()
    for value in list(_instance_map.values()):
        value.destroy()
    _component_map.clear()

def remove_buffers() -> None:
    _constructed_images.clear()
