from yta_image.edition.filter.gameboy import image_file_to_gameboy
from yta_image.edition.filter.sticker import image_file_to_sticker
from yta_image.edition.filter.pixelate import pixelate_image
from yta_image.edition.filter.motion_blur import MotionBlurDirection, apply_motion_blur
from yta_general_utils.dataclasses import FileReturn
from typing import Union


class ImageFilter:
    """
    Class to simplify and encapsulate the functionality
    related to applying filters to an image.
    """

    @staticmethod
    def to_gameboy(
        image_filename: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Apply the original GameBoy colors palette to the provided
        'image_filename'.
        """
        # TODO: We need to refactor this when the original method
        # is also refactored
        return image_file_to_gameboy(image_filename, output_filename)
    
    @staticmethod
    def pixelate(
        image: any,
        pixel_size: int = 8,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Pixelates the provided 'image_filename' and saves
        it as the 'output_filename'. The smaller the
        'pixel_size' is, the less pixelated the image
        becomes.

        We recommend you a 'pixel_size' between 8 and 16.
        """
        return pixelate_image(image, (pixel_size, pixel_size), output_filename)
    
    @staticmethod
    def to_sticker(
        image_filename: str,
        output_filename: Union[str, None] = None
    ):
        """
        Turn the provided 'image_filename' into a sticker, which
        is the same image without the background and with a new
        white and wide border.
        """
        # TODO: Check that it is a valid 'image_filename'
        # TODO: Refactor to accept other image types, not only files
        return image_file_to_sticker(image_filename, output_filename)
    
    @staticmethod
    def motion_blur(
        image: any,
        kernel_size: int = 30,
        direction: MotionBlurDirection = MotionBlurDirection.HORIZONTAL,
        output_filename: Union[str, None] = None
    ):
        """
        Apply a Motion Blur effect, in the given 'direction', to
        the provided 'image'.
        """
        if kernel_size <= 0:
            raise Exception('The "kernel_size" parameter must be a positive number.')

        return apply_motion_blur(image, kernel_size, direction, output_filename)
    
    # TODO: Add 'image_to_sketch' if working, but I think it is
    # too heavy processing for nothing interesting...