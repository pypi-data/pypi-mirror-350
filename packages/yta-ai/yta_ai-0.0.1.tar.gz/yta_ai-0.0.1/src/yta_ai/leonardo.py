from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileType
from yta_file_downloader import Downloader
from yta_programming.env import Environment
from typing import Union

import requests
import os
import time


MODEL_LEONARDO_DIFFUSION_XL = '1e60896f-3c26-4296-8ecc-53e2afecc132'

class Leonardo:
    """
    Class to wrap the functionality of Leonardo
    AI.
    """

    @staticmethod
    def _request_generation(
        prompt: str
    ):
        """
        Makes a request to generate an image. It returns the generation id.

        This method needs the non-free API working.
        """
        ParameterValidator.validate_mandatory_string('prompt', prompt, do_accept_empty = False)
        
        #return '69503ef1-85c8-41cc-b292-f672946920d7'
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"

        payload = {
            'modelId': MODEL_LEONARDO_DIFFUSION_XL,
            'width': 1024,   # test 1536
            'height': 576,   # test 864
            'num_images': 1,
            'prompt': prompt
        }

        LEONARDO_API_KEY = Environment.get_current_project_env('LEONARDOAI_API_KEY')

        headers = {
            "accept": "application/json",
            "authorization": f'Bearer {LEONARDO_API_KEY}',
            "content-type": "application/json",
        }

        response = requests.post(url, json = payload, headers = headers)
        response = response.json()

        print(response)

        return response['sdGenerationJob']['generationId']

    @staticmethod
    def _download_generated_image(generation_id, output_filename):
        """
        Downloads the AI-generated image by using the provided 'generation_id'.

        It downloads the image and resizes it to 1920x1080.
        """
        url = 'https://cloud.leonardo.ai/api/rest/v1/generations/' + str(generation_id)

        headers = {
            "accept": "application/json",
            "authorization": "Bearer " + str(os.getenv('LEONARDOAI_API_KEY')),
        }

        response = requests.get(url, headers = headers)
        response = response.json()

        # TODO: Do a passive waiting
        is_downloadable = True

        if len(response['generations_by_pk']['generated_images']) == 0:
            is_downloadable = False

        while not is_downloadable:
            time.sleep(10)
            print('Doing a request in loop')

            # We do the call again
            response = requests.get(url, headers = headers)
            response = response.json()
            
            if len(response['generations_by_pk']['generated_images']) > 0:
                is_downloadable = True

        downloadable_url = response['generations_by_pk']['generated_images'][0]['url']

        return Downloader.download_image(downloadable_url, output_filename)

    @staticmethod
    def generate_image(
        prompt: str,
        output_filename: Union[str, None] = None
    ):
        """
        Generate an AI image with the provided 'prompt' and
        store it locally as the given 'output_filename'.
        """
        if not PythonValidator.is_string(prompt):
            raise Exception('The provided "prompt" is not a valid string.')
        
        output_filename = Output.get_filename(output_filename, FileType.IMAGE)
        
        return Leonardo._download_generated_image(
            Leonardo._request_generation(prompt),
            output_filename
        )

