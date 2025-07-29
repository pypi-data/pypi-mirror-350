from yta_image.parser import ImageParser
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from typing import Union

import numpy as np


class Blip:
    """
    Class to describe an image using the Blip engine, which
    is from Salesforce and will use pretrained models that are
    stored locally in 'C:/Users/USER/.cache/huggingface/hub',
    loaded in memory and used to describe it.

    The process could take from seconds to a couple of minutes
    according to the system specifications.
    """
    
    def describe(
        self,
        image: Union[str, Image.Image, np.ndarray]
    ) -> str:
        image = ImageParser.to_pillow(image)

        # models are stored in C:\Users\USERNAME\.cache\huggingface\hub
        processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
        model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')
        inputs = processor(image, return_tensors = 'pt')
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokes = True)

        # TODO: Fix strange characters. I received 'a red arrow pointing up
        # to the right [SEP]' response from describing an image. What is the
        # '[SEP]' part? What does it mean? I don't want that in response.
        return description