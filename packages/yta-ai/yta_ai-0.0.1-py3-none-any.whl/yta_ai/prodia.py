# TODO: This must be replaced by the new 'FileReturned'
from yta_general_utils.dataclasses import FileReturn
from yta_constants.file import FileType
from yta_file_downloader import Downloader
from yta_programming.env import Environment
from yta_programming.output import Output
from yta_validation.parameter import ParameterValidator
from typing import Union

import time
import requests


PRODIA_API_KEY =  Environment.get_current_project_env('PRODIA_API_KEY')

class Prodia:
    """
    Class to wrap prodia functionality. Prodia is an
    image generator engine.
    """

    @staticmethod
    def generate_image(
        prompt: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        ParameterValidator.validate_mandatory_string('prompt', prompt, do_accept_empty = False)
        
        # If you comment this and uncomment the one below it works
        # seed = randint(1000000000, 9999999999)
        # response = requests.get('https://api.prodia.com/generate?new=true&prompt=' + prompt + '&model=absolutereality_v181.safetensors+%5B3d9d4d2b%5D&steps=20&cfg=7&seed=' + str(seed) + '&sampler=DPM%2B%2B+2M+Karras&aspect_ratio=square')
        payload = {
            'new': True,
            'prompt': prompt,
            #'model': 'absolutereality_v181.safetensors [3d9d4d2b]',   # this model works on above request, not here
            'model': 'sd_xl_base_1.0.safetensors [be9edd61]',
            #'negative_prompt': '',
            'steps': 20,
            'cfg_scale': 7,
            'seed': 2328045384,
            'sampler': 'DPM++ 2M Karras',
            'width': 1344,
            'height': 768
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": PRODIA_API_KEY
        }
        url = 'https://api.prodia.com/v1/sdxl/generate'
        response = requests.post(url, json = payload, headers = headers)
        response = response.json()

        output_filename = Output.get_filename(output_filename, FileType.IMAGE)

        # When requested it is queued, so we ask for it until it is done
        if "status" in response and response['status'] == 'queued':
            job_id = response['job']
            return Prodia._retrieve_job(job_id, output_filename)
        else:
            print(response)
            raise Exception('There was an error when generating a Prodia AI Image.')

    @staticmethod
    def _retrieve_job(
        job_id: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Makes a request for the image that is being
        generated with the provided 'job_id'.

        It has a loop to wait until it is done. This
        code is critic because of the loop.
        """
        url = f'https://api.prodia.com/v1/job/{str(job_id)}'

        headers = {
            'accept': 'application/json',
            'X-Prodia-Key': PRODIA_API_KEY
        }

        response = requests.get(url, headers = headers)
        response = response.json()
        #print(response)

        # TODO: Do a passive waiting
        is_downloadable = True

        if response['status'] != 'succeeded':
            is_downloadable = False

        # TODO: Implement a tries number
        while not is_downloadable:
            time.sleep(5)
            print('Doing a request in loop')

            # We do the call again
            response = requests.get(url, headers = headers)
            response = response.json()
            print(response)
            if 'imageUrl' in response:
                is_downloadable = True

        image_url = response['imageUrl']

        output_filename = Output.get_filename(output_filename, FileType.IMAGE)

        return Downloader.download_image(image_url, output_filename)