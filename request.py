import os
import json
import requests
import re
from urllib.parse import quote, unquote
from importlib import import_module

from flask import Flask
from flask_restful import Resource, Api


ARG_RE = re.compile(r"([^&]+)=([^&]*)")


class DataSplitter:

    protocol = 'https'
    domain = ''
    tld = 'com'
    path = ''
    index = ''
    timeout = '8.0'

    def __init__(self, data):

        attrs = dir(self)
        self.params = dict()
        self.data = re.findall(ARG_RE, data)

        for k, v in self.data:
            if k in attrs:
                setattr(self, k, unquote(v))
            else:
                self.params[k] = unquote(v)

        self.path = self.path.replace(',', '/')
        try:
            self.data.timeout = float(self.data.timeout)
        except (ValueError, TypeError):
            self.data.timeout = 8.0


class Meta(Resource):
    def get(self):
        return "My RESTful api, this is supposed to interact with the cleverbot.com RESTful api"


class Resp(Resource):
    def get(self, data):
        self.data = DataSplitter(data)
        self.url = '{0.protocol}://www.{0.domain}.{0.tld}/{0.path}'.format(self.data)

        try:
            with requests.get(
                    self.url,
                    params=self.data.params,
                    timeout=self.data.timeout
                ) as resp:

                try:
                    extr = resp.json()
                except TypeError:
                    return 'Invalid schema'
                except Exception as e:
                    return str(e)

        except requests.exceptions.Timeout:
            return 'Connection timed out'
        except Exception as e:
            return str(e)

        try:
            value = eval("extr" + self.data.index)
        except IndexError:
            return 'Invalid index: ' + self.data.index
        except SyntaxError:
            return 'Invalid index syntax: ' + self.data.index
        except Exception as e:
            return str(e)

        return value


class Objects:
    """Don't mind this"""
    pass

objs = Objects()

app = Flask(__name__)
api = Api(app)

api.add_resource(Resp, '/request/<string:data>')
api.add_resource(Meta, '/')

PRESETS = [os.path.splitext(pre)[0] for pre in os.listdir('presets') if os.path.splitext(pre)[1] == '.py']

for pre in PRESETS:
    module = import_module('presets.{}'.format(pre))
    module.setup(api, app, pre, objects=objs)

if __name__ == '__main__':
     app.run()
