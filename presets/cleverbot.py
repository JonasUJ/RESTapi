import requests
import json
from flask import Response, request

from presets.cleverbotfool.fool import Fool


class CleverBot:

    def __init__(self, user, key, cs='MXYxCTh2MQlBdldYQ1BBVkxGT1cJMUZ2MTUxNjM5OTM2Mgk2NGlJIGJvcmVkLgk='):
        self.user = user
        self.key = key
        self.url = 'https://www.cleverbot.com/getreply'

        self.params = {
            'key': key,
            'cs': cs,
            'callback': '',
            'input': ''
        }

    def query(self, text, fool=True):

        fooled_entry = Fool.get(text)
        if fool and fooled_entry:
            print('In: {}\nFooled out: {}'.format(text, fooled_entry))
            return fooled_entry

        self.params['input'] = text

        try:
            resp = requests.get(self.url, params=self.params, timeout=8.0)
            respdict = resp.json()
        except requests.exceptions.Timeout:
            return "Looks like something is broken, oops, expect me to be functional soon! (Maybe this is a single time thing, just try again)"
        except Exception as e:
            print(e)
            return 'Error, please contact us preferably with a screencap of your\'s and this message. [{}: {}]'.format(type(e), e)

        if respdict.get('status') == '505':
            return "I'm currently out of gas, but expecting a top up soon!"
        elif respdict.get('status') == '401':
            return 'Invalid key'
        elif respdict.get('status') == '413' or respdict.get('status') == '414':
            return "Sorry, but i don't understand that long queries."
        elif respdict.get('status') == '502' or respdict.get('status') == '504':
            return 'Something is broken, and we are unable to fix it at this moment'
        elif respdict.get('status') == '503':
            return self.query(text)

        elif respdict.get('status', 'success') == 'success':
            self.params['cs'] = respdict['cs']
            print('In: {}\nOut: {}'.format(respdict['input'], respdict['output']))
            return '{}{}'.format(f'@{self.user} ' if self.user != 'default' else '', respdict['output'])
        else:
            print('Non-success status:', respdict['status'])
            return False
        

    def __repr__(self):
        return f'{self.__class__.__name__}(user={self.user})'


class BotHandler:
    
    def __init__(self):
        self.bots = dict()


    def get_bot(self, key='', user=''):
        if self.bots.get(user):
            return self.bots[user]
        else:
            print(f'Created new CleverBot for user: {user}')
            self.bots[user] = CleverBot(user=user, key=key)
            return self.bots[user]


def setup(api, app, name, objects):

    if not hasattr(objects, f'BotHandler_{name}'):
        setattr(objects, f'BotHandler_{name}', BotHandler())

    @app.route(f'/{name}')
    def cleverbot_endpoint():
        clevbot = getattr(objects, f'BotHandler_{name}').get_bot(key=request.args['key'], user=request.args.get('user', 'default'))
        print(f'Responding with: {str(clevbot)}')
        text = clevbot.query(request.args['input'])

        resp = Response(text, status=200, mimetype='text/plain')
        return resp