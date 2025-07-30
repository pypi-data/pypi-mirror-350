from yta_image.mask.presets import ImageMaskPreset
from yta_image.parser import ImageParser
from yta_validation import PythonValidator
from PIL import Image
from typing import Union

import numpy as np
import cv2


class ImageMask:
    """
    Class to encapsulate and simplify the functionality
    related to image masking.
    """

    @staticmethod
    def apply_mask_preset(
        image: Union[str, Image.Image, np.ndarray],
        mask_preset: ImageMaskPreset,
        output_filename: Union[str, None] = None
    ):
        """
        Apply the provided 'mask' to the given 'image'.

        This method return the result image as a ndim = 4 numpy
        array of not normalized values between 0 and 255, even
        the alpha channel.
        """
        if not PythonValidator.is_subclass(mask_preset, ImageMaskPreset):
            raise Exception('The provided "mask_preset" parameter is not a valid ImageMaskPreset class instance.')

        image = ImageParser.to_numpy(image, mode = 'RGB')

        # Obtain mask as ndim = 1 where black is transparent
        mask = ImageParser.to_numpy(mask_preset.apply_on(image))[:, :, 1]
        
        # Add the mask to the Pillow Image
        image = np.dstack((image, mask))

        if output_filename is not None:
            # TODO: Apply 'output' handler
            cv2.imwrite(output_filename, image)

        # TODO: Maybe convert to pillow?

        return image