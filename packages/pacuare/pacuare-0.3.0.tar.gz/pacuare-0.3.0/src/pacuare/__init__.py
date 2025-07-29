import requests
import pandas as pd

class Client:
    """A client for the Pacuare API."""
    def __init__(self, api_key: str, base: str = 'https://api.pacuare.dev/v1'):
        """
        Create a new client.
        An API key must be generated in your account settings to access the API.
        `base` is for development purposes.
        """
        self.api_key = api_key
        self.base = base
    
    def query(self, sql: str, params: list = []) -> pd.DataFrame:
        """Query your database using SQL, returning a Pandas DataFrame of the results."""
        res = requests.post(self.base + '/query',
                            headers={
                                'Authorization': 'Bearer ' + self.api_key
                            },
                            json={
                                'query': sql,
                                'params': params
                            })

        print(res.text)
        return pd.DataFrame.from_records(res.json()['values'], columns=res.json()['columns'])