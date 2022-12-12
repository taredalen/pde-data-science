import os
import random

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

class Movie:
    def __init__(self, description, title):
        self._description = description

    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value

current_movie = Movie('description', 'title')

class ActionRecommendMovie(Action):
    def name(self) -> Text:
         return 'action_get_movie_recommendation'

    def run(self, dispatcher, tracker, domain):
        comedies = discover.discover_movies({'with_genres': 35}) # comedy
        random_comedy = random.choice(comedies)

        title = random_comedy.title
        poster = 'https://image.tmdb.org/t/p/original' + random_comedy.poster_path
        overview = random_comedy.overview
        current_movie.set_description(overview)

        dispatcher.utter_message(title, poster)

class ActionDescription(Action):
    def name(self) -> Text:
         return 'action_get_movie_description'

    def run(self, dispatcher, tracker, domain):
        description = current_movie.get_description()
        dispatcher.utter_message(description)