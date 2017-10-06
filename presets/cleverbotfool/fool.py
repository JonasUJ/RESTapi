class Fool:

    replace_chars = [
        '?', '.', ',', '!', '$', '^', '*', '(', ')', '\''
    ]

    fool = {
        'what anime is the image': 'Kimi no Na wa',
        'what is the artwork': 'Kimi no Na wa',
        'is college music a girl or a boy': 'Ask College Music',
        'is college music a boy or a girl': 'Ask College Music',
        'who is college music': 'The MVP of this stream',
        'do you like this song': 'Yes, I love this song and all other songs on this stream',
        'what playlist is this': 'http://lofi.collegemusic.co.uk/',
        'which playlist is this': 'http://lofi.collegemusic.co.uk/',
        'nourish or college music': 'College Music obviously!',
        'who’s better nourish or college music': 'College Music obviously!',
        'thoughts on ambition': 'new phone who dis?'
    }

    @classmethod
    def get(self, key):
        key = key.lower()
        for char in self.replace_chars:
            key = key.replace(char, '')

        return self.fool.get(key, None)
