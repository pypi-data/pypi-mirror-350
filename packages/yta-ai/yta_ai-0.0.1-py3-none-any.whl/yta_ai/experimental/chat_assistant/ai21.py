from ai21 import AI21Client

import os


API_KEY = os.environ.get("AI21_API_KEY")

# This AI allows you to work just with registering. They give you 90$ to start

def paraphrase(text):
    client = AI21Client(
        api_key = API_KEY,
    )

    # TODO: This model works in English, so I receive the suggestion in English

    # This method returns a lot of paraphrased, we will choose the first one
    response = client.paraphrase.create(text = text, start_index = 0)

    # Response has suggestions, with text 
    return response.suggestions[0].text

def test():
    print(paraphrase('Hola, mi nombre es Alberto y tengo el culo abierto.'))