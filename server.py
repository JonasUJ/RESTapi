import json
import requests
import re

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

argregex = re.compile(r"(\w+)=(\w+)")

class DataSplitter:

    keywords = ['protocol', 'domain', 'tld', 'path']

    def __init__(self, data):
        self.params = dict()
        self.data = re.findall(argregex, data)
        for k, v in self.data:
            if k in self.keywords:
                setattr(self, k, v)
            else:
                self.params[k] = v



class RespMeta(Resource):
    def get(self):
        return """
        My RESTful api, this is supposed to interact with the cleverbot.com RESTful api
        """


class Resp(Resource):
    def get(self, data):
        self.data = DataSplitter(data)
        print(self.data.params)

        self.url = '{0.protocol}://{0.domain}.{0.tld}/{1}'.format(self.data, self.data.path.replace('-', '/'))
        print(self.url)

        with requests.get(self.url, params=self.data.params) as resp:
            return resp.json()

 
api.add_resource(Resp, '/request/<string:data>')
api.add_resource(RespMeta, '/meta')

if __name__ == '__main__':
     app.run()