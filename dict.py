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
        print(word)
        for entry in data['results'][0]['lexicalEntries']:
            print(entry['lexicalCategory'] + ". " + entry['entries'][0]['senses'][0]['definitions'][0])
            print("example: " + entry['entries'][0]['senses'][0]['examples'][0]['text'])
            print("pronunciations: " + entry['pronunciations'][0]['phoneticSpelling'])

if __name__ == '__main__':
    d = dict()
    if len(sys.argv) == 1:
        print('No input word. e.g. dict hello world')
    for word in sys.argv[1:]:
        d.run(word)
