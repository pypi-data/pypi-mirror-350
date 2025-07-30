from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from climax._renderer import HalfcellRenderer

from rich_pixels import Pixels

from textual import events
from textual.app import RenderResult
from textual.widgets import Static

class ImagePanel(Static, can_focus=True):    

    def __init__(self, theimage:np.ndarray, cmap: str = 'gray', id=None):
        super().__init__(id=id)

        self.zoom_factor = 1.0

        self.renderer = None
        self.renderer_yscale = 0.5
        self.renderer_xscale = 1.0

        self.set_cmap(cmap)
        self.set_pixels(theimage)


    def render(self) -> RenderResult:
        return self.pixels

    def set_pixels(self, theimage: np.ndarray, vmin: Optional[int] = 0, vmax: Optional[int] = 255, zoom_factor: Optional[float] = 1.):
        self.image = theimage
        if zoom_factor:
            self.zoom_factor = zoom_factor

        mapped_image = self.cmap(self.stretch(np.clip(theimage, vmin, vmax)).astype(np.uint8))  # apply colormap. When you invoke a color map like this, it expects pixel values in the range 0-255. stretch does that conversion
        for achannel in range(mapped_image.shape[2]):
            mapped_image[:, :, achannel] = self.stretch(mapped_image[:, :, achannel])
        
        self.renderer = HalfcellRenderer(mapped_image)
        segments = self.renderer.render((int(self.image.shape[0] * self.zoom_factor), int(self.image.shape[1] * self.zoom_factor)))

        self.pixels = Pixels.from_segments(segments)

        # These three lines adjust the dimensions of the image panel to fit the image.
        self.styles.width = self.image.shape[1]*self.renderer_xscale * self.zoom_factor
        self.styles.height = self.image.shape[0]*self.renderer_yscale * self.zoom_factor 

    def set_cmap(self, thecmap: str = 'gray'):
        self.cmap = plt.get_cmap(thecmap)

    def display_slice(self):
        self.update(self.pixels)

    async def _on_mouse_move(self, event: events.MouseMove) -> None:
        x, y = int(event.x / (self.zoom_factor*self.renderer_xscale)), int(event.y / (self.zoom_factor * self.renderer_yscale))

        if x < self.image.shape[1] and y < self.image.shape[0]-1:
            self.tooltip = f"(x={x},y={y}:{y+1})={self.image[y, x]}:{self.image[y+1, x]}"  # We do not seem to be able to get subpixel resolution for the MouseEvent. 
        elif x < self.image.shape[1] and y == self.image.shape[0]-1:
            self.tooltip = f"(x={x},y={y})={self.image[y, x]}"  # We do not seem to be able to get subpixel resolution for the MouseEvent. 
        else:
            self.tooltip = None
        event.stop()

    def stretch(self, image_array: np.ndarray, minimum: int = 0, maximum: int = 255) \
            -> np.ndarray:
        """
        Linear stretch of the contrast of an image.
        :param image_array:
        :param minimum: minimum pixel value in the resulting image (0)
        :param maximum: maximum pixel value (255)
        :return: image_out, an image array.
        """

        sc: float = 0.

        # Define output variable.
        image_out: np.ndarray = image_array.copy()

        if maximum == minimum:
            image_out[:] = minimum
            return image_out

        # Find the appropriate pixel values for the low and high thresholds.
        low = np.min(image_array)
        high = np.max(image_array)

        if high == low:
            image_out[:] = (minimum + maximum) / 2
            return image_out

        # Determine the scaling factor.
        sc = (maximum - minimum) / (high - low)

        # Linear stretch of image_in.
        if low != 0:
            image_out = image_out - low

        if sc != 1:
            image_out = image_out * sc

        if minimum != 0:
            image_out = image_out + minimum

        return image_out

     
