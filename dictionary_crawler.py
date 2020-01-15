import urllib

from bs4 import BeautifulSoup
import requests
import json


class DictionaryCrawler:
    def get_meaning(self, word):
        r = requests.get(
            "https://www.synonym.com/synonyms/{}".format(word),
            proxies=urllib.request.getproxies(),
        )
        soup = BeautifulSoup(r.text, "html.parser")
        span = soup.find("meta", property="og:description")
        res = span.extract()['content']
        res = res.split('|')
        definition = synonym = antonym = meaning = ""
        if len(res) > 0:
            meaning = res[0]
        if len(res) > 1 and ":" in res[1]:
            definition = res[1].split(":")[1]
        if len(res) > 2 and ":" in res[1]:
            synonym = res[2].split(":")[1]
        if len(res) > 3 and ":" in res[1]:
            antonym = res[3].split(":")[1]
        print(word)
        di = {
            "meaning": meaning,
            "definition": definition,
            "synonym": synonym,
            "antonym": antonym,
            "language": "en",
            "code": word[0] + str(len(word)),
            "advance_code": word[0] + str(len(word)) + word[-1].lower()
        }
        return di


if __name__ == '__main__':
    response_json = []
    failed = []
    with open("words.json", "r") as f:
        data = json.loads(f.read())
        for item in data['rows']:
            res = DictionaryCrawler().get_meaning(item['id'])
            if res['definition']:
                res['word'] = item['id']
                print(res)
                response_json.append(res)
            else:
                failed.append(item['id'])
            break
    with open("output.json", "a+") as fi:
        fi.write(str(json.dumps(response_json)))
    with open("failed.json", "a+") as fi:
        fi.write(str(json.dumps(failed)))
