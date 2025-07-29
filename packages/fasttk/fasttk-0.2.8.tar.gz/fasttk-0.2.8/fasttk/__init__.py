
import sys
from logging import (
    Formatter, StreamHandler, getLogger, INFO, LogRecord, WARNING, ERROR,
    DEBUG, Logger
)

class _ColoredFormatter(Formatter):

    COLORMAP = {
        DEBUG: "32",
        INFO: "39",
        WARNING: "33",
        ERROR: "31"
    }

    def formatMessage(self, record: LogRecord):
        s = super().formatMessage(record)
        return f"\x1b[{self.COLORMAP[record.levelno]}m{s}\x1b[0m"

def _setup_logger() -> tuple[Logger, StreamHandler]:
    print("\x1b]4;2;rgb:39/c5/bb\x1b\\", end="")
    _lg = getLogger("FastTk")
    _lg.setLevel(DEBUG)
    _lg_h = StreamHandler(sys.stdout)
    _lg_h.setFormatter(_ColoredFormatter(
        "%(asctime)s [%(levelname)s](%(name)s) %(message)s",
        "%Y-%m-%d %H:%M:%S"
    ))
    _lg.addHandler(_lg_h)
    return _lg, _lg_h
_logger, _handler = _setup_logger()

def remove_logger() -> None:
    _logger.removeHandler(_handler)

from fasttk.base import Component, Node
from fasttk.tools import Props, EventSpec
from fasttk.style import Style
from fasttk.tkvm import ftk
from fasttk.nodes import *

__all__ = (
    "TreeviewItem",
    "TreeviewColumn",
    "Treeview",
    "Spinbox",
    "Text",
    "Scale",
    "Combobox",
    "Scrollbar",
    "Entry",
    "Radiobutton",
    "Checkbutton",
    "Node",
    "Label",
    "Button",
    "Frame",
    "Props",
    "Component",
    "Style",
    "EventSpec",
    "ftk",
    "remove_logger",
)
