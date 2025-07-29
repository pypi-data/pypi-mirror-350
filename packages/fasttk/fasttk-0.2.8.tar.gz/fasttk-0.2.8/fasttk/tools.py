
from tkinter.font import Font
from typing import Any, Literal, TypeAlias

MODIFIERS: TypeAlias = Literal[
    "Control",
    "Mod1",
    "Alt",
    "Mod2",
    "Shift",
    "Mod3",
    "Lock",
    "Mod4",
    "Extended",
    "Mod5",
    "Button1",
    "Meta",
    "Button2",
    "Double",
    "Button3",
    "Triple",
    "Button4",
    "Quadruple",
    "Button5",
]

EVENT_TYPES: TypeAlias = Literal[
    "Activate",
    "Destroy",
    "Map",
    "ButtonPress",
    "Button",
    "Enter",
    "MapRequest",
    "ButtonRelease",
    "Expose",
    "Motion",
    "Circulate",
    "FocusIn",
    "MouseWheel",
    "CirculateRequest",
    "FocusOut",
    "Property",
    "Colormap",
    "Gravity",
    "Reparent",
    "Configure",
    "KeyPress",
    "Key",
    "ResizeRequest",
    "ConfigureRequest",
    "KeyRelease",
    "Unmap",
    "Create",
    "Leave",
    "Visibility",
    "Deactivate"
]

BUTTON: TypeAlias = Literal[0, 1, 2, 3, 4, 5]

# For full list of available key names,
# see: https://www.tcl-lang.org/man/tcl8.6/TkCmd/keysyms.htm
KEYS: TypeAlias = Literal[
    "BackSpace", "5", "K", "at", "H", "g", "D", "F11", 
    "F5", "Clear", "s", "equal", "F8", "1", "P", "L", 
    "V", "Prior", "c", "Pause", "numbersign", "End", "bracketleft", "F3",
    "e", "braceright", "6", "braceleft", "Left", "z", "parenleft", "Control_R",
    "minus", "b", "F", "y", "Return", "comma", "j", "ampersand",
    "v", "F12", "B", "S", "Shift_L", "Shift_R", "q", "3",
    "t", "parenright", "J", "Delete", "quotedbl", "Next", "0", "Z",
    "period", "m", "Y", "8", "p", "Control_L", "Alt_R", "Q",
    "question", "F9", "N", "M", "less", "u", "Caps_Lock", "n",
    "Down", "W", "semicolon", "F7", "bracketright", "2", "asciicircum", "F4",
    "k", "T", "underscore", "A", "U", "apostrophe", "exclam", "4",
    "I", "bar", "Up", "F10", "7", "asciitilde", "greater", "percent",
    "9", "colon", "F1", "X", "asterisk", "h", "l", "plus",
    "Right", "Alt_L", "Scroll_Lock", "backslash", "x", "App", "dollar", "F2",
    "E", "Tab", "i", "Win_R", "space", "slash", "r", "o",
    "C", "R", "O", "G", "grave", "Insert", "Num_Lock", "Win_L",
    "Home", "Escape", "a", "w", "F6", "d", "f"
]

class Props:

    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any):
        self._args = args
        self._kwargs = kwargs

class Selector:
    
    _select_map: dict[str, list[tuple[str]]]

    def __init__(self, selector: str):
        self._select_map = {}
        self._select_map["*"] = []
        or_select = selector.split()
        for select in or_select:
            if select.startswith("."):
                target = self._select_map.get("*")
                tags = select.removeprefix(".").split(".")
                target.append(tuple(tags))
            else:
                segments = select.split(".")
                target = self._select_map.get(segments[0], None)
                if target is None:
                    target = []
                    self._select_map[segments[0]] = target
                target.append(tuple(segments[1:]))
    
    def check(self, type: str, tags: set[str]) -> bool:
        typed = self._select_map.get(type, [])
        for require in typed:
            if not require: return True
            if all(tag in tags for tag in require):
                return True
        for require in self._select_map.get("*"):
            if all(tag in tags for tag in require):
                return True
        return False

class _EventSpec:
    def __call__(
        self,
        *,
        event: EVENT_TYPES | str,
        button: BUTTON | None = None,
        key: KEYS | str | None = None,
        modifier1: MODIFIERS | None = None,
        modifier2: MODIFIERS | None = None,
        virtual: bool = False
    ) -> str:
        builds = []
        if modifier2: builds.append(modifier2)
        if modifier1: builds.append(modifier1)
        builds.append(event)
        if button is not None: builds.append(str(button))
        if key: builds.append(key)
        inner = '-'.join(builds)
        return f"<<{inner}>>" if virtual else f"<{inner}>"

class _TclFont:
    
    def __call__(self, font: Font) -> str:
        f = font.actual()
        parts = [f['family'], str(f['size'])]

        if f.get('weight', 'normal') == 'bold':
            parts.append('bold')
        if f.get('slant', 'roman') == 'italic':
            parts.append('italic')
        if f.get('underline', 0):
            parts.append('underline')
        if f.get('overstrike', 0):
            parts.append('overstrike')

        return ' '.join(parts)

EventSpec = _EventSpec()
FontDescriptor = _TclFont()
