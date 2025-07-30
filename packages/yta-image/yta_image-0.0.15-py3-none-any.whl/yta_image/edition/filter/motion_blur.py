"""
Thanks for the inspiration:
https://www.geeksforgeeks.org/opencv-motion-blur-in-python/
"""
from yta_image.parser import ImageParser
from yta_image.converter import ImageConverter
from yta_constants.enum import YTAEnum as Enum
from yta_programming.output import Output
from yta_constants.file import FileType
from yta_general_utils.dataclasses import FileReturn
from typing import Union

import cv2 
import numpy as np 


class MotionBlurDirection(Enum):
    """
    The direction we want to apply on the
    Motion Blur effect.
    """
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    DIAGONAL_TOP_RIGHT = 'diagonal_top_right'
    DIAGONAL_TOP_LEFT = 'diagonal_top_left'

def apply_motion_blur(
    image: any,
    kernel_size: int = 30,
    direction: MotionBlurDirection = MotionBlurDirection.HORIZONTAL,
    output_filename: Union[str, None] = None
):
    """
    Apply a motion blur effect on the given 'image'
    using the provided 'kernel_size' (the greater
    this value is, the more motion blur effect we
    will get on the image). The motion blur can be
    applied in one 'direction', and the result image
    can be stored locally if 'output_filename' is
    provided.
    """
    direction = MotionBlurDirection.to_enum(direction)

    # TODO: 'image' param type must be refactored
    image = ImageConverter.numpy_image_to_opencv(ImageParser.to_numpy(image))
    
    kernel = np.zeros((kernel_size, kernel_size)) 

    if direction == MotionBlurDirection.HORIZONTAL:
        kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size) 
    elif direction == MotionBlurDirection.VERTICAL:
        kernel[:, int((kernel_size - 1) / 2)] = np.ones(kernel_size) 
    elif direction == MotionBlurDirection.DIAGONAL_TOP_LEFT:
        np.fill_diagonal(kernel, 1)
    elif direction == MotionBlurDirection.DIAGONAL_TOP_RIGHT:
        np.fill_diagonal(np.fliplr(kernel), 1)
    
    # Normalize and apply
    kernel /= kernel_size
    image = cv2.filter2D(image, -1, kernel) 

    # TODO: Refactor this please
    if output_filename is not None:
        output_filename = Output.get_filename(output_filename, FileType.IMAGE)
        cv2.imwrite(output_filename, image)

    return FileReturn(
        ImageConverter.opencv_image_to_numpy(image),
        output_filename
    )

# TODO: Maybe this method has to be moved to 
# video handling
def get_progressive_kernel_sizes(
    steps: int,
    max: int
):
    """
    Return an incremental array of 'steps' kernel sizes
    from 0 (excluded) to the provided 'max' value.
    
    This method is useful to apply an incremental effect.

    If steps = 20 and max = 100, it will return:
    [5, 10, 15, ..., 95, 100] (20 elements)
    """
    return np.linspace(0, max, steps + 1, endpoint = True, dtype = int)[1:]

