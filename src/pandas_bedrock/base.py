import pandas
import boto3

class Client:
    def __init__(self, model, **kwargs) -> None:
        self.session = boto3.Session(**kwargs)
        self.client = self.session.client('bedrock-runtime')
        self.model = model
        
    def ask(self, prompt: str, df: pandas.DataFrame) -> str:
        _body = {
            'prompt': prompt,
            'data': df.to_dict(orient='records')
        }
        try:
            resp = self.client.invoke_model(
                body=_body,
                contentType='application/json',
                accept='application/json',
                modelId=self.model
            )
        except Exception as e:
            raise e
        return resp['body'].read().decode('utf-8')