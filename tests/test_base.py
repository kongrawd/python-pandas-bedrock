import pytest
import pandas
import pandas_bedrock


def test_client(target_env):
    client = pandas_bedrock.Client(
        model=target_env['model_id'],
        region_name=target_env['aws_region_name'],
        profile_name=target_env['aws_profile_name']
        )
    df = pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert client.ask('prompt', df) == 'response'