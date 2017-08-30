import csv
import os

import asyncio
import aiohttp
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXTS = {'avi', 'mp4', 'mkv'}

sem = asyncio.Semaphore(5)

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


async def get_http(url, params):
    async with sem:
        response = await aiohttp.request('get', url, params=params)
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        return soup


async def get_movie_details(movie):
    url = 'https://nova.rambler.ru/search'
    params = {'query': movie}
    soup = await  get_http(url, params)
    return soup

async def get_kinopoisk_url(movie):
    print('Started: {}'.format(movie))
    req = "{} {} {}".format(movie, 'фильм', 'kinopoisk.ru')
    soup = await get_movie_details(req)
    for tag in soup.find_all(lambda tag: 'b-serp-item__info' in tag.attrs.get('class', [])):
        url = tag.span.text
        if 'www.kinopoisk.ru/film/' in url:
            return movie, url

movies = list(get_movies("/media/kulik/TOSHIBA EXT/Movies"))
loop = asyncio.get_event_loop()
tasks = [loop.create_task(get_kinopoisk_url(movie)) for movie in movies]
combined_tasks = asyncio.wait(tasks)
loop.run_until_complete(combined_tasks)

with open('movies10.csv', 'w') as f:
    writer = csv.writer(f, delimiter='|')
    for task in tasks:
        movie, url = task.result()
        writer.writerow((movie, url))


