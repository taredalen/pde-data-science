import os
from dotenv import load_dotenv

from tmdbv3api import TMDb
from tmdbv3api import Movie

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

load_dotenv()

tmdb = TMDb()
movie = Movie()
tmdb.api_key = os.getenv("TMDB_API")


class ActionHelloWorld(Action):

    def name(self) -> Text:
         return "action_get_movie_recommendation"

    def run(self, dispatcher, tracker, domain):

        search = movie.search("Corpse Bride")

        first_result = search[0]

        #response = 'https://image.tmdb.org/t/p/original' + first_result.poster_path
        response = tracker.latest_action_name
        dispatcher.utter_message(response)


