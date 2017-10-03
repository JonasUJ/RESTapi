import json
import requests
import re

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

argregex = re.compile(r"(\w+)=(\w+)")

class DataSplitter:

    keywords = ['url']

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
        return 'My RESTful api, this is supposed to interact with the cleverbot.com RESTful api'


class Resp(Resource):
    def get(self, data):
        self.data = DataSplitter(data)
        print(self.data, dir(self.data))
        print(self.data.url, self.data.params)
        with requests.get(self.data.url, params=self.data.params) as resp:
            return resp.json()
 
api.add_resource(Resp, '/request/<string:data>')
api.add_resource(RespMeta, '/meta')

if __name__ == '__main__':
     app.run()