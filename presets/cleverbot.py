import requests
import json
from flask import Response, request

from presets.cleverbotfool.fool import Fool


class CleverBot:

    def __init__(self, user, key, cs=''):
        self.user = user
        self.key = key
        self.url = 'https://www.cleverbot.com/getreply'

        self.params = {
            'key': key,
            'cs': cs,
            'callback': '',
            'input': ''
        }

    def query(self, text, fool=False):

        fooled_entry = Fool.get(text)
        if fool and fooled_entry:
            print('In: {}\nFooled out: {}'.format(text, fooled_entry))
            return fooled_entry

        self.params['input'] = text

        try:
            with requests.get(self.url, params=self.params, timeout=8.0) as resp:
                respdict = resp.json()

                if respdict.get('status') == '505':
                    return "I'm currently out of gas, but expecting a top up soon!"
                elif respdict.get('status', 'success') == 'success':
                    self.params['cs'] = respdict['cs']
                    print('In: {}\nOut: {}'.format(respdict['input'], respdict['output']))
                    return respdict['output']
                else:
                    print('Non-success status:', respdict['status'])
                    return False
        
        except requests.exceptions.Timeout:
            return "Looks like something is broken, oops, expect me to be functional soon!"
        except Exception as e:
            print(e)
            return 'Error, please contact us preferably with a screencap of your\'s and this message. [{}: {}]'.format(type(e), e)

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

    if not hasattr(objects, 'BotHandler'):
        setattr(objects, 'BotHandler', BotHandler())

    @app.route(f'/{name}')
    def cleverbot_endpoint():
        clevbot = objects.BotHandler.get_bot(key=request.args['key'], user=request.args.get('user', 'default'))
        print(f'Responding with: {clevbot}')
        text = clevbot.query(request.args['input'])

        resp = Response(text, status=200, mimetype='text/plain')
        return resp