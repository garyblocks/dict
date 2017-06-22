# author: Gary Wang
# date: 2017.6
import requests
import sys

class dict(object):

    def __init__(self):
        self.app_id  = 'ce930943'
        self.app_key = 'ca5112897fe7de140a40c2efee87a6ed'
        self.lang    = 'en'
        self.base    = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'

    def find(self, entry, path):
        cur = entry
        for i in path:
            if isinstance(i, str):
                if i in cur:
                    cur = cur[i]
                else:
                    return ''
            else:
                if cur:
                    cur = cur[0]
                else:
                    return ''
        return cur

    def parse(self, entry):
        res = {}
        res['category'] = self.find(entry, ['lexicalCategory'])
        res['def'] = self.find(entry, ['entries', 0, 'senses', 0, 'definitions', 0])
        res['ex'] = self.find(entry, ['entries', 0, 'senses', 0, 'examples', 0, 'text'])
        res['pronun'] = self.find(entry, ['pronunciations', 0, 'phoneticSpelling'])
        return res

    def run(self, word):
        url       = self.base + self.lang + '/' + word.lower()
        response  = requests.get(url, headers={'app_id': self.app_id, 'app_key': self.app_key})
        http_code = response.status_code
        if http_code == 404:
            print('word "' + word + '" not found')
            return
        elif http_code != 200:
            print("Can't access oxford dictionaries services.")
            print("Http error: " + str(http_code))
        # print("text \n" + response.text)
        data = response.json()
        head = '\033[93m\033[1m' + word + '\033[0m'
        output = ''
        sounds = set()
        pronun = ' \033[94m\033[3m['
        for entry in data['results'][0]['lexicalEntries']:
            info = self.parse(entry)
            if info['pronun'] not in sounds and info['pronun']:
                sounds.add(info['pronun'])
                if len(sounds) > 1:
                    pronun += ', '
                pronun += info['pronun']
            output += '\033[91m[' + info['category'] + '] \033[0m' + info['def'] + '\n'
            output += '\033[92m\033[2m[e.g.] ' + info['ex'] + '\033[0m\n'
        print(head + pronun + ']\033[0m\n')
        print(output)

if __name__ == '__main__':
    d = dict()
    if len(sys.argv) == 1:
        print('No input word. e.g. dict hello world')
    for word in sys.argv[1:]:
        d.run(word)
