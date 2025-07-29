
import atexit
import logging
from tkinter import *
from tkinter import ttk
from queue import Queue as TQueue, Empty
from threading import Event as TEvent
from uuid import UUID, uuid4 as random_uuid
from typing import TypeVar, Coroutine, Any, Callable, Never

from fasttk.style import COLORS
from fasttk.aworker import AsyncWorker, CallWrapper
from fasttk.base import Component, Props, remove_buffers, _remove_all_components

VERSION = "v0.2.8"
_T = TypeVar("_T")

def _then(obj: Any) -> None:
    pass

def _error(e: Exception) -> Never:
    raise e

_logger = logging.getLogger("FastTk")

class FastTk:

    _tk: Tk
    _window_map: dict[UUID, Toplevel]
    _worker: AsyncWorker
    _reload_queue: TQueue[list[str]]
    _pass_event: TEvent
    _import_cb: Callable

    def __init__(self):
        self._tk = Tk()
        ttk.Style().theme_use("clam")
        self._window_map = {}
        self._worker = AsyncWorker(self._tk)
    
    def _mount_component(
        self,
        obj: Tk | Toplevel | Widget,
        component: Component
    ) -> None:
        component.__vtk_build__()
        component.__vtk_set_ref__(obj)
        component.__vtk_apply_styles__()
        component.__vtk_repr_styles__(
            {} if isinstance(obj, (Toplevel, Tk)) else obj.node._use_style
        )
        component.__vtk_build_widgets__(
            obj, component,
            obj if isinstance(obj, (Toplevel, Tk)) else obj.winfo_toplevel()
        )
        component.__vtk_cross_binding__()
        component.__vtk_mount_hook__()
        
        remove_buffers()
    
    def _remove_window(self, window_id: UUID, e: Event) -> None:
        if e.widget._w == ".!toplevel":
            self._window_map.pop(window_id)

    def _clear_up(self) -> None:
        self._worker.stop()


    # for dev server

    def _track_reload(self, q_reload: TQueue, e_pass: TEvent, callback: Callable) -> None:
        self._reload_queue = q_reload
        self._pass_event = e_pass
        self._import_cb = callback
        self._tk.after(50, self._track_reload_call)
    
    def _track_reload_call(self):
        try:
            modules = self._reload_queue.get_nowait()
        except Empty:
            pass
        else:
            # reload
            self._remove_all()
            self._import_cb(modules)
            # notice
            self._reload_queue.task_done()
            self._pass_event.set()
        finally:
            self._tk.after(50, self._track_reload_call)

    def _remove_all(self):
        _remove_all_components()
        for window in list(self._window_map.values()):
            window.destroy()
        self._window_map.clear()

    # for normal usage

    def main_window(
        self,
        cp: type[Component],
        props: Props | None = None,
        *,
        title: str = "MainWindow",
        size: tuple[int, int] = (400, 300),
        background: COLORS = "white"
    ) -> None:
        props = props if props else Props()
        component = cp(props=props)
        self._tk.title(title)
        self._tk.geometry(f"{size[0]}x{size[1]}")
        self._tk.configure(background=background)
        self._mount_component(self._tk, component)

    def create_window(
        self,
        cp: type[Component],
        props: Props | None = None,
        *,
        title: str = "NewWindow",
        size: tuple[int, int] = (400, 300),
        background: COLORS = "white"
    ) -> Toplevel:
        props = props if props else Props()
        window_id = random_uuid()
        window = Toplevel(self._tk)
        window.title(title)
        window.geometry(f"{size[0]}x{size[1]}")
        window.configure(background=background)
        window.bind("<Destroy>", lambda e: self._remove_window(window_id, e))
        self._window_map[window_id] = window
        component = cp(props=props)
        self._mount_component(window, component)
        return window

    def mount_component(
        self,
        obj: Tk | Toplevel | Widget,
        cp: type[Component],
        props: Props | None = None,
    ) -> Component:
        component = cp(props=props or Props())
        self._mount_component(obj, component)
        return component

    def promise(
        self,
        task: Coroutine[Any, Any, _T] | Callable[..., _T],
        then: Callable[[_T], Any] = _then,
        error: Callable[[Exception], Any] = _error,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None
    ) -> None:
        return self._worker.run(CallWrapper(task, args, kwargs), then, error)

    def mainloop(self) -> None:
        try:
            _logger.debug(f"FastTk  {VERSION}  ᓚᘏᗢ")
            atexit.register(self._clear_up)
            self._worker.start()
            self._tk.mainloop()
        finally:
            self._worker.stop()
            _logger.debug("Goodbye!~   ᓚᘏᗢ")


ftk = FastTk()
