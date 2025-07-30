"""
Welcome to Youtube Autonomous Image Module.
"""
from yta_image.parser import ImageParser
from yta_image.converter import ImageConverter
from yta_image.edition.filter import ImageFilter
from yta_image.edition.filter.motion_blur import MotionBlurDirection
from yta_image.description.descriptor import DefaultImageDescriptor
from yta_image.region.finder import ImageRegionFinder
from yta_image.size import ImageResizer
from yta_image.background import ImageBackgroundRemover
from yta_image.edition.editor import ImageEditor
from PIL import Image as PillowImage
from typing import Union


class _Filter:
    """
    Class to simplify the access to our filters 
    for our custom Image class. This class must
    be used in our custom Image class.
    """

    image: any
    """
    Instance of our custom Image class to simplify
    the way we applicate filters.
    """

    def __init__(
        self,
        image: 'Image'
    ):
        # TODO: Maybe receive the Pillow image instead (?)
        self.image = image.image

    def pixelate(
        self,
        pixel_size: int,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.pixelate(self.image, pixel_size, output_filename)

    def motion_blur(
        self,
        kernel_size: int = 30,
        direction: MotionBlurDirection = MotionBlurDirection.HORIZONTAL,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.motion_blur(self.image, kernel_size, direction, output_filename)
    
class _Transform:
    """
    Class to simplify the access to our image
    transformations for our custom Image class.
    This class must be used in our custom Image
    class.
    """

    image: any
    """
    Instance of our custom Image class to simplify
    the way we applicate transformations.
    """

    def __init__(
        self,
        image: 'Image'
    ):
        # TODO: Maybe receive the Pillow image instead (?)
        self.image = image.image

    def to_gameboy(
        self,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.to_gameboy(self.image, output_filename)
    
    def to_sticker(
        self,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.to_sticker(self.image, output_filename)

class _Color:
    """
    Class to simplify the access to our image
    color changes for our custom Image class.
    This class must be used in our custom Image
    class.
    """

    image: any
    """
    Instance of our custom Image class to simplify
    the way we applicate color changes.
    """

    def __init__(
        self,
        image: 'Image'
    ):
        # TODO: Maybe receive the Pillow image instead (?)
        self.image = image.image

    # TODO: Talk about limits (yta_image\edition\settings.py)
    def set_temperature(
        self,
        factor: int = 0
    ):
        return ImageEditor.modify_color_temperature(self.image, factor)

    def set_contrast(
        self,
        factor: int = 0
    ):
        return ImageEditor.modify_contrast(self.image, factor)
    
    def set_brightness(
        self,
        factor: int = 0
    ):
        return ImageEditor.modify_brightness(self.image, factor)
    
    def set_sharpness(
        self,
        factor: int = 0
    ):
        return ImageEditor.modify_sharpness(self.image, factor)

    def set_white_balance(
        self,
        factor: int = 0
    ):
        return ImageEditor.modify_white_balance(self.image, factor)
    
    def set_color_hue(
        self,
        factor: int = 0
    ):
        return ImageEditor.modify_color_hue(self.image, factor)

class Image:
    """
    Class to wrap images and make easier the way we
    work with them.
    """

    image: PillowImage.Image
    """
    The image but stored as a Pillow image.
    """
    filter: _Filter
    """
    A shortcut to the available filters. The filters,
    once they are applied, return a new image. The
    original image remains unchanged.
    """
    transform: _Transform
    """
    A shortcut to the available transformations. The
    transformations, once they are applied, return a
    new image. The original image remains unchanged.
    """
    color: _Color
    """
    A shortcut to the available color changes. The
    color changes, once they are applied, return a new
    image. The original image remains unchanged.
    """
    _description: str
    """
    A description of the image, given by an engine that
    has been trained to describe images.
    """
    _green_regions: any
    """
    The green regions that have been found in the image.
    """
    _alpha_regions: any
    """
    The alpha (transparent) regions that have been found
    in the image.
    """

    @property
    def as_pillow(
        self
    ) -> PillowImage.Image:
        return self.image
    
    @property
    def as_numpy(
        self
    ) -> 'np.ndarray':
        return ImageConverter.pil_image_to_numpy(self.image)
    
    @property
    def as_opencv(
        self
    ) -> 'np.ndarray':
        return ImageConverter.pil_image_to_opencv(self.image)
    
    @property
    def as_base64(
        self
    ) -> str:
        return ImageConverter.pil_image_to_base64(self.image)
    
    # TODO: Add other libraries to be able to transform
    @property
    def description(
        self
    ) -> str:
        """
        A description of the image, given by an engine that
        has been trained to describe images.
        """
        if not hasattr(self, '_description'):
            self._description = DefaultImageDescriptor().describe(self.image)

        return self._description
    
    @property
    def green_regions(
        self
    ):
        """
        The green regions that have been found in the image.
        """
        if not hasattr(self, '_green_regions'):
            self._green_regions = ImageRegionFinder.find_green_regions(self.image)

        return self._green_regions
    
    @property
    def alpha_regions(
        self
    ):
        """
        The alpha (transparent) regions that have been found
        in the image.
        """
        if not hasattr(self, '_alpha_regions'):
            self._alpha_regions = ImageRegionFinder.find_transparent_regions(self.image)

        return self._alpha_regions

    def __init__(
        self,
        image: Union[
            str,
            'np.ndarray',
            PillowImage.Image
        ]
    ):
        self.image = ImageParser.to_pillow(image)
        self.filter = _Filter(self)
        self.transform = _Transform(self)
        self.color = _Color(self)

    def resize(
        self,
        size: tuple,
        output_filename: Union[str, None] = None
    ):
        """
        This method returns the image modified but
        does not modify the original image.
        """
        return ImageResizer.resize(self.image, size, output_filename).file_converted
    
    def remove_background(
        self,
        output_filename: Union[str, None] = None
    ):
        return ImageBackgroundRemover.remove_background(self.image, output_filename).file_converted

# TODO: Maybe I want to update the self.image when
# I modify something so I return a new Image
# instance with that modified image, so if you do
# image = image.filters.pixelate(10) you will update
# your image instance, but if you do
# n_image = image.filters.pixelate(10) you will get
# a new instance in n_image