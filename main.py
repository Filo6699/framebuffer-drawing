from time import time as now
from time import sleep
from random import randint

from framebuffer import Framebuffer
import draw


def run():
    fb = Framebuffer()
    fb.fill((0, 0, 0))

    p1 = (1500, 600)
    p2 = (400, 800)
    p3 = (800, 100)
    color = (255, 0, 0)
    draw.triangle(fb, p1, p2, p3, color)
    draw.rectange(fb, (200, 200), (700, 700), (0, 255, 255))
    draw.circle(fb, (900, 900), 50, (255, 255, 0))
    draw.line(fb, (0, 1080 // 2), (1919, 1080 // 2), (255, 255, 255))

    fb.make_screenshot()


if __name__ == "__main__":
    run()
