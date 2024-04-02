import pytest
import pandas
import pandas_bedrock


def test_client(target_env):
    client = pandas_bedrock.Client(
        model=target_env['model_id'],
        region_name=target_env['aws_region_name'],
        profile_name=target_env['aws_profile_name']
        )
    df = pandas.DataFrame({'goat': [1, 2, 3], 'cow': [4, 5, 6]})
    assert 'cow' in client.ask('Respond strictly one word that\'s either goat or cow, what\'s the second column\'s word', df)

def test_dataframe_ask(target_env):
    client = pandas_bedrock.Client(
        model=target_env['model_id'],
        region_name=target_env['aws_region_name'],
        profile_name=target_env['aws_profile_name']
        )
    df = pandas.DataFrame({
        'Name': ['Scooby Doo', 'Lassie', 'Snoopy', 'Pluto', 'Santa’s Little Helper'],
        'Breed': ['Great Dane', 'Collie', 'Beagle', 'Mixed', 'Greyhound'],
        'Show': ['Scooby-Doo', 'Lassie', 'Peanuts', 'Disney', 'The Simpsons']
    })
    resp = client.ask('explain', df)
    print(resp)
    assert 'dog' in resp.lower()

def test_dataframe_ask_list(target_env):
    client = pandas_bedrock.Client(
        model=target_env['model_id'],
        region_name=target_env['aws_region_name'],
        profile_name=target_env['aws_profile_name']
        )
    df1 = pandas.DataFrame({
        'Prompt_ID': [1, 2, 3],
        'Prompt': [
            'Write a poem about the autumn season.',
            'Explain the theory of relativity in simple terms.',
            'Create a short story about a space-faring cat.'
        ]
    })
    df2 = pandas.DataFrame({
        'Response_ID': [1, 2, 3],
        'Prompt_ID': [1, 2, 3],
        'Response': [
            'Leaves in blaze, fall\'s firmament prays, as hues cascade, a seasonal serenade.',
            'Einstein\'s theory talks of time and space, saying speed can face, a relative embrace.',
            'Cosmo the cat, with a helmet so snug, leaped into the black, a starry hug.'
        ]
    })
    resp = client.ask('Explain the theory of relativity in simple terms.', [df1, df2])
    print(resp)
    assert 'einstein' in resp.lower()
