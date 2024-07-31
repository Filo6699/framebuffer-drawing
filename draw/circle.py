from typing import Tuple

from framebuffer import Framebuffer


def draw_circle(
    fb: Framebuffer,
    center: Tuple[int, int],
    radius: int,
    color: Tuple[int, int],
):
    x, y = center
    for ax in range(-radius, radius + 1):
        for ay in range(-radius, radius + 1):
            if ax == ay == 0:
                continue
            dist = (ax * ax + ay * ay) ** (0.5)
            if dist <= radius:
                fb.set_pixel(x + ax, y + ay, color)
