from typing import TYPE_CHECKING, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from botocore.config import Config

from .models.base import Claude

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - (%(filename)s:%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)

logger = logging.getLogger(__name__)

class BedrockProvider:
    def __init__(self, model_id: str, api_name: str, client_config: Config = Config(read_timeout=300), **kwargs):
        """
        Initialize the BedrockProvider with the necessary parameters.

        Args:
            model_id (str): The unique identifier for the model.
            api_name (str): The name of the API to be used.
            client_config (Config, optional): Configuration for the boto3 client. Defaults to Config(read_timeout=300).
            **kwargs: Arbitrary keyword arguments for boto3.Session.

        Raises:
            NoCredentialsError: If no AWS credentials are found.
        """
        self.model_id = model_id
        self.api_name = api_name
        self.model_name = self.get_model_name(model_id)
        try:
            self.session = boto3.Session(**kwargs)
            self.session.client('sts').get_caller_identity()
        except NoCredentialsError:
            logger.error('No AWS credentials found. Please configure your AWS profile.')
            raise
        self.client = self.session.client('bedrock-runtime', client_config)

    def get_model_name(self, model_id: str) -> str:
        try:
            model_name = model_id.split('.')[1].split('-')[0]
        except IndexError:
            logger.error(f'IndexError: Unable to get model_name from: {model_id}')
            raise ValueError(f'Unable to get model_name from: {model_id}')
        return model_name

    def invoke(self, prompt: str, **kwargs) -> str:
        if self.model_name.lower() == 'claude':
            return Claude(provider=self).invoke(prompt, **kwargs)
        else:
            logger.warning(f'{self.model_name} model not implemented yet.')
            raise NotImplementedError(f'{self.model_name} model not implemented yet.')

    def call_api(self, request_body: str) -> str:
        if self.api_name == 'text_api':
            logger.debug(f'Calling API for model_id {self.model_id}')
            logger.debug(f'Request body: {request_body}')
            try:
                resp = self.client.invoke_model(
                    body=request_body,
                    contentType='application/json',
                    accept='application/json',
                    modelId=self.model_id,
                )
                logger.info(f'Successfully called API for model_id {self.model_id}')
                return resp['body'].read().decode('utf-8')
            except ClientError as e:
                logger.error(f'ClientError when calling API for model_id {self.model_id}: {e}')
                raise
            except BotoCoreError as e:
                logger.error(f'BotoCoreError when calling API for model_id {self.model_id}: {e}')
                raise
            except Exception as e:
                logger.error(f'Unexpected error when calling API for model_id {self.model_id}: {e}')
                raise
        elif self.api_name == 'messaging_api':
            logger.warning(f'{self.api_name} API not implemented yet.')
            raise NotImplementedError(f'{self.api_name} API not implemented yet.')
        else:
            logger.warning(f'{self.api_name} API not supported.')
            raise NotImplementedError(f'{self.api_name} API not implemented yet.')
