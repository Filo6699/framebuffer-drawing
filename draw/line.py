from typing import Tuple

from framebuffer import Framebuffer


def draw_line(
    fb: Framebuffer,
    start: Tuple[int, int],
    end: Tuple[int, int],
    color: Tuple[int, int, int],
):
    if start[0] > end[0]:
        start, end = end, start

    x2, y2 = end
    x2 -= start[0]
    y2 -= start[1]

    cur_x = 0

    for x in range(x2 + 1):
        y = round(cur_x * y2 / x2)
        fb.set_pixel(cur_x + start[0], y + start[1], color)

        cur_x += 1
