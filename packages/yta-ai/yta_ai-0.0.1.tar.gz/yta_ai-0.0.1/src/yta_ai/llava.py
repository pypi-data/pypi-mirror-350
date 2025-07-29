import ollama


class Llava:
    """
    Class to describe an image using the Llava engine
    through the 'ollama' python package.
    """

    def describe(
        self,
        image_filename: str
    ):
        """
        THIS METHOD IS NOT WORKING YET.

        TODO: This is not working because of my pc limitations.
        It cannot load the resources due to memory capacity.
        """
        res = ollama.chat(
            model = 'llava',
            messages = [
                {
                    'role': 'user',
                    'content': 'Describe this image',
                    'images': [
                        image_filename
                    ]
                }
            ]
        )

        response_content = res['message']['content']

        return response_content