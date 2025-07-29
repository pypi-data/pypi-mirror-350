from abc import ABC, abstractmethod


class Prompt(ABC):
    """
    Abstract class to be inherited by any prompt
    generator class.
    """

    @abstractmethod
    def get(self):
        """
        Get the prompt using the provided parameters (if
        existing and needed).
        """
        pass

class ColouringBookSketchPrompt(Prompt):
    """
    Prompt to generate a colouring book or sketch
    image with the shape of the provided element
    with only black borders and pure white filling
    and a green chroma background to be removed
    easily.
    """
    
    def get(
        self,
        element: str
    ):
        return f'Create a simple, child-friendly coloring page featuring a {element}. The {element} should have crisp, clean black outlines with no shading or gradients. The interior of the {element} should be filled with pure white. Ensure that the black lines are distinct and well-defined. The background of the image should be a solid, intense green, like chroma key green, with no additional details or elements.'