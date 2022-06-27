from bs4 import BeautifulSoup
import requests
import random
import re

class Webtoon:
    def __init__(self):

        #random elements
        self.random_page = random.randint(1, 40)
        self.random_element = random.randint(0, 35)

        #bs4 setup on all webtoons
        self.url = 'https://hiperdex.com/page/' + str(self.random_page) + '/'
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, 'lxml')

        self.run()

    def webtoon_title(self):
        self.title = self.soup.find_all('h3', {'class': 'h5'})
        self.name = self.title[self.random_element]
        return self.name.text

    def webtoon_url(self):
        self.regex_search = re.compile('https.+\/\"')
        self.wt_url = re.search(self.regex_search, str(self.name))
        self.wt_url = str(self.wt_url.group(0))[:-1]
        return self.wt_url

    def webtoon_page(self):
        self.selected_webtoon_html = requests.get(self.wt_url).text
        self.selected_webtoon_soup = BeautifulSoup(self.selected_webtoon_html, 'lxml')

    def webtoon_img(self):
        self.img_html = self.selected_webtoon_soup.find_all('a', {'href' : self.wt_url})
        self.img_regex_search = re.compile('https.+\.(jpg|png|webp|jpeg)\"')
        self.img_url = re.search(self.img_regex_search, str(self.img_html))
        self.img_url = str(self.img_url.group(0))[:-1]
        return self.img_url

    def webtoon_rating(self):
        self.rating = self.selected_webtoon_soup.find('span', {'property' : 'ratingValue'})
        return self.rating.text

    def webtoon_summary(self):
        self.summary = self.selected_webtoon_soup.find('div', {'class' : 'summary__content'})
        return self.summary.text

    def run(self):
        self.webtoon_title()
        self.webtoon_url()
        self.webtoon_page()
        self.webtoon_img()
        self.webtoon_rating()
        self.webtoon_summary()