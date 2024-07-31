from typing import Tuple

from framebuffer import Framebuffer


def draw_rectangle(
    fb: Framebuffer,
    start: Tuple[int, int],
    end: Tuple[int, int],
    color: Tuple[int, int, int],
):
    x1, y1 = start
    x2, y2 = end

    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            fb.set_pixel(x, y, color)
