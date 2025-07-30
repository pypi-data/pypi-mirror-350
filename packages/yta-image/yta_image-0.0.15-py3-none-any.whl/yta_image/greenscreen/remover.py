"""
This module contains the methods to remove greenscreens
from images and transform them into transparent pixels.
"""
from yta_image.parser import ImageParser
from yta_image.color.picker import ColorPicker
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileType
from yta_general_utils.dataclasses import FileReturn
from typing import Union
from PIL import Image

import cv2
import numpy as np
import skimage.exposure


class ImageGreenscreenRemover:
    """
    Class to remove green pixels (greenscreens) from
    images and turn them into transparent pixels.
    """

    @staticmethod
    def remove_greenscreen_from_image_manually(
        image: Union[str, Image.Image, np.ndarray],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Greenscreen pixels obtained by region identification are removed
        manually and turned into transparent pixels to make a new image
        that has those regions as transparent.
        """
        image = ImageParser.to_pillow(image)

        green_rgb_color, similar_greens = ColorPicker.get_most_common_green_rgb_color_and_similars(image)
        green_pixels = [green_rgb_color] + similar_greens

        # Now we just replace green and similars with transparent pixel
        image = image.convert('RGBA')

        pixels = image.getdata()
        new_image_data = []
        for pixel in pixels:
            if pixel[:3] in green_pixels:
                new_image_data.append((pixel[0], pixel[1], pixel[2], 0))
            else:
                new_image_data.append((pixel[0], pixel[1], pixel[2], 255))

        image.putdata(new_image_data)

        if output_filename is not None:
            output_filename = Output.get_filename(output_filename, FileType.IMAGE)
            image.save(output_filename)

        return FileReturn(
            image,
            output_filename
        )

    @staticmethod
    def remove_greenscreen_from_image(
        image_filename: Union[str, cv2.typing.MatLike],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        This methods gets a greenscreen image (one with lots of uniform
        green pixels), does some modifications and replaces the green
        pixels with transparent pixels (due to alpha channel).

        # This is the best option as the green is well chosen.

        Thanks: https://stackoverflow.com/questions/51719472/remove-green-background-screen-from-image-using-opencv-python
        """
        # TODO: Improve this to be able to handle from
        # pillow and numpy image
        ParameterValidator.validate_mandatory_string('image_filename', image_filename, do_accept_empty = False)
        
        img = image_filename
        if PythonValidator.is_string(image_filename):
            # TODO: Implement 'file_is_image_file' when available (FileValidator.file_is_image_file)
            img = cv2.imread(image_filename)

        # TODO: This is not working, it raises
        # TypeError: Subscripted generics cannot be used with class and instance checks
        # if not variable_is_type(img, cv2.typing.MatLike):
        #     # TODO: Raise Exception
        #     return None

        # 1. Perform a basic masking
        # Convert the image to LAB space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        # Threshold the alpha channel to isolate green background
        a_channel = lab[:, :, 1]
        th = cv2.threshold(a_channel, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Mask the original image with binary mask
        masked = cv2.bitwise_and(img, img, mask = th)    # contains dark background
        m1 = masked.copy()
        m1[th == 0] = (255, 255, 255)                    # contains white background

        # 2. Remove green shade along the border
        # Convert masked image to LAB space
        mlab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)

        # Normalize the alph achannel mlab[:, :, 1] to use the 
        # entire intensity range between [0 - 255]
        dst = cv2.normalize(mlab[:, :, 1], dst = None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)

        # Green color represents the lower end of the range [0-255] 
        # while red color represents the higher end in the a-channel
        threshold_value = 100
        dst_th = cv2.threshold(dst, threshold_value, 255, cv2.THRESH_BINARY_INV)[1]

        # Set intensity value in the a-channel of the selected pixels to 127
        mlab[:, :, 1][dst_th == 255] = 127

        # Convert the image to BGRA and the pixels that were dark we 
        # transform to green but with max alpha to be transparent
        img2 = cv2.cvtColor(mlab, cv2.COLOR_LAB2BGR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2BGRA)
        # We add the alpha channel
        img2[th == 0] = (0, 255, 0, 0)

        if output_filename is not None:
            output_filename = Output.get_filename(output_filename, FileType.IMAGE)
            cv2.imwrite(output_filename, img2)

        # Check this, is interesting: https://stackoverflow.com/questions/44290606/alpha-masking-a-non-square-region-python-cv2
        return FileReturn(
            img,
            output_filename
        )
    
    @staticmethod
    def remove_greenscreen_from_image_with_blur(
        image_filename: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        This methods gets a greenscreen image (one with lots of uniform
        green pixels), does some modifications and replaces the green
        pixels with transparent pixels (due to alpha channel).

        The result is worse in the test cases than the 
        'remove_greenscreen_from_image' method.

        Thanks: https://stackoverflow.com/questions/51719472/remove-green-background-screen-from-image-using-opencv-python
        """
        # TODO: Improve this to be able to handle from
        # pillow and numpy image
        ParameterValidator.validate_mandatory_string('image_filename', image_filename, do_accept_empty = False)

        img = image_filename
        if PythonValidator.is_string(image_filename):
            # TODO: Implement 'file_is_image_file' when available (FileValidator.file_is_image_file)
            img = cv2.imread(image_filename)

        # TODO: This is not working, it raises
        # TypeError: Subscripted generics cannot be used with class and instance checks
        # if not variable_is_type(img, cv2.typing.MatLike):
        #     # TODO: Raise Exception
        #     return None

        # Convert to LAB
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        # Extract A channel
        A = lab[:, :, 1]

        # Threshold A channel
        thresh = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Blur threshold image
        blur = cv2.GaussianBlur(thresh, (0, 0), sigmaX = 5, sigmaY = 5, borderType = cv2.BORDER_DEFAULT)

        # Stretch so that 255 -> 255 and 127.5 -> 0
        mask = skimage.exposure.rescale_intensity(blur, in_range = (127.5, 255), out_range = (0, 255)).astype(np.uint8)

        # Add mask to image as alpha channel
        result = img.copy()
        result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask

        if output_filename is not None:
            output_filename = Output.get_filename(output_filename, FileType.IMAGE)
            cv2.imwrite(output_filename, result)

        return FileReturn(
            result,
            output_filename
        )