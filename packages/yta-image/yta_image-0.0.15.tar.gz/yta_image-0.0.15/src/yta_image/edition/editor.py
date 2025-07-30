"""
Image edition module.

Interesting links below:
- https://www.geeksforgeeks.org/image-enhancement-techniques-using-opencv-python/
- https://www.geeksforgeeks.org/changing-the-contrast-and-brightness-of-an-image-using-python-opencv/
"""
from yta_image.edition.settings import COLOR_TEMPERATURE_CHANGE_LIMIT, COLOR_HUE_CHANGE_LIMIT, CONTRAST_LIMIT, SHARPNESS_LIMIT, BRIGHTNESS_LIMIT
from yta_image.parser import ImageParser
from yta_validation.number import NumberValidator
from yta_file.handler import FileHandler
from yta_constants.enum import YTAEnum as Enum
from PIL import Image, ImageEnhance
from pillow_lut import load_cube_file
from typing import Union

import cv2
import numpy as np
import colorsys


class LutTable(Enum):
    """
    Image LUT tables definition to be able to handle them
    and apply to images to modify those images.

    You create a table in which you set the new values
    for all the 256 pixels so the previous 0 will be
    other number (or maybe 0 in that case).
    """

    INVERSE = 'inverse'
    SQUARE_ROOT = 'square_root'
    CUBE = 'cube'

    def get_lut_table(
        self
    ):
        """
        Obtain the LUT table array, which is a 2D table with 256
        indexes containing the pixel color in which the original
        color must be converted.
        """
        functions = {
            LutTable.INVERSE: lambda pixel: 255 - pixel,
            LutTable.SQUARE_ROOT: lambda pixel: (pixel * 255) ** (1 / 2),
            LutTable.CUBE: lambda pixel: (pixel ** 3) / (255 ** 2)
        }

        return np.array([
            functions[self](i)
            for i in range(256)
        ], dtype = np.uint8)
        
    def apply_to_image(
        self,
        image: any
    ) -> np.ndarray:
        """
        Apply the lut table to the provided image.

        Result is a numpy array in RGB format.
        """
        # We obtain a result in GBR format and we transform
        # it into an RGB
        return cv2.LUT(ImageParser.to_opencv(image), self.get_lut_table())[:, :, ::-1]
    
class ImageEditor:
    """
    Class to simplify and encapsulate all the functionality
    related to image edition.
    """
    
    @staticmethod
    def modify_color_temperature(
        image: Union[str, Image.Image, np.ndarray],
        factor: int = 0
    ):
        return change_image_color_temperature(image, factor)

    @staticmethod
    def modify_color_hue(
        image: Union[str, Image.Image, np.ndarray],
        factor: int = 0
    ):
        return change_image_color_hue(image, factor)
    
    @staticmethod
    def modify_brightness(
        image: Union[str, Image.Image, np.ndarray],
        factor: int = 0
    ):
        return change_image_brightness(image, factor)

    @staticmethod
    def modify_contrast(
        image: Union[str, Image.Image, np.ndarray],
        factor: int = 0
    ):
        return change_image_contrast(image, factor)
    
    @staticmethod
    def modify_sharpness(
        image: Union[str, Image.Image, np.ndarray],
        factor: int = 0
    ):
        return change_image_sharpness(image, factor)
    
    @staticmethod
    def modify_white_balance(
        image: Union[str, Image.Image, np.ndarray],
        factor: int = 0
    ):
        return change_image_white_balance(image, factor)
    
    @staticmethod
    def apply_lut(
        image: Union[str, Image.Image, np.ndarray],
        lut_table: LutTable
    ):
        """
        Apply the 2D Lut table provided in the 'lut_table'
        parameter to the also given 'image'.

        Thanks to:
        - https://gist.github.com/blroot/b22abc23526af2711d92cc3b3f13b907
        """
        lut_table = LutTable.to_enum(lut_table)

        return lut_table.apply_to_image(image)
    
    @staticmethod
    def apply_3d_lut(
        image: Union[str, Image.Image, np.ndarray],
        lut_3d_filename: str
    ):
        """
        Apply a 3D Lut table, which is loaded from the
        provided 'lut_3d_filename' .cube file, to the
        also given 'image'.

        Thanks to:
        - https://stackoverflow.com/questions/73341263/apply-3d-luts-cube-files-into-an-image-using-python
        """
        if not FileHandler.is_file(lut_3d_filename):
            raise Exception('The "lut_3d_filename" provided is not a valid file.')
        # TODO: Improve the validation to check that is .cube
        
        return ImageParser.to_pillow(image).filter(load_cube_file(lut_3d_filename))

def change_image_color_temperature(
    image: any,
    factor: int = 0
) -> np.ndarray:
    """
    Change the 'image' color temperature by the
    provided 'factor', that must be a value between
    [-50, 50].

    The color change consist of updating the red and
    blue values, where red is calid and blue is cold.
    Increasing the temperature means increasing the
    red color, and decreasing it, decreasing the blue
    color.
    """
    if not NumberValidator.is_number_between(factor, COLOR_TEMPERATURE_CHANGE_LIMIT[0], COLOR_TEMPERATURE_CHANGE_LIMIT[1]):
        raise Exception(f'The "factor" parameter provided is not a number between [{COLOR_TEMPERATURE_CHANGE_LIMIT[0]}, {COLOR_TEMPERATURE_CHANGE_LIMIT[1]}].')
    
    # The '.copy()' makes it writeable
    image = ImageParser.to_numpy(image).copy()

    if factor == 0:
        return image

    # We want the factor being actually a value between 0.50 and 1.50,
    # but multiplying by 1.5 is equal to divide by 0.75 so I need to
    # manually do this calculation to apply the formula correctly
    factor = 1 - (0.25 - normalize(factor, COLOR_TEMPERATURE_CHANGE_LIMIT[0], 0, 0, 0.25)) if factor < 0 else 1 + normalize(factor, 0, COLOR_TEMPERATURE_CHANGE_LIMIT[1], 0, 0.5)
    
    r, b = image[:, :, 0], image[:, :, 2]
    
    # Min and max values are 0 and 255
    r = np.clip(r * factor, 0, 255)
    b = np.clip(b / factor, 0, 255)
    
    # Reconstruimos la imagen con los canales modificados
    image[:, :, 0] = r
    image[:, :, 2] = b

    return image

# These below are 2 functions to convert
# TODO: Please, move these functions to a method
# maybe in 'yta_general_utils' or in 'yta_multimedia'
rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def change_image_color_hue(
    image: any,
    factor: int = 0
) -> np.ndarray:
    """
    Change the 'image' color hue by the provided
    'factor', that must be a value between [-50, 50].

    Colorize PIL image `original` with the given
    `factor` (hue within 0-360); returns another PIL image.
    """
    # TODO: This method is not working
    if not NumberValidator.is_number_between(factor, COLOR_HUE_CHANGE_LIMIT[0], COLOR_HUE_CHANGE_LIMIT[1]):
        raise Exception(f'The "factor" parameter provided is not a number between [{COLOR_HUE_CHANGE_LIMIT[0]}, {COLOR_HUE_CHANGE_LIMIT[1]}].')
    
    # The '.copy()' makes it writeable
    image = ImageParser.to_numpy(image).copy()

    factor = normalize(factor, COLOR_HUE_CHANGE_LIMIT[0], COLOR_HUE_CHANGE_LIMIT[1], 0, 360)
    
    # TODO: This code is not working well
    # TODO: This method is very very slow
    #arr = np.array(np.asarray(img).astype('float'))
    #r, g, b, a = np.rollaxis(image, axis = -1)
    print(image.size) # size is 6220800
    r, g, b = np.rollaxis(image, axis = -1)
    #r, g, b = np.moveaxis(image, -1, 0)
    h, s, v = rgb_to_hsv(r, g, b)
    h = factor / 360.0
    r, g, b = hsv_to_rgb(h, s, v)
    #arr = np.dstack((r, g, b, a))
    arr = np.dstack((r, g, b)).astype(np.uint8)
    print(arr.size) # size is 220800
    print(arr)

    # TODO: I don't like this line below
    return arr
    return Image.fromarray(arr.astype('uint8'), 'RGBA')

def change_image_brightness(
    image: any,
    factor: int = 0
) -> np.ndarray:
    """
    Change the 'image' brightness by the provided
    'factor', that must be a value between [-100, 100].
    """
    image = ImageParser.to_pillow(image).copy()

    # TODO: Check factor is between the limit
    if not NumberValidator.is_number_between(factor, BRIGHTNESS_LIMIT[0], BRIGHTNESS_LIMIT[1]):
        raise Exception(f'The provided factor must be a number between [{BRIGHTNESS_LIMIT[0]}, {BRIGHTNESS_LIMIT[1]}].')

    # factor from -100 to 0 must be from 0.5 to 1
    # factor from 0 to 100 must be from 1 to 2
    factor = normalize(factor, BRIGHTNESS_LIMIT[0], 0, 0.5, 1.0) if factor <= 0 else normalize(factor, 0, BRIGHTNESS_LIMIT[1], 1.0, 2.0)

    image = ImageEnhance.Brightness(image).enhance(factor)

    return ImageParser.to_numpy(image)

def change_image_contrast(
    image: any,
    factor: int = 0
) -> np.ndarray:
    """
    Change the 'image' contrast by the provided
    'factor', that must be a value between [-100, 100].
    """
    image = ImageParser.to_pillow(image).copy()

    # TODO: Check factor is between the limit
    if not NumberValidator.is_number_between(factor, CONTRAST_LIMIT[0], CONTRAST_LIMIT[1]):
        raise Exception(f'The provided factor must be a number between [{CONTRAST_LIMIT[0]}, {CONTRAST_LIMIT[1]}].')

    # factor from -100 to 0 must be from 0.5 to 1
    # factor from 0 to 100 must be from 1 to 2
    factor = normalize(factor, CONTRAST_LIMIT[0], 0, 0.5, 1.0) if factor <= 0 else normalize(factor, 0, CONTRAST_LIMIT[1], 1.0, 2.0)

    image = ImageEnhance.Contrast(image).enhance(factor)

    return ImageParser.to_numpy(image)

def change_image_sharpness(
    image: any,
    factor: int = 0
) -> np.ndarray:
    """
    Change the 'image' sharpness by the provided
    'factor', that must be a value between [-100, 100].

    A factor of -100 gives you a blurred image while
    a factor of 100 gives you a sharped image.
    """
    image = ImageParser.to_pillow(image).copy()

    # TODO: Check factor is between the limit
    if not NumberValidator.is_number_between(factor, SHARPNESS_LIMIT[0], SHARPNESS_LIMIT[1]):
        raise Exception(f'The provided factor must be a number between [{SHARPNESS_LIMIT[0]}, {SHARPNESS_LIMIT[1]}].')

    
    # factor from -100 to 0 must be from 0.5 to 1
    # factor from 0 to 100 must be from 1 to 2
    factor = normalize(factor, SHARPNESS_LIMIT[0], 0, 0.0, 1.0) if factor <= 0 else normalize(factor, 0, SHARPNESS_LIMIT[1], 1.0, 2.0)

    image = ImageEnhance.Sharpness(image).enhance(factor)

    return ImageParser.to_numpy(image)

def change_image_white_balance(
    image: any,
    factor: int = 0
) -> np.ndarray:
    """
    TODO: Explain
    
    The result is in RGB format.
    """
    # TODO: I'm not using the 'factor'
    # TODO: I have a factor limit setting for this
    
    # TODO: Apply factor -> 0.0 means no change
    image = ImageParser.to_opencv(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # Average of green channel
    avg_a = np.average(image[:, :, 1])
    # Average of red channel
    avg_b = np.average(image[:, :, 2])
    image[:, :, 1] = image[:, :, 1] - ((avg_a - 128) * (image[:, :, 0] / 255.0) * 1.2)
    image[:, :, 2] = image[:, :, 2] - ((avg_b - 128) * (image[:, :, 0] / 255.0) * 1.2)

    balanced_image = cv2.cvtColor(image, cv2.COLOR_LAB2RGB)

    return balanced_image

# TODO: I have a new ValueNormalizer class to handle normalization
# so this has to be avoided and use that general function instead
def normalize(
    number: float,
    input_lower_limit: float,
    input_upper_limit: float,
    output_lower_limit: float = 0.0,
    output_upper_limit: float = 1.0
):
    """
    Normalize the 'number' value to be between 'output_lower_limit'
    and 'output_upper_limit', according to the input provided, that
    is between the 'input_lower_limit' and 'input_upper_limit' 
    values.
    """
    if not NumberValidator.is_number(number) or not NumberValidator.is_number(input_lower_limit) or not NumberValidator.is_number(input_upper_limit) or not NumberValidator.is_number(output_lower_limit) or not NumberValidator.is_number(output_upper_limit):
        raise Exception('All the parameters must be numbers.')

    if not NumberValidator.is_number_between(number, input_lower_limit, input_upper_limit):
        raise Exception('The "number" parameter provided is not a number between the input limits provided.')
    
    if input_upper_limit <= input_lower_limit or output_upper_limit <= output_lower_limit:
        raise Exception('The upper limit must be greater than the lower limit.')
    
    return (number - input_lower_limit) / (input_upper_limit - input_lower_limit) * (output_upper_limit - output_lower_limit) + output_lower_limit