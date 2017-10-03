import json
import requests
import re
from urllib.parse import quote, unquote

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

argregex = re.compile(r"([^&]+)=([^&]+)")

class DataSplitter:

    keywords = {
        'protocol': 'https',
        'domain': '',
        'tld': 'com',
        'path': '',
        'index': ''
        }

    def __init__(self, data):
        self.params = dict()
        self.data = re.findall(argregex, data)
        for k, v in self.data:
            if k in self.keywords.keys():
                setattr(self, k, unquote(v))
            else:
                self.params[k] = unquote(v)

        attrs = dir(self)
        for k, v in self.keywords.items():
            if not k in attrs:
                setattr(self, k, v)


class RespMeta(Resource):
    def get(self):
        return """
        My RESTful api, this is supposed to interact with the cleverbot.com RESTful api
        """


class Resp(Resource):
    def get(self, data):
        self.data = DataSplitter(data)
        print(self.data.params)

        self.url = '{0.protocol}://www.{0.domain}.{0.tld}/{1}'.format(self.data, self.data.path.replace(',', '/'))
        print(self.url)

        try:
            with requests.get(self.url, params=self.data.params) as resp:
                
                try:
                    extr = resp.json()
                except TypeError:
                    return 'Invalid schema'
                except Exception as e:
                    return str(e)

                try:
                    value = eval("extr" + self.data.index)
                except Exception as e:
                    return str(e)

                return value
        except Exception as e:
            return str(e)

 
api.add_resource(Resp, '/request/<string:data>')
api.add_resource(RespMeta, '/meta')

if __name__ == '__main__':
     app.run()