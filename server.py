import json
import requests

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class RespMeta(Resource):
    def get(self):
        return 'My RESTful api, this is supposed to interact with the cleverbot.com RESTful api'

class Resp(Resource):
    def get(self, url, index):
        #with requests.get(url)
        return index, url
 
api.add_resource(Resp, '/request/<string:inp>')
api.add_resource(RespMeta, '/meta')

if __name__ == '__main__':
     app.run()