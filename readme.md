# Python RESTful api

This API is supposed to interact with other APIs, but you know, I made it so
you'll probably not wanna use it ¯\\\_(ツ)\_/¯

Consider writing your own code that does the same if you absolutely must.

## Intro

The reason I created this is that I wanted a
[NightBot](https://beta.nightbot.tv) command the interacted with the
Cleverbot API, too bad that API only returns a JSON object,
and NightBot doesn't understand that.

This will let you specify the index in the JSON object you want and give you
only that.

## Usage

Let's say you send a request to
https://cleverbot.com/getreply?key=apikey&input=hello then Cleverbot might
return something along the lines of:
```json
{
  "cs": "CmE7ASDno0dPdsnIwn=2.dAJndnWi1!ina8dn=",
  "input": "hello",
  "output": "Hello. Who are you?",
  "output_label": "welcome"
}
```
(This is of course simplified for the sake of readability, but you get the
idea.)

Now, if NightBot got this response, it'd just error out and say the response is
more than 400 characters, and even if it didn't, you'd only want the `"output"`
part.

This is where you would send the request through this API, and only have it
return `"Hello. Who are you?"`. You would simply make a request to
`/request/protocol=https&domain=cleverbot&tld=com&path=getreply&key=apikey&input=hello&index=['output']`
which would give you the value `"Hello. Who are you?"`.

Notice that the request contains a lot of parameters, separated by ampersands,
these are:
- `protocol` The protocol used to make the request, defaults to `https`
- `domain` The domain to make the request to
- `tld` The Top Level Domain of the `domain`, defaults to `com`
- `path` The path of the request, since `/`s would screw up the request to the
API, this is separated by `,`s
- `index` The index in the JSON object

Everything else is passed as parameters to the specified API, in this case
`input` is passed.

## Presets

**This has changed, now all a preset requires is a `setup(api, app, name, objects)` function.**

Presets help by making the request less painful, and can also do stuff depending
on the response from the API, instead of just returning it.

Let's say we make a preset `foo.py`, which would allow you to make requests to
`/foo/`. This wouldn't return anything until we put something in the `foo.py`
preset, we can put in a `Endpoint` class that inherits from
`flask_restful.Resource`.

```python
class Endpoint(flask_restful.Resource):
  def get(self, data):
    # Logic goes here
```
The `Endpoint` class must have a `get` method that takes `data` as a parameter

`data` is everything beyond the `/` in `/foo/` e.g. it would be
`bar=baz&spam=eggs` in `/foo/bar=baz&spam=eggs`. Whatever `get` returns will be
what the API returns.

In the `cleverbot.py` preset, the `Endpoint` basically looks like this:

```python
class Endpoint(Resource):

  url = 'https://www.cleverbot.com/getreply'

  def get(self, data):
    with requests.get(self.url + '?' + data) as resp:
      return resp.json()['output']
```

## Hosting

To use this, you would of course need to host it somewhere. Personally, I like
[Heroku](https://www.heroku.com) since it's free, but there are other options,
and if you just run the script `request.py` you can host it locally at
`127.0.0.1:5000`
