import json
from typing import Union, List
import pandas

def dfs_to_json_string(dfs: Union[List[pandas.DataFrame], pandas.DataFrame]) -> str:
    return json.dumps(dfs.to_dict(orient='records')) if isinstance(dfs, pandas.DataFrame) else json.dumps([df.to_dict(orient='records') for df in dfs])
