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
            with requests.get(
                    self.url,
                    params=self.data.params,
                    timeout=8.0
                ) as resp:

                response = resp.json()
                print('Status:', response.get('status', 'n/a'))

                if response.get('status', None) == '505':
                    return "I'm currently out of gas, but expecting a top up soon!"

                try:
                    output = response['output']
                    set_cs(response['cs'])
                except IndexError:
                    return "Uh oh, looks like I didn't understand that"
                except Exception as e:
                    return str(e)

        except requests.exceptions.Timeout as e:
            return "Looks like something is broken, oops, expect me to be functional soon!"
        except Exception as e:
            return 'Error, please contact us preferably with a screencap of your\'s and this message. [{}: {}]'.format(type(e), e)

        print('In: {}\nOut: {}'.format(response['input'], response['output']))
        return output
