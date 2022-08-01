import requests
from lxml import html

page = requests.get('https://puzzle-english.com/directory/1000-popular-words')
tree = html.fromstring(page.content.decode())
mass = []


def get_word():
    for i in enumerate(tree.xpath('//li')):
        try:
            mass.append(i[1][0].text + i[1][1].text + i[1][2].text)
        except Exception:
            pass
    return mass


