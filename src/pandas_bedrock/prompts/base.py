from abc import ABC, abstractmethod
from typing import Union, List
import pandas as pd
import json

class BasePromptFormatter(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def format_prompt(self, prompt: str, **kwargs) -> str:
        """
        Abstract method for formatting a prompt. Should be overridden by subclasses.

        Parameters:
        - prompt (str): The base prompt or question.
        - kwargs: Additional keyword arguments for model-specific customization. For each key in kwargs,
            add the key and value to the prompt. This is a simple way to allow for model-specific customization.
            For example, if kwargs contains {"system": "you're an personalized assistant."},
            the prompt will include "system: you're an personalized assistant."

        Returns:
        - str: The formatted prompt.
        """
        pass
