"""
This is an interesting idea but it is outdated.
"""
from yta_general_utils.text_processor import remove_marks_and_accents
from utils.ai.chat import get_script

CHARS_PER_SECOND = 17 # For Matthew
SECONDS_PER_PAUSE = 0.4 # Estimated by me

# TODO: Here I will generate narration scripts from an idea, from cero
def __seconds_to_chars(seconds):
    """
    Returns the number of chars that, when narrated, will last the expected 'seconds'
    duration in seconds.
    """
    # This has been manually calculated for Matthew. Each voice will work at its own speed.
    # 1 second => 17 characters
    # 1 '.' => +0.5 seconds
    return int(CHARS_PER_SECOND * seconds)

def __chars_to_seconds(text):
    """
    Returns the number of seconds that the provided chars number would last in a 
    narration.
    """
    return len(text) / CHARS_PER_SECOND

def __estimate_duration(text: str):
    """
    This method analyzes the provided narration script to estimate the duration that
    the text will last when narrated.
    """
    # We estimate based on simple chars without marks. Only narrative chars
    estimated_seconds = __chars_to_seconds(remove_marks_and_accents(text))
    # We treat each stop mark as a pause, so we add that time in seconds
    count = 0
    count += text.count('?')
    text = text.replace('?', '')
    count += text.count('!')
    text = text.replace('!', '')
    count += text.count('...')
    text = text.replace('...', '')
    count += text.count('.')
    text = text.replace('.', '')
    estimated_seconds += SECONDS_PER_PAUSE * count

    return estimated_seconds


def generate(idea, duration):
    """
    Generates a narration script from the provided 'idea' that will last around 'duration' minutes.

    # TODO: Finish it
    """
    # TODO: Ask AI for an script of 'x' characters

    # I want to create one script that lasts this time below
    time_in_seconds = 60 * duration
    needed_chars = __seconds_to_chars(time_in_seconds)

    # TODO: Ask for AI generated script
    return 'This need to be done, by now is just a fixed text.'
    return get_script(idea, needed_chars)



# https://www.reddit.com/r/OpenAI/comments/vm3kfk/comment/ie4j7vf/