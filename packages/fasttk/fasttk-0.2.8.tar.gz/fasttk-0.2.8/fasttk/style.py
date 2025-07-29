
from tkinter import font
from typing import TypedDict, Literal, Any, TypeAlias

# For some platform specified cursor styles,
# See: https://www.tcl-lang.org/man/tcl8.6/TkCmd/cursors.htm
CURSORS: TypeAlias = Literal[
    "X_cursor", "arrow", "based_arrow_down", "based_arrow_up", "boat", "bogosity",
    "bottom_left_corner", "bottom_right_corner", "bottom_side", "bottom_tee",
    "box_spiral", "center_ptr", "circle", "clock", "coffee_mug", "cross",
    "cross_reverse", "crosshair", "diamond_cross", "dot", "dotbox", "double_arrow",
    "draft_large", "draft_small", "draped_box", "exchange", "fleur", "gobbler",
    "gumby", "hand1", "hand2", "heart", "icon", "iron_cross", "left_ptr",
    "left_side", "left_tee", "leftbutton", "ll_angle", "lr_angle", "man",
    "middlebutton", "mouse", "none", "pencil", "pirate", "plus", "question_arrow",
    "right_ptr", "right_side", "right_tee", "rightbutton", "rtl_logo", "sailboat",
    "sb_down_arrow", "sb_h_double_arrow", "sb_left_arrow", "sb_right_arrow",
    "sb_up_arrow", "sb_v_double_arrow", "shuttle", "sizing", "spider", "spraycan",
    "star", "target", "tcross", "top_left_arrow", "top_left_corner",
    "top_right_corner", "top_side", "top_tee", "trek", "ul_angle", "umbrella",
    "ur_angle", "watch", "xterm"
]

# For all available colors in Tcl,
# See: https://www.tcl-lang.org/man/tcl8.6/TkCmd/colors.htm
COLORS: TypeAlias = Literal[
    'alice blue', 'antique white', 'aqua', 'aquamarine', 'azure', 'beige',
    'bisque', 'black', 'blanched almond', 'blue', 'blue violet', 'brown',
    'burlywood', 'cadet blue', 'chartreuse', 'chocolate', 'coral',
    'cornflower blue', 'cornsilk', 'crymson', 'cyan', 'dark blue', 'dark cyan',
    'dark goldenrod', 'dark gray', 'dark green', 'dark grey', 'dark khaki',
    'dark magenta', 'dark olive green', 'dark orange', 'dark orchid', 'dark red',
    'dark salmon', 'dark sea green', 'dark slate blue', 'dark slate gray',
    'dark slate grey', 'dark turquoise', 'dark violet', 'deep pink',
    'deep sky blue', 'dim gray', 'dim grey', 'dodger blue', 'firebrick',
    'floral white', 'forest green', 'fuchsia', 'gainsboro', 'ghost white',
    'gold', 'goldenrod', 'gray', 'green', 'green yellow', 'grey', 'honeydew',
    'hot pink', 'indian red', 'indigo', 'ivory', 'khaki', 'lavender',
    'lavender blush', 'lawn green', 'lemon chiffon', 'light blue', 'light coral',
    'light cyan', 'light goldenrod', 'light goldenrod yellow', 'light gray',
    'light green', 'light grey', 'light pink', 'light salmon', 'light sea green',
    'light sky blue', 'light slate blue', 'light slate gray', 'light slate grey',
    'light steel blue', 'light yellow', 'lime', 'lime green', 'linen', 'magenta',
    'maroon', 'medium aquamarine', 'medium blue', 'medium orchid',
    'medium purple', 'medium sea green', 'medium slate blue',
    'medium spring green', 'medium turquoise', 'medium violet red',
    'midnight blue', 'mint cream', 'misty rose', 'moccasin', 'navajo white',
    'navy', 'navy blue', 'old lace', 'olive', 'olive drab', 'orange',
    'orange red', 'orchid', 'pale goldenrod', 'pale green', 'pale turquoise',
    'pale violet red', 'papaya whip', 'peach puff', 'peru', 'pink', 'plum',
    'powder blue', 'purple', 'red', 'rosy brown', 'royal blue', 'saddle brown',
    'salmon', 'sandy brown', 'sea green', 'seashell', 'sienna', 'silver',
    'sky blue', 'slate blue', 'slate gray', 'slate grey', 'snow',
    'spring green', 'steel blue', 'tan', 'teal', 'thistle', 'tomato',
    'turquoise', 'violet', 'violet red', 'wheat', 'white', 'white smoke',
    'yellow', 'yellow green'
]

_Color: TypeAlias = COLORS | str | tuple[int, int, int]
_Anchor: TypeAlias = Literal[
    "top_left", "top_right", "top",
    "left", "right", "center",
    "bottom_left", "bottom_right", "bottom"
]

RELIEF: TypeAlias = Literal[
    "flat", "groove", "raised", "ridge", "solid", "sunken"
]

STATE: TypeAlias = Literal[
    "normal", "active", "disabled", "focus", "pressed", "selected",
    "background", "readonly", "alternate", "invalid", "!active",
    "!disabled", "!focus", "!pressed", "!selected", "!background",
    "!readonly", "!alternate", "!invalid"
]

_Padding: TypeAlias = int | tuple[int, int, int, int] | tuple[int, int] | tuple[int, int, int]

_constructed_fonts: dict[str, font.Font] = {}

class Style(TypedDict, total=False):

    # selector
    # button.top scaler.y.x.z
    _selector: str

    # states
    _states: tuple[STATE, ...] | STATE

    # display - Only on Frame
    display: Literal["pack", "place", "grid"]

    # margin - In pack/grid container only
    margin: _Padding
    margin_top: int
    margin_left: int
    margin_right: int
    margin_bottom: int

    # padding
    padding: _Padding
    padding_top: int
    padding_left: int
    padding_right: int
    padding_bottom: int

    item_padding: _Padding
    item_padding_top: int
    item_padding_left: int
    item_padding_right: int
    item_padding_bottom: int

    # Pack child params
    expand: bool

    # Pack container params
    pack_direction: Literal["column", "column_reverse", "row", "row_reverse"]
    align_items: Literal["left", "right", "center", "stretch", "top", "bottom"]
    spread_items: bool

    # Grid

    # Format:
    # specs -> <specs>, <spec> | <spec>
    # spec -> <range> <weight>
    # range -> <index> | <index>-<index>
    # example: 
    #   0-1 5, 3 1, 4-6 3
    row_weight: str
    column_weight: str

    # Grid placement:
    # spec -> <index> | <range>
    # range -> <index>-<index>
    grid: str

    # Minsize:
    # Similar with weight format
    row_minsize: str
    column_minsize: str

    # Stick:
    stick: Literal[
        "left", "right", "top", "bottom",
        "horizontal", "vertical",
        "detach_left", "detach_right", "detach_top", "detach_bottom",
        "all", "none"
    ]

    # Place
    left: int | float
    top: int | float
    width: int | float
    height: int | float

    # == Widget options ==

    # Basics
    cursor: CURSORS
    take_focus: bool
    
    # Frame options
    border_width: int

    # Label options
    compound_mode: Literal[
        "text", "image", "center", "top", "bottom", "left", "right", "none"
    ]
    
    font: str
    font_size: int
    font_unit: Literal["pixel", "pound"]
    font_weight: Literal["normal", "bold"]
    font_variant: tuple[Literal["italic", "underlined", "overstrike"], ...]

    foreground: _Color
    background: _Color
    field_background: _Color
    select_foreground: _Color
    select_background: _Color
    light_color: _Color
    dark_color: _Color
    border_color: _Color
    indicator_foreground: _Color
    indicator_background: _Color


    insert_width: int
    insert_color: _Color

    image_height: int
    image_width: int
    image_scale: float

    text_align: Literal['left', 'center', 'right']
    text_wrap: int | Literal['none', 'char', 'word']
    text_width: int
    text_height: int
    compound_position: _Anchor

    border_style: RELIEF
    underline: int
    default_button: bool
    input_mask: str
    input_width: int
    orientation: Literal['vertical', 'horizontal']
    combo_size: int
    combo_foreground: _Color
    combo_background: _Color

    scale_length: int
    scale_width: int
    spin_wrap: bool

    treeview_height: int
    treeview_show: Literal["no_headings", "columns", "all"]
    treeview_select: Literal["single", "multiple", "none"]
    treeview_indent: int
    treeview_row_height: int

    heading_background: _Color
    heading_foreground: _Color
    heading_font: str
    heading_font_size: int
    heading_font_unit: Literal["pixel", "pound"]
    heading_font_weight: Literal["normal", "bold"]
    heading_font_variant: tuple[Literal["italic", "underlined", "overstrike"], ...]
    heading_border_style: RELIEF
    heading_border_color: COLORS

    indicator_size: int
    indicator_margin: _Padding
    indicator_margin_top: int
    indicator_margin_left: int
    indicator_margin_right: int
    indicator_margin_bottom: int

    cell_padding: _Padding
    cell_padding_top: int
    cell_padding_left: int
    cell_padding_right: int
    cell_padding_bottom: int


_anchor_mapping = {
    "top_left": "nw",
    "top_right": "ne",
    "top": "n",
    "left": "w",
    "right": "e",
    "center": "center",
    "bottom_left": "sw",
    "bottom_right": "se",
    "bottom": "s"
}

_pack_direction_mapping = {
    "column": "top",
    "column_reverse": "bottom",
    "row": "left",
    "row_reverse": "right"
}

_stick_mapping = {
    "left": "w",
    "right": "e",
    "top": "n",
    "bottom": "s",
    "horizontal": "we",
    "vertical": "ns",
    "detach_left": "nse",
    "detach_right": "nsw",
    "detach_top": "swe",
    "detach_bottom": "nwe",
    "all": "nswe",
    "none": ""
}

class StyleRepr:

    layout: Literal["pack", "place", "grid"]

    # frame only
    container: Literal["pack", "place", "grid"]

    # pack/grid
    margin_x: tuple[int, int]
    margin_y: tuple[int, int]
    padding: tuple[int, int, int, int]
    item_padding: tuple[int, int, int, int]
    indicator_margin: tuple[int, int, int, int]
    cell_padding: tuple[int, int, int, int]

    # pack
    pack_side: Literal['left', 'right', 'top', 'bottom']
    pack_anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
    pack_fill: Literal["none", "x", "y", "both"]
    pack_expand: bool

    # grid
    row_config: dict[int, dict[str, int]]
    column_config: dict[int, dict[str, int]]
    row_spec: tuple[int, int]
    column_spec: tuple[int, int]
    stick: str

    # place
    x: int | None
    rel_x: float | None
    y: int | None
    rel_y: float | None
    width: int | None
    rel_width: float | None
    height: int | None
    rel_height: float | None

    # widgets
    cursor: str
    take_focus: bool
    use_font: font.Font | None
    heading_use_font: font.Font | None
    compound_mode: Literal[
        "text", "image", "center", "top", "bottom", "left", "right", "none"
    ]
    foreground: str | None
    background: str | None
    field_background: str | None
    heading_background: str | None
    heading_foreground: str | None
    select_foreground: str | None
    select_background: str | None
    indicator_foreground: str | None
    indicator_background: str | None
    border_color: str | None
    insert_color: str | None
    light_color: str | None
    dark_color: str | None
    image_size: tuple[int, int]
    image_scale: float
    compound_anchor: str
    relief: str
    label_justify: str | None
    label_wrap: int | None
    label_underline: int | None
    border_width: int | None
    button_default: str
    entry_show: str | None
    bar_orientation: str
    label_width: int | None
    combobox_height: int | None
    entry_width: int | None

    combo_foreground: str | None
    combo_background: str | None
    scale_length: int | None
    scale_width: int | None
    text_wrap: str
    text_height: int | None
    insert_width: int | None
    spinbox_wrap: bool
    treeview_select: str
    treeview_show: str
    treeview_height: int | None
    treeview_indent: int | None
    treeview_row_height: int | None
    indicator_size: int | None

    heading_relief: str
    heading_border_color: str | None

    def __init__(self, style_sheet: Style, parent_style: Style):
        # layout analyze
        self.layout = parent_style.get("display", None) or "place"
        if self.layout == "pack":
            self.extract_margin(style_sheet)
            self.padding = self.extract_padding(style_sheet, "padding")
            self.extract_pack_side(parent_style)
            self.extract_pack_params(style_sheet, parent_style)
        elif self.layout == "grid":
            self.stick = _stick_mapping[style_sheet.get("stick", "none")]
            self.extract_margin(style_sheet)
            self.padding = self.extract_padding(style_sheet, "padding")
            self.extract_grid_span(style_sheet)
        else:
            self.padding = self.extract_padding(style_sheet, "padding")
            self.extract_place_coord(style_sheet)
        # container analyze
        self.container = style_sheet.get("display", None) or "place"
        if self.container == "grid":
            self.extract_grid_container(style_sheet)
        # set widget props
        self.cursor = style_sheet.get("cursor", "arrow")
        self.take_focus = style_sheet.get("take_focus", False)
        self.compound_mode = style_sheet.get("compound_mode", "center")
        self.extract_font(style_sheet)
        self.extract_font(
            style_sheet,
            font="heading_font",
            font_size="heading_font_size",
            font_unit="heading_font_unit",
            font_weight="heading_font_weight",
            font_variant="heading_font_variant",
            target="heading_use_font"
        )

        self.foreground = self.extract_color(style_sheet.get("foreground", None))
        self.background = self.extract_color(style_sheet.get("background", None))
        self.field_background = self.extract_color(style_sheet.get("field_background", None))
        self.heading_background = self.extract_color(style_sheet.get("heading_background", None))
        self.heading_foreground = self.extract_color(style_sheet.get("heading_foreground", None))
        self.select_background = self.extract_color(style_sheet.get("select_background", None))
        self.select_foreground = self.extract_color(style_sheet.get("select_foreground", None))
        self.insert_color = self.extract_color(style_sheet.get("insert_color", None))
        self.border_color = self.extract_color(style_sheet.get("border_color", None))
        self.indicator_foreground = self.extract_color(style_sheet.get("indicator_foreground", None))
        self.indicator_background = self.extract_color(style_sheet.get("indicator_background", None))
        self.light_color = self.extract_color(style_sheet.get("light_color", None))
        self.dark_color = self.extract_color(style_sheet.get("dark_color", None))
        self.heading_border_color = self.extract_color(style_sheet.get("heading_border_color", None))

        # label props
        self.label_justify = style_sheet.get("text_align", "center")
        self.extract_text_wrap(style_sheet)
        self.relief = style_sheet.get("border_style", "flat")
        self.label_underline = style_sheet.get("underline", None)
        self.extract_image(style_sheet)
        self.extract_compound_position(style_sheet)
        self.border_width = style_sheet.get("border_width", None)
        self.label_width = style_sheet.get("text_width", None)

        # button props
        button_default = style_sheet.get("default_button", False)
        self.button_default = "active" if button_default else "normal"

        # entry props
        self.entry_show = style_sheet.get("input_mask", None)
        self.entry_width = style_sheet.get("input_width", None)

        # scrollbar props
        self.bar_orientation = style_sheet.get("orientation", "vertical")

        # combobox props
        self.combobox_height = style_sheet.get("combo_size", None)
        self.combo_foreground = self.extract_color(style_sheet.get("combo_foreground", None))
        self.combo_background = self.extract_color(style_sheet.get("combo_background", None))

        # scale props
        self.scale_length = style_sheet.get("scale_length", None)
        self.scale_width = style_sheet.get("scale_width", None)

        # text props
        self.text_height = style_sheet.get("text_height", None)
        self.insert_width = style_sheet.get("insert_width", None)

        # spinbox wrap
        self.spinbox_wrap = style_sheet.get("spin_wrap", False)

        # treeview props
        self.extract_treeview(style_sheet)
        self.heading_relief = style_sheet.get("heading_border_style", "flat")
        self.treeview_indent = style_sheet.get("treeview_indent", None)
        self.treeview_row_height = style_sheet.get("treeview_row_height", None)
        self.item_padding = self.extract_padding(style_sheet, "item_padding")
        self.indicator_margin = self.extract_padding(style_sheet, "indicator_margin")
        self.indicator_size = style_sheet.get("indicator_size", None)
        self.cell_padding = self.extract_padding(style_sheet, "cell_padding")


    def props_map(self, name_mapping: dict[str, str]) -> dict[str, Any]:
        result = {}
        for src, dest in name_mapping.items():
            value = getattr(self, src, None)
            if value is not None:
                result[dest] = value
        return result

    # pack extraction

    def extract_pack_params(self, style: Style, parent: Style) -> None:
        parent_align = parent.get("align_items", "center")

        # expand widget if parent_spread is spread
        self.pack_expand = parent.get("spread_items", False)

        # check axis
        x_axis = self.pack_side in ("left", "right")
        # Vertical fill
        x_expand = True if parent_align == "stretch" else False
        # Axis fill - Expand along axis
        y_expand = style.get("expand", False)
        # Expand reduction -> fill
        if x_expand and y_expand: self.pack_fill = "both"
        elif x_expand: self.pack_fill = "y" if x_axis else "x"
        elif y_expand: self.pack_fill = "x" if x_axis else "y"
        else: self.pack_fill = "none"

        # Default anchor - center
        self.pack_anchor = "center"
        # No vertical fill - set anchor
        if not x_expand:
            # X axis
            if x_axis:
                if parent_align == "top":
                    self.pack_anchor = "n"
                elif parent_align == "bottom":
                    self.pack_anchor = "s"
            # Y axis
            else:
                if parent_align == "left":
                    self.pack_anchor = "w"
                elif parent_align == "right":
                    self.pack_anchor = "e"

    def extract_pack_side(self, style: Style) -> None:
        direction = style.get("pack_direction", "column")
        self.pack_side = _pack_direction_mapping.get(direction)

    def extract_margin(self, style: Style) -> None:
        margin = self.extract_padding(style, "margin")
        self.margin_x = (margin[0], margin[2])
        self.margin_y = (margin[1], margin[3])
    
    def extract_padding(self, style: Style, prefix: str) -> tuple[int, int, int, int]:
        padding = style.get(prefix, (0, 0, 0, 0))
        if isinstance(padding, int):
            padding = [padding] * 4
        elif isinstance(padding, tuple):
            length = len(padding)
            if length == 2:
                padding = [padding[0], padding[1], padding[0], padding[1]]
            elif length == 3:
                padding = [padding[0], padding[1], padding[2], padding[1]]
            elif length <= 1:
                padding = [0, 0, 0, 0]
            elif length == 4:
                padding = list(padding)
            else:
                padding = list(padding[0:4])
        else:
            padding = [0, 0, 0, 0]
        for index, key in enumerate(("_top", "_right", "_bottom", "_left")):
            key = prefix + key
            if (n := style.get(key, -1)) >= 0: padding[index] = n
        return (padding[3], padding[0], padding[1], padding[2])

    # grid extraction

    def extract_grid_container(self, style: Style) -> None:
        
        def decode_and_set(
            option_repr: str,
            field: str,
            target: dict[int, dict[str, int]]
        ) -> None:
            if not option_repr:
                return None
            result: list[tuple[list[int], int]] = []
            for segment in option_repr.split(','):
                a, w = segment.strip().split(' ')
                if '-' in a:
                    l, r = map(int, a.split('-'))
                    index = list(range(l, r + 1))
                else:
                    index = [int(a)]
                result.append((index, int(w)))
            for option in result:
                for index in option[0]:
                    if setting := target.get(index, {}):
                        setting[field] = option[1]
                    else:
                        setting[field] = option[1]
                        target[index] = setting

        self.row_config = {}
        self.column_config = {}
        decode_and_set(style.get("row_weight", ""), "weight", self.row_config)
        decode_and_set(style.get("column_weight", ""), "weight", self.column_config)
        decode_and_set(style.get("row_minsize", ""), "minsize", self.row_config)
        decode_and_set(style.get("column_minsize", ""), "minsize", self.column_config)
        
    def extract_grid_span(self, style: Style) -> None:
        def decode_str(spec_str: str) -> tuple[int, int]:
            if not spec_str: return (0, 1)
            if '-' in spec_str:
                start, end = map(int, spec_str.split('-'))
                return (start, end - start + 1)
            else:
                return (int(spec_str), 1)
        specs = style.get("grid", "0, 0")
        row, column = map(str.strip, specs.split(','))
        self.row_spec = decode_str(row)
        self.column_spec = decode_str(column)

    # place extraction

    def extract_place_coord(self, style: Style) -> None:
        width = style.get("width", 50)
        height = style.get("height", 50)
        left = style.get("left", 0)
        top = style.get("top", 0)

        self.width = None
        self.rel_width = None
        self.height = None
        self.rel_height = None
        self.x = None
        self.rel_x = None
        self.y = None
        self.rel_y = None

        if isinstance(width, int): self.width = width
        else: self.rel_width = width
        if isinstance(height, int): self.height = height
        else: self.rel_height = height
        if isinstance(left, int): self.x = left
        else: self.rel_x = left
        if isinstance(top, int): self.y = top
        else: self.rel_y = top

    # font extraction

    def extract_font(self, style: Style, **src_kws: str) -> None:
        src_kws.setdefault("font", "font")
        src_kws.setdefault("font_size", "font_size")
        src_kws.setdefault("font_unit", "font_unit")
        src_kws.setdefault("font_weight", "font_weight")
        src_kws.setdefault("font_variant", "font_variant")
        src_kws.setdefault("target", "use_font")
        setattr(self, src_kws["target"], None)
        font_spec = style.get(src_kws["font"], "")
        if not font_spec: return None
        size = style.get(src_kws["font_size"], 10)
        unit = style.get(src_kws["font_unit"], "pixel")
        size = size if unit == "pound" else -size
        weight = style.get(src_kws["font_weight"], "normal")
        variants = style.get(src_kws["font_variant"], ())
        variant_no = 0
        slant = "roman"
        overstrike = False
        underlined = False
        if "italic" in variants:
            slant = "italic"
            variant_no += 1
        if "overstrike" in variants:
            overstrike = True
            variant_no += 2
        if "underlined" in variants:
            underlined = True
            variant_no += 4
        font_repr = font_spec + str(size) + weight + str(variant_no)
        target_font = _constructed_fonts.get(font_repr, None)
        if not target_font:
            target_font = font.Font(
                family=font_spec, size=size, slant=slant, weight=weight,
                overstrike=overstrike, underline=underlined,
                name=font_repr
            )
            _constructed_fonts[font_repr] = target_font
        setattr(self, src_kws["target"], target_font)
    
    # color extraction

    def extract_color(self, color_repr: str | tuple[int, int, int]) -> str | None:
        if not color_repr: return None
        if isinstance(color_repr, str): return color_repr
        else: return "#%02x%02x%02x" % color_repr

    # image extraction

    def extract_image(self, style: Style) -> None:
        self.image_size = (
            style.get("image_width", 0), style.get("image_height", 0)
        )
        self.image_scale = style.get("image_scale", 1.0)

    # compound_position extraction

    def extract_compound_position(self, style: Style) -> None:
        v = style.get("compound_position", "")
        if not v: self.compound_anchor = "center"
        else: self.compound_anchor = _anchor_mapping.get(v, "center")

    # wrap extraction

    def extract_text_wrap(self, style: Style) -> None:
        wrap = style.get("text_wrap", None)
        if wrap is None:
            self.label_wrap = None
            self.text_wrap = "none"
            return None
        if isinstance(wrap, int):
            self.label_wrap = wrap
            self.text_wrap = "none"
        else:
            self.label_wrap = None
            self.text_wrap = wrap

    # treeview extraction
    def extract_treeview(self, style: Style) -> None:
        self.treeview_height = style.get("treeview_height", None)
        select_mode = style.get("treeview_select", "single")
        show = style.get("treeview_show", "all")
        if select_mode == "single":
            self.treeview_select = "browse"
        elif select_mode == "multiple":
            self.treeview_select = "extended"
        else:
            self.treeview_select = "none"
        if show == "all":
            self.treeview_show = "tree headings"
        elif show == "columns":
            self.treeview_show = "headings"
        else:
            self.treeview_show = "tree"



if __name__ == '__main__':
    print(StyleRepr({
        "display": "grid",
        "margin": 10,
        "margin_right": 30,
        "margin_top": 20,
        "padding": (50, 10),
        "padding_left": 20,
        "row_weight": "0 5, 1-3 1, 4 5",
        "column_weight": "0 5, 1-3 1, 4 5",
        "column_minsize": "1-5 20",
        "row": "2-3",
        "column": "0",
        "height": 50,
        "stick": ("n", "e", "s", "w")
    }, {
        
    }).__dict__)

