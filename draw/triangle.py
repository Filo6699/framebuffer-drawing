from typing import Tuple
from itertools import combinations

from framebuffer import Framebuffer


def point_line_sdf(
    point: Tuple[int, int],
    line_point1: Tuple[int, int],
    line_point2: Tuple[int, int],
) -> bool:
    """
    Signed distance from a point to a line.
    (i don't really know what side is which sign)
    """

    x, y = point

    x1, y1 = line_point1
    x2, y2 = line_point2

    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    sign = (a * x + b * y + c) >= 0

    return sign


def draw_triangle(
    fb: Framebuffer,
    p1: Tuple[int, int],
    p2: Tuple[int, int],
    p3: Tuple[int, int],
    color: Tuple[int, int, int],
):
    # If triangle is faced away from camera, it doesn't get rendered
    if point_line_sdf(p3, p1, p2) == False:
        return

    min_x = min(p1[0], p2[0], p3[0])
    min_y = min(p1[1], p2[1], p3[1])

    max_x = max(p1[0], p2[0], p3[0])
    max_y = max(p1[1], p2[1], p3[1])

    lines = [set() for _ in range(max_y - min_y + 1)]

    for comb in combinations((p1, p2, p3), 2):
        x1, y1 = comb[0]
        x2, y2 = comb[1]

        for l in range(min(y2, y1), max(y2, y1) + 1):
            denom = y2 - y1
            if denom == 0:
                denom = 1
            x = round((l - y1) * (x2 - x1) / denom + x1)
            lines[l - min_y].add(x)

    for y, l in enumerate(lines):
        l = list(l)
        if len(l) == 1:
            # print(l[0], y)
            fb.set_pixel(l[0], y + min_y, color)
            continue
        fb.set_range((min(l), y + min_y), (max(l), y + min_y), color)
