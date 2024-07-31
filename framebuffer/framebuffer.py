import mmap
import struct
import fcntl
from typing import Tuple
from PIL import Image


# Constants for ioctl to get screen information
FBIOGET_VSCREENINFO = 0x4600


class Framebuffer:
    def __init__(self, fbdev: str = "/dev/fb0"):
        """
        Initialize the framebuffer object.

        :param fbdev: Path to the framebuffer device.
        """
        self._fbfd = open(fbdev, "r+b")
        self._vinfo = struct.unpack(
            "16I", fcntl.ioctl(self._fbfd, FBIOGET_VSCREENINFO, " " * 64)
        )
        self.fb_width, self.fb_height, fb_bpp = (
            self._vinfo[0],
            self._vinfo[1],
            self._vinfo[6],
        )
        self._fb_bytes = fb_bpp // 8

        if self._fb_bytes not in [3, 4]:
            raise ValueError("Unsupported bytes per pixel")

        self._fb_data_size = self.fb_width * self.fb_height * self._fb_bytes

        self._fbdata = mmap.mmap(
            self._fbfd.fileno(), self._fb_data_size, mmap.MAP_SHARED, mmap.PROT_WRITE
        )

    def fill(self, color: Tuple[int, int, int]) -> None:
        """
        Fill the entire framebuffer with a single color.

        :param color: A tuple representing the RGB color to fill the framebuffer.
        """
        color = self._convert_color(color)
        self._fbdata[:] = color * (self.fb_width * self.fb_height)

    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """
        Set a single pixel to a specified color.

        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :param color: A tuple representing the RGB color of the pixel.
        """
        if x < 0 or y < 0 or x >= self.fb_width or y >= self.fb_height:
            return

        offset = (x + y * self.fb_width) * self._fb_bytes
        pixel_value = self._convert_color(color)
        self._fbdata[offset : offset + self._fb_bytes] = pixel_value

    def set_range(
        self,
        start_point: Tuple[int, int],
        end_point: Tuple[int, int],
        color: Tuple[int, int, int],
    ):
        """
        Set a range of pixels in the buffer to a specified color.
        Goes horizonally and then down from start point address to end point address.

        :param start_point: The starting point (x, y) of the range.
        :param end_point: The ending point (x, y) of the range.
        :param color: A tuple representing the RGB color of the range.
        """
        straddr = (start_point[0] + start_point[1] * self.fb_width) * self._fb_bytes
        endaddr = (end_point[0] + end_point[1] * self.fb_width) * self._fb_bytes

        pixels_amount = (endaddr - straddr) // self._fb_bytes
        pixel_value = self._convert_color(color)
        self._fbdata[straddr:endaddr] = pixel_value * pixels_amount

    def make_screenshot(self, filename="./screenshot.png"):
        """
        Take a screenshot of the current framebuffer and save it as a PNG file.

        :param filename: The filename to save the screenshot.
        """
        mode = "RGB" if self._fb_bytes == 3 else "RGBA"

        self._fbdata.seek(0)
        pixels = self._fbdata.read(self.fb_width * self.fb_height * self._fb_bytes)
        image = Image.frombytes(mode, (self.fb_width, self.fb_height), pixels)

        if self._fb_bytes == 3:
            # For BGR format, we convert to RGB
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        elif self._fb_bytes == 4:
            # For BGRA format, we convert to RGBA
            r, g, b, a = image.split()
            image = Image.merge("RGBA", (b, g, r, a))

        image.save(filename, "PNG")

    def _convert_color(self, color: Tuple[int, int, int]):
        """
        Convert an RGB color to the appropriate pixel format.

        :param color: A tuple representing the RGB color.
        :return: The pixel value in the appropriate format.
        """
        if self._fb_bytes == 4:  # ARGB format
            pixel_value = struct.pack(
                "I",
                (0xFF << 24) | (color[0] << 16) | (color[1] << 8) | color[2],
            )
        elif self._fb_bytes == 3:  # RGB format
            pixel_value = struct.pack("BBB", color[0], color[1], color[2])
        return pixel_value

    def __del__(self):
        """
        Clean up resources by closing the mmap and file descriptor.
        """
        if self._fbdata:
            self._fbdata.close()
        if self._fbfd:
            self._fbfd.close()
