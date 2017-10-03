import json
import requests
import re

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

argregex = re.compile(r"(\w+)=(\w+)")

class DataSplitter:
    def __init__(self, data):
        self.data = re.findall(argregex, data)
        for k, v in self.data:
            setattr(self, k, v)


class RespMeta(Resource):
    def get(self):
        return 'My RESTful api, this is supposed to interact with the cleverbot.com RESTful api'

class Resp(Resource):
    def get(self, data:DataSplitter):
        #with requests.get(url)
        return dir(data)
 
api.add_resource(Resp, '/request/<string:url>')
api.add_resource(RespMeta, '/meta')

if __name__ == '__main__':
     app.run()