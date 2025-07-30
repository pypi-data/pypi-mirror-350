from yta_image.parser import ImageParser
from yta_programming.output import Output
from yta_general_utils.file.enums import ImageFileExtension
from yta_general_utils.dataclasses import FileReturn
from PIL import ImageDraw, Image
from typing import Union
from abc import ABC, abstractmethod

import numpy as np


class ImageMaskPreset(ABC):
    """
    Abstract class to be implemented by the custom
    image masks.
    """
    
    @abstractmethod
    def apply_on(
        image: Union[str, Image.Image, np.ndarray],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        pass

class RoundedCornersImageMaskPreset(ImageMaskPreset):

    def apply_on(
        image: Union[str, Image.Image, np.ndarray],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Generate a mask of the provided 'image' with the corners
        rounded and return it as a not normalized RGB Pillow Image 
        with all values between 0 (white) and 255 (black). This 
        means that the result, if converted to array, will be
        [0, 0, 0] for each white pixel and [255, 255, 255] for 
        black ones.

        Thank you: https://github.com/Zulko/moviepy/issues/2120#issue-2141195159
        """
        image = ImageParser.to_pillow(image)

        # Create a whole black image of the same size
        mask = Image.new('L', image.size, 'black')
        mask_drawing = ImageDraw.Draw(mask)

        # Generate the rounded corners mask
        w, h = image.size
        radius = 20
        # Rectangles to cover
        mask_drawing.rectangle([radius, 0, w - radius, h], fill = 'white')
        mask_drawing.rectangle([0, radius, w, h - radius], fill = 'white')
        # Circles at the corners: TL, TR, BL, BR
        mask_drawing.ellipse([0, 0, 2 * radius, 2 * radius], fill = 'white')
        mask_drawing.ellipse([w - 2 * radius, 0, w, 2 * radius], fill = 'white')
        mask_drawing.ellipse([0, h - 2 * radius, 2 * radius, h], fill = 'white')
        mask_drawing.ellipse([w - 2 * radius, h - 2 * radius, w, h], fill = 'white')

        if output_filename is not None:
            output_filename = Output.get_filename(output_filename, ImageFileExtension.PNG)
            mask.save(output_filename)

        return FileReturn(
            mask,
            output_filename
        )
    
class TicketImageMaskPreset(ImageMaskPreset):

    def apply_on(
        image: Union[str, Image.Image, np.ndarray],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Create triangles on top and bottom to simulate
        a shop printed ticket over the given 'image'.
        """
        image = ImageParser.to_pillow(image)

        # Create a whole black image of the same size
        mask = Image.new('L', image.size, 'white')
        mask_drawing = ImageDraw.Draw(mask)

        # Generate the mask
        w, h = image.size
        triangle_size = 15

        for i in range(0, w, triangle_size):
            mask_drawing.polygon([(i, h), (i + triangle_size, h), (i + triangle_size // 2, h - triangle_size)], fill = 'black')
            mask_drawing.polygon([(i, 0), (i + triangle_size, 0), (i + triangle_size // 2, triangle_size)], fill = 'black')

        if output_filename is not None:
            output_filename = Output.get_filename(output_filename, ImageFileExtension.PNG)
            mask.save(output_filename)

        return FileReturn(
            mask,
            output_filename
        )
