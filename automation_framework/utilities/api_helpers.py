import requests


class ApiHelper:

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_current_weather(self, **kwargs):
        """ Universal method for weather requests.
            Accepts kwargs like:
            - q='London'
            - id=2643743
            - lat=51.5085, lon=-0.1257
            and builds a request accordingly.
        """
        params = {
            "appid": self.api_key,
            "units": "metric",
        }

        params.update(kwargs)
        return requests.get(self.base_url, params=params)