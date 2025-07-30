"""
AI Image generation file that contains the classes
capable to generate AI images. These classes will
raise Exceptions if the parameters are not provided
and will use internal functionality to do it.

Programmer help: The classes implement parameter
validation and raise exceptions, but the other files
from which other methods are imported do not 
implement them, so make sure you pass the right
and expected parameters. This should be the ideal
structure to keep in code, but you know... I write
code very fast so I can't go back and review and
refactor code often... So sorry about that :P
"""
from yta_ai.prodia import Prodia
from yta_ai.pollinations import Pollinations
from yta_general_utils.dataclasses import FileReturn
from yta_constants.file import FileType
from yta_programming.output import Output
from yta_validation import PythonValidator
from abc import ABC, abstractmethod
from typing import Union


class AIImageGenerator(ABC):
    """
    Abstract class to be inherited by any specific
    AI image generator.
    """

    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Generate an image with the given 'prompt' and
        store it locally if 'output_filename' is 
        provided.
        """
        pass

class DefaultImageGenerator(AIImageGenerator):
    """
    Default AI image generator. Useful when you don't
    know which engine you should use. We have choosen
    one that is a good choice for a general context.
    """

    def generate_image(
        self,
        prompt: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Generate an AI image and return 2 values, the
        image read with pillow and the final output
        filename used to store the image locally.
        """
        return ProdiaAIImageGenerator().generate_image(prompt, output_filename)

class ProdiaAIImageGenerator(AIImageGenerator):
    """
    Prodia AI image generator.
    """

    def generate_image(
        self,
        prompt: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Generate an AI image and return 2 values, the
        image read with pillow and the final output
        filename used to store the image locally.
        """
        if not PythonValidator.is_string(prompt):
            raise Exception('Provided "prompt" parameter is not a valid prompt.')

        output_filename = Output.get_filename(output_filename, FileType.IMAGE)
        
        return Prodia.generate_image(prompt, output_filename)
    
class PollinationsAIImageGenerator(AIImageGenerator):
    """
    Pollinations AI image generator.

    This is using the Pollinations platform wich
    contains an AI image generator API and 
    open-source model.

    Source: https://pollinations.ai/
    """

    def generate_image(
        self,
        prompt: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Generate an image with the Pollinations AI image
        generation model using the provided 'prompt' and
        stores it locally as 'output_filename'.
        """
        if not PythonValidator.is_string(prompt):
            raise Exception('Provided "prompt" parameter is not a valid prompt.')

        output_filename = Output.get_filename(output_filename, FileType.IMAGE)
        
        return Pollinations.generate_image(prompt, output_filename)