from yta_image.parser import ImageParser
from yta_temp import Temp
from yta_validation import PythonValidator
# TODO: I should avoid using this FileReturn
from yta_general_utils.dataclasses import FileReturn
from yta_programming.output import Output
from yta_constants.file import FileType
from PIL import Image
from typing import Union
from subprocess import run

import numpy as np


class ImageBackgroundRemover:
    """
    Class to remove backgrounds from images.
    """

    @staticmethod
    def remove_background(
        image: Union[str, Image.Image, np.ndarray],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Remove the background of the provided 'image'. This
        method returns the image as a pillow image in the
        first element, and the created image filename as the
        second element.
        """
        image_filename = image

        # If provided image is not a file, we store it
        # to be able to handle
        if not PythonValidator.is_string(image):
            image_filename = Temp.get_wip_filename('background_to_remove.png')
            ImageParser.to_pillow(image).save(image_filename)

        output_filename = Output.get_filename(output_filename, FileType.IMAGE)

        run([
            'backgroundremover',
            '-i',
            image_filename,
            '-o',
            output_filename
        ])

        return FileReturn(
            ImageParser.to_pillow(output_filename),
            output_filename
        )
    
    """
    # Problem with Circular import
    from backgroundremover.bg import remove as remove_background
    r = lambda image_filename: image_filename.buffer.read() if hasattr(image_filename, "buffer") else image_filename.read()
    w = lambda o, data: o.buffer.write(data) if hasattr(o, "buffer") else o.write(data)

    # These below are default values
    x = remove_background(
        r(image_filename),
        model_name = 'u2net',
        alpha_matting = False,
        alpha_matting_foreground_threshold = 240,
        alpha_matting_background_threshold = 10,
        alpha_matting_erode_structure_size = 10,
        alpha_matting_base_size = 1000
    )
    w(output_filename, x)
    """

    # TODO: This below seems to work (as shown in this 
    # commit https://github.com/nadermx/backgroundremover/commit/c590858de4c7e75805af9b8ecdd22baf03a1368f)
    """
    from backgroundremover.bg import remove
    def remove_bg(src_img_path, out_img_path):
        model_choices = ["u2net", "u2net_human_seg", "u2netp"]
        f = open(src_img_path, "rb")
        data = f.read()
        img = remove(data, model_name=model_choices[0],
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_structure_size=10,
                    alpha_matting_base_size=1000)
        f.close()
        f = open(out_img_path, "wb")
        f.write(img)
        f.close()
    """