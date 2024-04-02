import pandas
import boto3
import json
from typing import List, Union

class Client:
    def __init__(self, model, **kwargs) -> None:
        self.session = boto3.Session(**kwargs)
        self.client = self.session.client('bedrock-runtime')
        self.model = model
        
    def ask(self, prompt: str, dfs: Union[List[pandas.DataFrame], pandas.DataFrame]) -> str:
        _dumps_dfs = json.dumps(dfs.to_dict(orient='records')) if isinstance(dfs, pandas.DataFrame) else json.dumps([df.to_dict(orient='records') for df in dfs])
        print(_dumps_dfs)
        _prompt = """\n\nHuman: Analyze the following dataframe(s) {} \
            \n\n{} \
            \n\nAssistant:""".format(_dumps_dfs, prompt)
        _body = json.dumps({
            'prompt': _prompt,
            'max_tokens_to_sample': 2048
        })
        try:
            resp = self.client.invoke_model(
                body=_body,
                contentType='application/json',
                accept='application/json',
                modelId=self.model
            ).get('body').read().decode('utf-8')
        except Exception as e:
            raise e
        return json.loads(resp).get('completion')
