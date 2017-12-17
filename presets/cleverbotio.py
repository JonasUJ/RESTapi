import requests
import json
from flask import Response, request


class CleverBot:

    def __init__(self, user, key):
        self.user = user
        self.key = key

        body = {
            'user': user,
            'key': key,
            'nick': None
        }

        requests.post('https://cleverbot.io/1.0/create', json=body)


    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': None,
            'text': text
        }

        try:
            with requests.post('https://cleverbot.io/1.0/ask', json=body, timeout=12.0) as resp:
                respdict = resp.json()

                if respdict['status'] == 'success':
                    return respdict['response']
                else:
                    print('Non-success status', respdict['status'])
                    return False
        
        except requests.exceptions.Timeout:
            return "Looks like something is broken, oops, expect me to be functional soon!"


class BotHandler:
    
    def __init__(self):
        self.bots = dict()


    def get_bot(self, key='', user=''):
        if self.bots.get(user):
            return self.bots[user]
        else:
            print('Created new CleverBot')
            self.bots[user] = CleverBot(user=user, key=key)
            return self.bots[user]


def setup(api, app, name, objects):

    if not hasattr(objects, 'BotHandler'):
        setattr(objects, 'BotHandler', BotHandler())

    @app.route(f'/{name}')
    def cleverbotio_endpoint():
        clevbot = objects.BotHandler.get_bot(key=request.args['key'], user=request.args['user'])
        text = clevbot.query(request.args['text'])

        resp = Response(text, status=200, mimetype='text/plain')
        return resp