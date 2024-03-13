# Full reference and credit to : https://automationpanda.com/2023/01/12/passing-test-inputs-into-pytest/
import json
import os
import pytest

def pytest_addoption(parser):
  """
  instead create a custom pytest command line argument. 
  Bas Dijkstra wrote an excellent article showing how to do this. 
  Basically, you could add the following function to conftest.py to add the custom argument:
  python -m pytest --target-env dev.json
  """
  parser.addoption(
    '--target-env',
    action='store',
    default='dev.json',
    help='Path to the target environment config file')
 
@pytest.fixture
def target_env(request, scope='session'):
  """
  conftest.py file so all tests can share it. 
  Since it uses session scope, pytest will execute it one time before all tests. 
  Test functions can call it like this: target_env['base_url']
  """
  config_path = request.config.getoption('--target-env')
  assert os.path.isfile(config_path)
 
  with open(config_path) as config_file:
    config_data = json.load(config_file)
 
  assert 'model_id' in config_data
  assert 'aws_region_name' in config_data
  assert 'aws_profile_name' in config_data
 
  return config_data