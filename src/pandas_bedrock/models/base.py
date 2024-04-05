from typing import TYPE_CHECKING, Optional
import json

from ..prompts.claude import ClaudePromptFormatter

if TYPE_CHECKING:
    from ..bedrock import BedrockProvider  # This import is only for type checking; it won't cause circular import at runtime.

class Claude:
    def __init__(self, provider: 'BedrockProvider'):
        self.provider: 'BedrockProvider' = provider
        self.prompt_formatter: ClaudePromptFormatter = ClaudePromptFormatter()

    def invoke(self, prompt: str, **kwargs) -> str:
        """
        Invokes the Claude API with a formatted prompt and optional parameters.

        Parameters:
        - prompt (str): The input prompt to be formatted and sent to the API.
        - kwargs: Arbitrary keyword arguments. Supports:
            - prompt_kwargs (dict): Additional parameters for prompt formatting.
            - request_kwargs (dict): Additional parameters for the API request, such as 'max_tokens_to_sample'.

        Returns:
            str: The response from the API.
        """
        # Get prompt_kwargs from kwargs
        prompt_kwargs = kwargs.get('prompt_kwargs', {})
        formatted_prompt: str = self.prompt_formatter.format_prompt(prompt, **prompt_kwargs)

        # Get request_kwargs from kwargs
        request_kwargs = kwargs.get('request_kwargs', {
            'max_tokens_to_sample': 2048,
        })

        request_body: str = json.dumps({
            'prompt': formatted_prompt,
            **request_kwargs,
        })
        response: str = self.provider.call_api(request_body)
        # Properly handle response parsing here.
        return json.loads(response).get('completion')
