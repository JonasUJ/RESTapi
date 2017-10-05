import os
import re
import requests
from urllib.parse import quote

from flask_restful import Resource

global cs
cs = ''

def set_cs(conv):
    global cs
    cs = conv

def get_cs():
    global cs
    return cs


ARG_RE = re.compile(r"([^&]+)=([^&]*)")


class DataSplitter:

    params = {
        'input': '',
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

        if not self.data.params['cs']:
            self.data.params['cs'] = get_cs()

        if not self.data.params['key']:
            return 'No cleverbot api key supplied'

        try:
            print(self.data.params)
            with requests.get(self.url, params=self.data.params) as resp:
                try:
                    response = resp.json()
                    output = response['output']
                    set_cs(response['cs'])
                except IndexError:
                    return 'Sorry, could not get a valid respone from cleverbot :('
                except Exception as e:
                    return str(e)

        except Exception as e:
            return str(e)

        print('In: {}\nOut: {}'.format(response['input'], response['output']))
        return output
