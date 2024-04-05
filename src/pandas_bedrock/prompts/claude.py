from typing import Union, List, Dict, Any
import json

from .base import BasePromptFormatter

class ClaudePromptFormatter(BasePromptFormatter):
    def format_prompt(self, prompt: str, **kwargs: Dict[str, Any]) -> str:
        """
        Formats the prompt specifically for the Claude model.

        Parameters and return are as per the base class.
        """
        try:
            # For each key in kwargs, add the key and value to the prompt
            # This is a simple way to allow for model-specific customization
            # For example, if kwargs contains {"system": "you're an personalized assistant."},
            # the prompt will include "system: you're an personalized assistant."
            formatted = f"\n\nHuman: {prompt}"
            for key, value in kwargs.items():
                formatted += f"\n\n{key}: {value}"
            formatted += f"\n\nAssistant:"
        except TypeError as e:
            return f"Error formatting prompt: {str(e)}"

        return formatted
