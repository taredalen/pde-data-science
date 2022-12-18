import os
import time
import random
from itertools import chain
from operator import itemgetter

from dotenv import load_dotenv

from tmdbv3api import TMDb, Movie, Discover, Search, Person

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

load_dotenv()

tmdb = TMDb()
movie = Movie()
discover = Discover()
search = Search()
person = Person()

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

def get_movie_by_genres(genre):
    movies = discover.discover_movies({
        'with_genres': genre,
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 10
    })
    random_movie = random.choice(movies)

    title = random_movie.title
    poster = 'https://image.tmdb.org/t/p/original' + random_movie.poster_path
    overview = random_movie.overview
    current_movie.set_description(overview)

    return poster, title

current_movie = Movie('description', 'title')

# ----------------------------------------------------------------------------------------------------------------------
class ActionRecommendMovie(Action):
    def name(self) -> Text:
        return 'action_get_movie_recommendation'

    def run(self, dispatcher, tracker, domain):
        time.sleep(2)

        poster, title = get_movie_by_genres(35)
        dispatcher.utter_message(title, poster)

class ActionDescription(Action):
    def name(self) -> Text:
        return 'action_get_movie_description'

    def run(self, dispatcher, tracker, domain):
        time.sleep(2)

        description = current_movie.get_description()
        dispatcher.utter_message(description)

class ActionGenres(Action):
    def name(self) -> Text:
        return 'action_get_movie_recommendation_genre_based'

    def run(self, dispatcher, tracker, domain):
        time.sleep(2)

        selected_genres = []

        for word in str.split(tracker.latest_message['text']):
            match = list(filter(lambda genre: genre['name'].lower() == word.lower(), genres_list))
            selected_genres.append(match)

        list_of_genres = list(chain.from_iterable(selected_genres))
        genres_idx = list(k for d in list_of_genres for k in d.values() if isinstance(k, int))

        poster, title = get_movie_by_genres(genres_idx[0])
        dispatcher.utter_message(title, poster)


class ActionSimilar(Action):
    def name(self) -> Text:
        return 'action_get_movie_recommendation_title_based'

    def run(self, dispatcher, tracker, domain):
        recommendations = []

        search_film = movie.search(tracker.get_slot('film'))
        first_result = sorted(search_film, key=itemgetter('popularity'), reverse=True)

        similar_movies = movie.recommendations(first_result[0].id)

        for similar in similar_movies:
            title = similar['title']
            ratings = (round(similar['vote_average'] / 10 * 5, 2))

            if similar['poster_path'] is None:
                poster = 'https://www.themoviedb.org/assets/2/v4/glyphicons/basic/glyphicons-basic-38-picture-grey-c2ebdbb057f2a7614185931650f8cee23fa137b93812ccb132b9df511df1cfac.svg'
            else:
                poster = 'https://image.tmdb.org/t/p/original' + similar['poster_path']

            item = {'image': poster, 'title': title, 'ratings': ratings}
            recommendations.append(item)

        time.sleep(2)

        data = {'payload': 'cardsCarousel', 'data': sorted(recommendations, key=itemgetter('ratings'), reverse=True)}
        dispatcher.utter_message(json_message=data)
