from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileType
from yta_file_downloader import Downloader
from typing import Union

from openai import OpenAI


# TODO: Is this actually useful? I think it could be removed...
class OpenAI:
    """
    Class to wrap the OpenAI functionality.
    """
    
    def generate_image(
        prompt: str,
        output_filename: Union[str, None] = None
    ):
        ParameterValidator.validate_mandatory_string('prompt', prompt, do_accept_empty = False)
        
        output_filename = Output.get_filename(output_filename, FileType.IMAGE)

        client = OpenAI()

        response = client.images.generate(
            model = "dall-e-3",
            prompt = prompt,
            size = "1792x1024",
            quality = "standard",
            n = 1,
        )

        image_url = response.data[0].url

        return Downloader.download_image(image_url, output_filename)