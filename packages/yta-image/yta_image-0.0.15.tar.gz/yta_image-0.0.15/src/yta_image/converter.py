from yta_validation import PythonValidator
from PIL import Image
from io import BytesIO

import numpy as np
import base64
import cv2


class ImageConverter:
    """
    Class to encapsulate and simplify the image
    conversion methods.
    """

    @staticmethod
    def numpy_image_to_pil(
        image: np.ndarray
    ):
        """
        This method checks if the provided 'image' is a numpy array and if its
        values are in the [0, 255] range or in the [0, 1] (normalized) range.
        It will raise an Exception if any of those conditions are not
        satisfied.

        This method will return the image converted into a Pillow image.
        """
        validate_numpy_image(image)

        return (
            # TODO: How do I know if the values are normalized or just [0, 255]
            # but with values below 1 (?)
            Image.fromarray((image * 255).astype(np.uint8))
            if np.all((image >= 0) & (image <= 1)) else
            Image.fromarray((image).astype(np.uint8))
        )
    
    @staticmethod
    def numpy_image_to_base64(
        image: np.ndarray
    ):
        """
        Turns the provided numpy 'image' into a base64 str image.
        """
        validate_numpy_image(image)

        buffer = BytesIO()
        image = ImageConverter.numpy_image_to_pil(image).save(buffer, format = 'PNG')
        buffer.seek(0)
        image_bytes = buffer.read()

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_base64_str = f'data:image/png;base64,{image_base64}'

        return image_base64_str
    
    @staticmethod
    def numpy_image_to_opencv(
        image: np.ndarray
    ):
        validate_numpy_image(image)
    
        # This is also a way:
        # pil_data = PIL.Image.open('Image.jpg').convert('RGB')
        # image = numpy.array(pil_data)[:, :, ::-1].copy()

        # I need to know if image is RGB or RGBA
        return (
            cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if image.ndim == 3 and image.shape[2] == 3 else # RGB
            cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
            if image.ndim == 2 and image.shape[2] == 4 else # RGBA 
            None # TODO: Maybe raise an Exception (?)
        )
    
    @staticmethod
    def pil_image_to_numpy(
        image: Image.Image
    ):
        """
        Turns the 'image' to a numpy array. The PIL image must be an
        array produced by the code 'Image.open(image_filename)'.
        """
        validate_pillow_image(image)

        # This will return it as RGB if (4, 4, 3) or as RGBA if (4, 4, 4)
        return np.asarray(image)
    
    @staticmethod
    def pil_image_to_base64(
        image: Image.Image
    ):
        """
        Turns the 'image' to a base64 image by turning it into a numpy
        image first. The PIL image must be an array produced by the code
        'Image.open(image_filename)'.
        """
        validate_pillow_image(image)

        return ImageConverter.numpy_image_to_base64(ImageConverter.pil_image_to_numpy(image))

    @staticmethod
    def pil_image_to_opencv(
        image: Image.Image
    ):
        """
        Turns the 'image' to a opencv image by turning it into a numpy
        image first. The PIL image must be an array produced by the code
        'Image.open(image_filename)'.
        """
        validate_pillow_image(image)

        return ImageConverter.numpy_image_to_opencv(ImageConverter.pil_image_to_numpy(image))
    
    @staticmethod
    def base64_image_to_pil(
        image
    ):
        """
        Turns the 'image' to a PIL Image, to be able
        to work with, and returns it.
        """
        validate_base64_image(image)

        return Image.open(BytesIO(base64.b64decode(image)))
    
    @staticmethod
    def base64_image_to_numpy(
        image
    ):
        """
        Turns the 'image' to a numpy image (np.ndarray),
        to be able to work with, and returns it. 
        """
        validate_base64_image(image)
        
        return ImageConverter.pil_image_to_numpy(ImageConverter.base64_image_to_pil(image))
    
    @staticmethod
    def base64_image_to_opencv(
        image
    ):
        """
        Turns the 'image' to an opencv image by turning it
        into a numpy array first.
        """
        validate_base64_image(image)

        return ImageConverter.pil_image_to_base64(ImageConverter.base64_image_to_pil)

    @staticmethod
    def opencv_image_to_numpy(
        image: np.ndarray
    ):
        """
        Turns the 'image' to an opencv image by turning it
        into a numpy array first.
        """
        validate_opencv_image(image)

        # An opencv image is just a numpy array with a meta param

        # I need to know if image is RGB or RGBA
        return (
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if image.ndim == 3 and image.shape[2] == 3 else # RGB
            cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            if image.ndim == 2 and image.shape[2] == 4 else # RGBA
            None # TODO: Maybe raise an Exception (?)
        )

    @staticmethod
    def opencv_image_to_pillow(
        image: np.ndarray
    ):
        """
        Turns the 'image' to a pillow image by turning it
        into a numpy array first.
        """
        validate_opencv_image(image)

        return ImageConverter.numpy_image_to_pil(ImageConverter.opencv_image_to_numpy(image))
    
    @staticmethod
    def opencv_image_to_base64(
        image: np.ndarray
    ):
        """
        Turns the 'image' to a base64 image by turning it
        into a numpy array first.
        """
        validate_opencv_image(image)

        return ImageConverter.numpy_image_to_base64(ImageConverter.opencv_image_to_numpy(image))
    
    # TODO: Move this below to another file as it is
    # not a conversion but a checking
    @staticmethod
    def is_base64_image(
        image: str
    ):
        """
        Check if the provided 'image' is a base64 image,
        the type of images that can be received from a
        server during a request.
        """
        is_valid = False

        if image_can_be_base64(image):
            base64_string = image.split(';base64,')[1]
            try:
                base64.b64decode(base64_string, validate = True)
                is_valid = True
            except Exception:
                pass

        return is_valid
    
def validate_numpy_image(image: np.ndarray):
    """
    This method checks if the provided 'image' is
    a numpy array, that the array has 3 or 4
    elements in each cell and if its values are in the 
    [0, 255] range or in the [0, 1] (normalized) range.
    It will raise an Exception if any of those
    conditions are not satisfied.
    """
    if not PythonValidator.is_numpy_array(image):
        raise Exception('The provided "image" parameter is not a numpy np.ndarray instance.')
    
    if image.ndim != 3 or image.shape[2] not in [3, 4]:
        raise Exception('The provided "image" parameter does not represent a RGB or RGBA image.')

    if not np.all((image >= 0) & (image <= 255)):
        raise Exception('The provided numpy array is not a valid image as its values are not between 0 and 255.')

    # TODO: What about '.astype('uint8')', maybe we can check if it is that type (?)

def validate_opencv_image(image: np.ndarray):
    """
    This method checks if the provided 'image' is a
    numpy array, that the array has 3 or 4 elements
    on each cell and if its values are in the [0, 255]
    range or in the [0, 1] (normalized) range. It will
    raise an Exception if any of those conditions are
    not satisfied.

    An opencv image is just a numpy array with some
    meta param.
    """
    # The only thing that could change is the message and I don't want
    # to duplicate code for a single 'opencv' word in a message
    return validate_numpy_image(image)

def validate_base64_image(image: str):
    """
    This method validates if the provided image is
    a valid base64 image by getting the prefix, the
    'base64' str and also trying to decode it. It
    will raise an Exception if the image is not a
    valid base64 image.
    """
    if not ImageConverter.is_base64_image(image):
        raise Exception('The provided "image" parameter is not a valid base64 image.')

def validate_pillow_image(image: Image.Image):
    if not PythonValidator.is_instance(image, Image.Image):
        raise Exception('The provided "image" is not an instance of a Pillow image.')
    
    if image.mode not in ['RGB', 'RGBA']:
        raise Exception('The provided pillow image is not in a valid mode for our software. Valid modes are: "RGB", "RGBA".')

def image_can_be_base64(image: str):
    """
    Check if the provided 'image' can be a base64
    image.
    """
    return (
        PythonValidator.is_string(image) and
        image.startswith('data:image/') and
        ';base64,' in image
    )
    