import random
from bokeh.palettes import Viridis256 as Palette


used_colors = set()


def get_color():
    global used_colors
    color = random.choice(Palette)
    while color in used_colors:
        color = random.choice(Palette)
    used_colors.add(color)
    return color
