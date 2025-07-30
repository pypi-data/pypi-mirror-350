from yta_image.converter import ImageConverter
from yta_file.handler import FileHandler
from yta_general_utils.file.filename import filename_is_type
from yta_general_utils.file.enums import FileType
from yta_validation import PythonValidator
from PIL import Image
from typing import Union

import numpy as np


class ImageParser:
    """
    Class to simplify the way we handle the image parameters
    so we can parse them as Pillow images, as numpy arrays,
    etc.
    """

    @staticmethod
    def to_pillow(
        image: Union[str, Image.Image, np.ndarray],
        mode: str = 'RGB'
    ) -> Image.Image:
        """
        Returns an instance of a Pillow Image.Image of the given
        'image' if it is a valid image and no error found.

        Result is a Pillow image which is in RGB (or RGBA) format.
        """
        # TODO: By now we are only accepting string filenames,
        # Pillow Image.Image instances and numpy arrays.
        if image is None:
            raise Exception('No "image" parameter provided.')
        
        if (
            not PythonValidator.is_string(image) and
            not PythonValidator.is_numpy_array(image) and
            not PythonValidator.is_instance(image, Image.Image)
        ):
            raise Exception('The "image" parameter provided is not a string nor a Image.Image nor a np.ndarray.')

        mode = (
            'RGB'
            if not mode else
            mode
        )

        if mode not in ['RGB', 'RGBA']:
            raise Exception('The provided "mode" parameters is not a valid mode: RGB or RGBA.')

        # We can have problems with np.ndarray
        if PythonValidator.is_numpy_array(image):
            image = ImageConverter.numpy_image_to_pil(image)
        elif PythonValidator.is_string(image):
            if not filename_is_type(image, FileType.IMAGE):
                raise Exception('The "image" parameter provided is not a valid image filename.')
            
            if not FileHandler.is_image_file(image):
                raise Exception('The "image" parameter provided is not a valid image.')
            
            image = Image.open(image)

        return image.convert(mode)
    
    @staticmethod
    def to_numpy(
        image: Union[str, Image.Image, np.ndarray],
        mode: str = 'RGB'
    ) -> np.ndarray:
        """
        Returns a numpy array representing the given 'image'
        if it is a valid image and no error found.

        The 'mode' parameter will be used to open the image
        with Pillow library and then turning into numpy when
        necessary. Must be 'RGB' or 'RGBA'.

        Result is in RGB or RGBA format.
        """
        # TODO: By now we are only accepting string filenames,
        # Pillow Image.Image instances and numpy arrays.
        if image is None:
            raise Exception('No "image" parameter provided.')
        
        if not PythonValidator.is_instance(image, [str, Image.Image, np.ndarray]):
            raise Exception('The "image" parameter provided is not a string nor a Image.Image nor a np.ndarray.')
        
        mode = 'RGB' if not mode else mode

        if mode not in ['RGB', 'RGBA']:
            raise Exception('The provided "mode" parameters is not a valid mode: RGB or RGBA.')

        # We can have problems with np.ndarray
        if PythonValidator.is_instance(image, Image.Image):
            image = ImageConverter.pil_image_to_numpy(image.convert(mode))
        elif PythonValidator.is_string(image):
            if not filename_is_type(image, FileType.IMAGE):
                raise Exception('The "image" parameter provided is not a valid image filename.')
            
            if not FileHandler.is_image_file(image):
                raise Exception('The "image" parameter provided is not a valid image.')
            
            image = ImageConverter.pil_image_to_numpy(Image.open(image).convert(mode))
        elif PythonValidator.is_numpy_array(image):
            if image.shape[2] == 3 and mode == 'RGBA':
                # numpy but RGB to RGBA
                image = np.dstack((image, np.ones((image.shape[0], image.shape[1]), dtype = np.uint8) * 255))
                # Moviepy uses the alpha channel as 0 or 1, not as 255
                # but this is only an image parser not a moviepy parser
                #image = np.dstack((image, np.ones((image.shape[0], image.shape[1]), dtype = np.uint8)))
            elif image.shape[2] == 4 and mode == 'RGB':
                # numpy but RGBA to RGB
                image = image[:, :, :3]

        return image
    
    @staticmethod
    def to_opencv(
        image: Union[str, Image.Image, np.ndarray],
        mode: str = 'RGB'
    ) -> np.ndarray:
        """
        The 'image' is read as a RGB numpy array and then
        transformed into an BGR numpy array because Opencv
        uses BGR format.

        Result is in BGR format.
        """
        return ImageParser.to_numpy(image, mode)[:, :, ::-1]