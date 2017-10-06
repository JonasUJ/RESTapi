import os
import re
import requests
from urllib.parse import unquote

from flask_restful import Resource
from presets.cleverbotfool.fool import Fool

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
        'callback': '',
        'fool': 'false'
    }

    def __init__(self, data):

        self.data = re.findall(ARG_RE, data)

        for k, v in self.data:
            if k in self.params.keys():
                self.params[k] = unquote(v)


class Endpoint(Resource):

    url = 'https://www.cleverbot.com/getreply'

    def get(self, data):
        self.data = DataSplitter(data)

        inp = self.data.params['input']

        fooled_entry = Fool.get(inp)
        if self.data.params['fool'] == 'true' and fooled_entry:
            print('In: {}\nFooled out: {}'.format(inp, fooled_entry))
            return fooled_entry

        if not self.data.params['cs']:
            self.data.params['cs'] = get_cs()

        if not self.data.params['key']:
            return 'No cleverbot api key supplied'

        try:
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
