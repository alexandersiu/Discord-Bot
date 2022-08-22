from bs4 import BeautifulSoup
from AnilistPython import Anilist
import requests
import random
import re

#this class will probe the myanimelist top 1500 most popular animes and will randomly output information about one of them
class RandomAnime:
    def __init__(self):
        self.url = 'https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(random.randint(0, 1500)) #procure url of the random anime
        self.html = requests.get(self.url).text #receives the html of said page
        self.soup = BeautifulSoup(self.html, 'lxml')

        self.run()

    #with the randomly generated anime on the top of the main MAL popularity page, we need the specific url of the anime
    def get_anime(self):
        self.page_soup = self.soup.find_all('tr', {'class' : 'ranking-list'})[0]
        self.regex_search = re.compile('href=.+id')
        self.anime_url = re.search(self.regex_search, str(self.page_soup))
        self.anime_url = str(self.anime_url.group(0))[:-4]
        self.anime_url = self.anime_url[6:]

        return self.anime_url

    #receives the html of the random anime url
    def anime_page(self):
        self.anime_html = requests.get(self.anime_url).text
        self.anime_soup = BeautifulSoup(self.anime_html, 'lxml')

    #outputs the title of the random anime
    def anime_title(self):
        self.title = self.anime_soup.find('h1', {'class' : 'title-name h1_bold_none'})
        
        return self.title.text
    
    #outputs the english title of the random anime if there is one
    def anime_title_eng(self):
        self.title_eng = self.anime_soup.find('p', {'class' : 'title-english title-inherit'})
        if self.title_eng == None:
            return False
        else:
            return self.title_eng.text

    #outputs the anime thumbnail of the random anime
    def anime_thumbnail(self):
        self.thumbnail_html = self.anime_soup.find('div', {'style' : 'text-align: center;'})
        self.regex = re.compile('src=\".+" ')
        self.thumbnail_url = re.search(self.regex, str(self.thumbnail_html))
        self.thumbnail_url = str(self.thumbnail_url.group(0))[:-2]
        self.thumbnail_url = self.thumbnail_url[5:]

        return self.thumbnail_url

    #outputs the anime rating of the random anime
    def anime_rating(self):
        self.rating = self.anime_soup.find('span', {'class' : 'numbers ranked'})

        return self.rating.text

    #outputs the anime popularity of the random anime
    def anime_popularity(self):
        self.popularity = self.anime_soup.find('span', {'class' : 'numbers popularity'})

        return self.popularity.text


    #outputs a synopsis of the random anime
    def anime_synopsis(self):
        self.synopsis = self.anime_soup.find('p', {'itemprop' : 'description'})
        self.synopsis = str(self.synopsis.text)[:1024]

        return self.synopsis

    #runs all of the functions
    def run(self):
        self.get_anime()
        self.anime_page()
        self.anime_title()
        self.anime_title_eng()
        self.anime_thumbnail()
        self.anime_rating()
        self.anime_popularity()
        self.anime_synopsis()

#this class will search for an anime based on the input from the user and output information about it
class AnimeSearch:
    def __init__(self, anime):
        self.anilist = Anilist() #uses the AniList library to search for the anime
        self.anime_dict = self.anilist.get_anime(anime) #receives a dictionary of the information about the anime

        self.anime_name_jp = self.anime_dict['name_romaji'] 
        if self.anime_name_jp == None:
            return False

        self.anime_cover_art = self.anime_dict['cover_image']
        self.anime_score = self.anime_dict['average_score']

        self.anime_genres = self.anime_dict['genres']
        self.anime_genres = ', '.join(map(str, self.anime_genres))

        self.anime_description = self.anime_dict['desc'][:1024]
        self.anime_description = self.anime_description.replace('<br>', '')
        self.anime_description = self.anime_description.replace('<i>', '')
