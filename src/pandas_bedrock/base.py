from abc import ABC, abstractmethod
from typing import List, Union
import pandas as pd
from .bedrock import BedrockProvider
from .utils import dfs_to_json_string
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - (%(filename)s:%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)

logger = logging.getLogger(__name__)

class BaseClient(ABC):
    def __init__(self, model_id: str, api_name: str, **kwargs):
        self.model_id = model_id
        self.api_name = api_name
        self.model = None
        logger.debug(f"Initializing BaseClient with model_id: {model_id} and api_name: {api_name}")

    @abstractmethod
    def ask(self, prompt: str, dfs: Union[List[pd.DataFrame], pd.DataFrame]) -> str:
        pass

    @abstractmethod
    def chat(self, prompt: str) -> None:
        pass

class Client(BaseClient):
    def __init__(self, model_id: str, api_name: str = 'text_api', **kwargs):
        super().__init__(model_id, api_name, **kwargs)
        try:
            self.model = BedrockProvider(model_id, api_name, **kwargs)
            logger.debug(f"Client initialized with model_id: {model_id}, api_name: {api_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Client with model_id: {model_id}, api_name: {api_name}. Error: {e}")
            raise

    def ask(self, prompt: str, dfs: Union[List[pd.DataFrame], pd.DataFrame], **kwargs) -> str:
        try:
            logger.info(f"Ask invoked with prompt: '{prompt}' and kwargs: {kwargs}")
            completion = self.model.invoke(
                prompt,
                prompt_kwargs={'Context': dfs_to_json_string(dfs)},
                **kwargs
            )
            logger.info(f"Ask completed: {completion}")
            return completion
        except Exception as e:
            logger.error(f"Error during ask operation with prompt: '{prompt}'. Error: {e}")
            raise

    def chat(self, prompt: str) -> None:
        try:
            logger.info(f"Chat invoked with prompt: '{prompt}'")
        except Exception as e:
            logger.error(f"Error during chat operation with prompt: '{prompt}'. Error: {e}")
            raise
