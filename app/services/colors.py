DEFAULT_COLORS = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]

THEMES: dict[str, list[str]] = {
    "green": DEFAULT_COLORS,
    "blue": ["#ebedf0", "#9ecae1", "#6baed6", "#3182bd", "#08519c"],
    "purple": ["#ebedf0", "#c9b1ff", "#9a7de8", "#6f42c1", "#4a2490"],
    "orange": ["#ebedf0", "#ffcb8e", "#f9a03f", "#e07602", "#bd5d00"],
    "red": ["#ebedf0", "#fdbbbb", "#f07070", "#d63333", "#a31515"],
    "pink": ["#ebedf0", "#f9b4ed", "#e876d3", "#d63da8", "#b01885"],
    "halloween": ["#ebedf0", "#fdf156", "#ffc722", "#ff9711", "#04001b"],
}


def get_theme(name: str) -> list[str] | None:
    return THEMES.get(name.lower())


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_palette(base_hex: str) -> list[str]:
    """Generate 5 colors: empty gray + 4 shades from light to dark based on base color."""
    base = hex_to_rgb(base_hex)
    empty = hex_to_rgb("#ebedf0")
    intensities = [0.25, 0.5, 0.75, 1.0]
    palette = [DEFAULT_COLORS[0]]
    for t in intensities:
        r = int(empty[0] + (base[0] - empty[0]) * t)
        g = int(empty[1] + (base[1] - empty[1]) * t)
        b = int(empty[2] + (base[2] - empty[2]) * t)
        palette.append(rgb_to_hex(r, g, b))
    return palette
