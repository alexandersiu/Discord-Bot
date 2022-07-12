from bs4 import BeautifulSoup
import requests
import random
import re

class RandomAnime:
    def __init__(self):
        self.url = 'https://myanimelist.net/topanime.php?limit=' + str(random.randint(0, 1000))
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, 'lxml')

        self.run()

    def get_anime(self):
        self.page_soup = self.soup.find_all('tr', {'class' : 'ranking-list'})[0]
        self.regex_search = re.compile('href=.+id')
        self.anime_url = re.search(self.regex_search, str(self.page_soup))
        self.anime_url = str(self.anime_url.group(0))[:-4]
        self.anime_url = self.anime_url[6:]

        return self.anime_url
    
    def anime_page(self):
        self.anime_html = requests.get(self.anime_url).text
        self.anime_soup = BeautifulSoup(self.anime_html, 'lxml')

    def anime_title(self):
        self.title = self.anime_soup.find('h1', {'class' : 'title-name h1_bold_none'})

        return self.title.text

    def anime_thumbnail(self):
        self.thumbnail_html = self.anime_soup.find('div', {'style' : 'text-align: center;'})
        self.regex = re.compile('src=\".+" ')
        self.thumbnail_url = re.search(self.regex, str(self.thumbnail_html))
        self.thumbnail_url = str(self.thumbnail_url.group(0))[:-2]
        self.thumbnail_url = self.thumbnail_url[5:]

        return self.thumbnail_url

    def anime_rating(self):
        self.rating = self.anime_soup.find('span', {'class' : 'numbers ranked'})

        return self.rating.text

    def anime_synopsis(self):
        self.synopsis = self.anime_soup.find('p', {'itemprop' : 'description'})
        self.synopsis = str(self.synopsis.text)[:1024]

        return self.synopsis

    def run(self):
        self.get_anime()
        self.anime_page()
        self.anime_title()
        self.anime_thumbnail()
        self.anime_synopsis()
