import csv
import os
import requests
from bs4 import BeautifulSoup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTS = {'avi', 'mp4', 'mkv'}
def filter_movie_files(files):
    return {' '.join(file.replace('_', ' ').replace('-', ' ').split('.')[:-1]) for file in files if file.split('.')[-1] in EXTS}
def get_movies(folder):
    movies = set()
    for dir_name, subdirs, files in os.walk(folder):
        current_movies = filter_movie_files(files)
        if dir_name != folder and len(current_movies) > 2:
            continue
        movies.update(current_movies)
    return movies
def http_get(url, params):
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
def get_movie_details(movie):
    url = 'https://nova.rambler.ru/search'
    params = {'query': movie}
    soup = http_get(url, params=params)
    return soup
def get_kinopoisk_url(movie):
    req = "{} {} {}".format(movie, 'фильм', 'kinopoisk.ru')
    soup = get_movie_details(req)
    for tag in soup.find_all(lambda tag: 'b-serp-item__info' in tag.attrs.get('class', [])):
        url = tag.span.text
        if 'www.kinopoisk.ru/film/' in url:
            return url
def get_kinopoisk_soup(url):
    return http_get('https://' + url, {})
def tag_finder(prop_name, prop_value):
    def _tag_finder(tag, ):
        return prop_value in tag.attrs.get(prop_name, [])
    return _tag_finder
def parse_kinopoisk(soup):
    try:
        title = soup.find_all(tag_finder('itemprop', 'name'))[0].text
    except:
        title = ""
    try:
        rating = soup.find_all(lambda tag: 'rating_ball' in tag.attrs.get('class', []))[0].text
    except:
        rating = ""
    try:
        genre_tag = soup.find_all(lambda tag: 'genre' in tag.attrs.get('itemprop', []))[0]
        genre = ", ".join([a.text for a in genre_tag.find_all('a')])
    except:
        genre = ""
    try:
        starring_tag = soup.find_all(lambda tag: 'actors' in tag.attrs.get('itemprop', []))[0].parent
        starring = ", ".join([a.text for a in starring_tag.find_all('a')])
    except:
        starring = ""
    try:
        description = soup.find_all(lambda tag: 'description' in tag.attrs.get('itemprop', []))[0].text
    except:
        description = ""
    return title, rating, genre, starring, description
def main():
    movies = list(get_movies("/media/kulik/TOSHIBA EXT/Movies"))
    with open('movies4.csv', 'w') as f:
        writer = csv.writer(f, delimiter='|')
        for movie in movies:
            url = get_kinopoisk_url(movie)
            writer.writerow((movie, url))
            print(movie, url)
            continue
            if url:
                soup = get_kinopoisk_soup(url)
                title, rating, genres, starring, description = parse_kinopoisk(soup)
                writer.writerow([title, movie, url, rating, genres, starring, description])
                print([title, movie, url, rating, genres, starring, description])
            else:
                print('NOT FOUND', movie)
main()
