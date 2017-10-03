import json

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class RespMeta(Resource):
    def get(self):
        return 'Working'

class Resp(Resource):
    def get(self, inp):
        return inp
 
api.add_resource(Resp, '/dept/<string:inp>')
api.add_resource(RespMeta, '/resp')

if __name__ == '__main__':
     app.run()