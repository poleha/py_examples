import asyncio
import csv
import os

import aiohttp
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTS = {'avi', 'mp4', 'mkv'}

YEAR_BREAKS = [str(year) for year in range(1940, 2018)]
BREAKS = ['[', '(', 'hdrip', 'bdrip', 'hdtvrip', 'unrated', 'xvid']

BREAKS += YEAR_BREAKS

semaphore = asyncio.Semaphore(5)


def filter_movie_files(files):
    return {' '.join(file.replace('_', ' ').replace('-', ' ').split('.')[:-1]) for file in files if
            file.split('.')[-1] in EXTS}


def get_movies(folder):
    movies = set()
    for dir_name, subdirs, files in os.walk(folder):
        current_movies = filter_movie_files(list(files) + list(subdirs))
        if dir_name != folder:
            continue
        movies.update(current_movies)
    return movies


async def http_get(url, params):
    response = await aiohttp.request('get', url, params=params)
    text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    return soup


async def get_movie_details(movie):
    url = 'https://nova.rambler.ru/search'
    params = {'query': movie}
    soup = await http_get(url, params=params)
    return soup


async def get_kinopoisk_details(movie):
    async with semaphore:
        req = "{} {} {}".format(movie, 'фильм', 'kinopoisk.ru')
        soup = await get_movie_details(req)
        for tag in soup.find_all(lambda tag: 'b-serp-item__link' in tag.attrs.get('class', [])):
            url = tag.attrs.get('href')
            if url and 'www.kinopoisk.ru/film/' in url:
                title = tag.text.replace("— КиноПоиск", '')
                title = title.replace("— смотреть онлайн", '')
                title = title.strip()
                try:
                    snippet = tag.parent.parent.p.text
                except:
                    snippet = ''
                print(url)
                return url, title, snippet


def correct_movie_names(movies):
    corrected_movies = set()
    for movie in movies:
        current_end_pos = len(movie)
        for br in BREAKS:
            pos = movie.lower().find(br.lower())
            if pos > 0:
                current_br = min(pos, current_end_pos)
        if current_br > 3:
            movie = movie[:current_br]
        movie = movie.replace('(', ' ')
        movie = movie.replace(')', ' ')
        movie = movie.replace('[', ' ')
        movie = movie.replace(']', ' ')
        movie = movie.replace("'", ' ')
        corrected_movies.add(movie)

    return corrected_movies


def main():
    movies = get_movies("/media/kulik/TOSHIBA EXT/Movies")
    movies = list(correct_movie_names(movies))[:2]

    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_kinopoisk_details(movie)) for movie in movies]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)


    """
    with open('movies10.csv', 'w') as f:
        writer = csv.writer(f, delimiter='|')
        for movie in movies:
            try:
                url, title, snippet = get_kinopoisk_details(movie)
            except:
                url, title, snippet = 'Not found', 'Not found', 'Not found'
            writer.writerow((movie, title, snippet, url))
            print(movie, title, url)
    """

main()
