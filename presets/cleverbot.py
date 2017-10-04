import os
import re
import requests
from urllib.parse import quote

from flask_restful import Resource


ARG_RE = re.compile(r"([^&]+)=([^&]*)")


class DataSplitter:

    params = {
        'userinput': '',
        'key': '',
        'cs': '',
        'callback': ''
    }

    def __init__(self, data):

        self.data = re.findall(ARG_RE, data)

        for k, v in self.data:
            if k in self.params.keys():
                self.params[k] = quote(v)


class Endpoint(Resource):

    url = 'https://www.cleverbot.com/getreply'

    def get(self, data):
        self.data = DataSplitter(data)

        if not self.data.params['key']:
            return 'No cleverbot api key supplied'

        try:
            with requests.get(self.url, params=self.data.params) as resp:
                try:
                    output = resp.json()['output']
                except IndexError:
                    return 'Sorry, could not get a valid respone from cleverbot :('
                except Exception as e:
                    return str(e)

        except Exception as e:
            return str(e)

        return output
