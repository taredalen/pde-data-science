import os
import random
from itertools import chain

from dotenv import load_dotenv

from tmdbv3api import TMDb, Movie, Discover

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

load_dotenv()

tmdb = TMDb()
movie = Movie()
discover = Discover()

tmdb.api_key = os.getenv('TMDB_API')

genres_list = [
    {'id': 28, 'name': 'Action'},
    {'id': 12, 'name': 'Adventure'},
    {'id': 16, 'name': 'Animation'},
    {'id': 35, 'name': 'Comedy'},
    {'id': 80, 'name': 'Crime'},
    {'id': 99, 'name': 'Documentary'},
    {'id': 18, 'name': 'Drama'},
    {'id': 10751, 'name': 'Family'},
    {'id': 14, 'name': 'Fantasy'},
    {'id': 36, 'name': 'History'},
    {'id': 27, 'name': 'Horror'},
    {'id': 10402, 'name': 'Music'},
    {'id': 9648, 'name': 'Mystery'},
    {'id': 10749, 'name': 'Romance'},
    {'id': 878, 'name': 'Science Fiction'},
    {'id': 10770, 'name': 'TV Movie'},
    {'id': 53, 'name': 'Thriller'},
    {'id': 10752, 'name': 'War'},
    {'id': 37, 'name': 'Western'}
]


# ----------------------------------------------------------------------------------------------------------------------

class Movie:
    def __init__(self, description, title):
        self._description = description

    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value


def get_movie_by_genres(genres):
    movies = discover.discover_movies({'with_genres': genres})
    random_movie = random.choice(movies)

    title = random_movie.title
    poster = 'https://image.tmdb.org/t/p/original' + random_movie.poster_path
    overview = random_movie.overview
    current_movie.set_description(overview)

    return title, poster


current_movie = Movie('description', 'title')


# ----------------------------------------------------------------------------------------------------------------------

class ActionRecommendMovie(Action):
    def name(self) -> Text:
        return 'action_get_movie_recommendation'

    def run(self, dispatcher, tracker, domain):
        poster, title = get_movie_by_genres(35)
        dispatcher.utter_message(poster, title)


class ActionDescription(Action):
    def name(self) -> Text:
        return 'action_get_movie_description'

    def run(self, dispatcher, tracker, domain):
        description = current_movie.get_description()
        dispatcher.utter_message(description)


class ActionGenres(Action):
    def name(self) -> Text:
        return 'action_get_movie_recommendation_genre_based'

    def run(self, dispatcher, tracker, domain):
        selected_genres = []

        for word in str.split(tracker.latest_message['text']):
            match = list(filter(lambda genre: genre['name'].lower() == word.lower(), genres_list))
            selected_genres.append(match)

        list_of_genres = list(chain.from_iterable(selected_genres))
        genres_idx = list(k for d in list_of_genres for k in d.values() if isinstance(k, int))

       # genres_idx = list(k for d in list_of_genres for k in d.values())

        poster, title = get_movie_by_genres(genres_idx)

        print(genres_idx)
        print(title)

        dispatcher.utter_message(poster, title)
