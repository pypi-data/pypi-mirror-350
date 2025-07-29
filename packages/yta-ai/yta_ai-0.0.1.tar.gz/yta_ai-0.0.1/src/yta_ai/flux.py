"""
Flux is an image generation software created by Blackforest Labs
(https://blackforestlabs.ai/). They have 3 different models and
2 of those are free-to-use.

Those models ('dev' and 'schnell') have been implemented here to
be used to generate images.

The HugginFace endpoints I've found when creating this file:
- https://huggingface.co/black-forest-labs/FLUX.1-schnell?inference_api=true
- https://huggingface.co/black-forest-labs/FLUX.1-dev?inference_api=true
"""
from yta_ai.hugginface import HugginFace
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileType
from typing import Union


SCHNELL_HUGGINFACE_ENDPOINT = 'https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell'
DEV_HUGGINFACE_ENDPOINT = 'https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev'

class Flux:
    """
    Class to wrap the image generation with 
    Flux engine.
    """

    @staticmethod
    def generate_dev(
        prompt: str,
        output_filename: Union[str, None] = None
    ):
        """
        Generates an image using the Flux 'dev' model, through the 
        HugginFace endpoint, and returns it read as PIL image. If
        'output_filename' provided, it will be also stored locally
        with that name.

        @param
            **prompt**
            The prompt you want to use in the image generation. The
            more specific and explicit you are, the more accurate 
            result you get.

        @param
            **output_filename**
            The filename you want for the image to be stored locally.
            If None provided it won't be stored.
        """
        ParameterValidator.validate_mandatory_string('prompt', prompt, do_accept_empty = False)
        
        output_filename = Output.get_filename(output_filename, FileType.IMAGE)
        
        return HugginFace(DEV_HUGGINFACE_ENDPOINT).generate_image({'inputs': prompt}, output_filename)

    @staticmethod
    def generate_schnell(
        prompt: str,
        output_filename: Union[str, None] = None
    ):
        """
        Generates an image using the Flux 'dev' model, through the 
        HugginFace endpoint, and returns it read as PIL image. If
        'output_filename' provided, it will be also stored locally
        with that name.

        @param
            **prompt**
            The prompt you want to use in the image generation. The
            more specific and explicit you are, the more accurate 
            result you get.

        @param
            **output_filename**
            The filename you want for the image to be stored locally.
            If None provided it won't be stored.
        """
        ParameterValidator.validate_mandatory_string('prompt', prompt, do_accept_empty = False)
        
        output_filename = Output.get_filename(output_filename, FileType.IMAGE)
        
        return HugginFace(SCHNELL_HUGGINFACE_ENDPOINT).generate_image({'inputs': prompt}, output_filename)

# TODO: Try to download the models and implement with Diffusers
# https://huggingface.co/black-forest-labs/FLUX.1-schnell?inference_api=true
# https://huggingface.co/black-forest-labs/FLUX.1-schnell?inference_api=true

# Interesting: https://www.youtube.com/watch?v=P-rzgaIfZCo