from yta_programming.env import Environment
from yta_validation.parameter import ParameterValidator

import google.generativeai as genai


GEMINI_API_KEY =  Environment.get_current_project_env('GEMINI_API_KEY')

class Gemini:
    """
    Class to wrap the Gemini AI chatbot.
    """

    @staticmethod
    def ask(
        prompt: str
    ):
        """
        Ask Gemini AI (gemini-1.5-flash) model by using the
        provided 'prompt' and return its response.
        """
        ParameterValidator.validate_mandatory_string('prompt', prompt, do_accept_empty = False)

        genai.configure(api_key = GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        chat = model.start_chat()
        response = chat.send_message(
            prompt,
        )

        return response.text