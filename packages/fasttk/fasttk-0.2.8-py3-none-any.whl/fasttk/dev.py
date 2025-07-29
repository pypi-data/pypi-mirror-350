
import os
import sys
import logging
import argparse
import threading
import importlib
import watchfiles
from queue import Queue as TQueue

from fasttk.tkvm import ftk

CWD = os.getcwd()

stop_event = threading.Event()
pass_event = threading.Event()
reload_queue: TQueue[list[str]] = TQueue()

root_logger = logging.getLogger("FastTk")
logger = logging.getLogger("FastTk.DevServer")

def _watch_worker(watch_target: str):

    logger = logging.getLogger("FastTk.WatchFiles")
    logger.info(f"Watching files at '{watch_target}'.")

    for changes in watchfiles.watch(
        watch_target, stop_event=stop_event, watch_filter=watchfiles.PythonFilter()
    ):
        logger.info(f"Changes detected:")
        path_list = []
        for file_change in changes:
            change, file = file_change
            logger.info(f" -> {change.name} file at {file}")
            path_list.append(file)
        reload_queue.put(path_list)

        pass_event.wait()
        logger.info("Reload complete, keep watching.")
        pass_event.clear()

    logger.info("WatchFiles thread exited.")

def _serve(
    src: str,
    cls_name: str,
    title: str,
    size: tuple[int, int],
    background: str
) -> None:
    
    logger.info(f"Loading window entrance in module {src}.")
    
    sys.path.append(CWD)
    entrance = importlib.import_module(src)
    component_cls = getattr(entrance, cls_name, None)
    if not component_cls:
        raise ImportError(f"Export entry point '{cls_name}' not found in module '{src}'.")

    logger.info("Starting FastTk dev server.")

    src_segments = src.split('.')
    module_dir = os.path.join(CWD, src_segments[0])
    watch_target = module_dir if os.path.isdir(module_dir) else CWD
    watch_thread = threading.Thread(
        target=_watch_worker, name="fasttk.WatchFiles", args=(watch_target, )
    )
    watch_thread.start()
    
    logger.info("Press Ctrl+C to stop.")

    def reload_callback(modules: list[str]) -> None:

        # NOTE This is a brute force reload implementation.
        # All related modules & packages are removed from sys.modules,
        # then the entire **top** module/package is **re-imported**.
        # This may cause performance issues, but avoids manual interpretation of
        # module relies and some difficult corner cases.

        nonlocal entrance
        reload_target = src_segments[0]
        try:
            logger.info(f"Reloading module/package '{reload_target}'.")
            remove_candidates = []
            for m_name in sys.modules.keys():
                if m_name.startswith(reload_target):
                    remove_candidates.append(m_name)
            for remove in remove_candidates:
                sys.modules.pop(remove, None)
            entrance = importlib.import_module(src)
            component = getattr(entrance, cls_name, None)
            if not component:
                raise ImportError(f"Export entry point '{cls_name}' not found in module '{src}'.")
            ftk.mount_component(ftk._tk, component)
        except Exception as e:
            logger.warning("Exception while reloading, skip this reload:", exc_info=True)

    try:
        ftk.main_window(
            component_cls, title=title, size=size, background=background
        )
        ftk._track_reload(reload_queue, pass_event, reload_callback)
        ftk.mainloop()
        stop_event.set()
    except KeyboardInterrupt:
        logger.info("Stop FastTk dev server.")
        pass_event.set()
        stop_event.set()

    watch_thread.join()

def start_dev_server(
    src: str,
    cls_name: str = "export",
    title: str = "FastTk Dev Window",
    size: tuple[int, int] = (600, 400),
    background: str = "white"
) -> None:
    try:
        _serve(src, cls_name, title, size, background)
    except Exception as e:
        logger.error(
            "Exception while starting dev server:", exc_info=True
        )
        pass_event.set()
        stop_event.set()

def _console():
    parser = argparse.ArgumentParser(
        description="Start FastTk dev server."
    )

    parser.add_argument(
        "module_path",
        type=str,
        help="input module path"
    )

    parser.add_argument(
        "-c", "--class",
        type=str,
        default=None,
        help="specify the class of main component"
    )

    parser.add_argument(
        "-s", "--size",
        type=str,
        default=None,
        help="specify the size of the dev window"
    )

    parser.add_argument(
        "-t", "--title",
        type=str,
        default=None,
        help="specify the title of the dev window"
    )

    parser.add_argument(
        "-b", "--background",
        type=str,
        default=None,
        help="specify the background of the dev window"
    )

    cmd_args = parser.parse_args()

    args = {}
    args["src"] = cmd_args.module_path
    if cls_name := getattr(cmd_args, "class"):
        args["cls_name"] = cls_name
    if cmd_args.size:
        args["size"] = tuple(map(int, cmd_args.size.split('x')))
    if cmd_args.title:
        args["title"] = cmd_args.title
    if cmd_args.background:
        args["background"] = cmd_args.background
    
    start_dev_server(**args)
