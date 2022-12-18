from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
import os
from tmdbv3api import TMDb, Movie, Discover
tmdb = TMDb()
movie = Movie()
discover = Discover()
import movie_title_fct
tmdb.api_key = os.getenv('TMDB_API_KEY')

# in any function

class MovieSearch(Action):
    def name(self) -> Text:
        return "action_movie_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_plot = next(tracker.get_latest_entity_values("plot"), None)
        print("plot detected", current_plot)
        if not current_plot:
            msg = "It seems you haven't written any plot for me to look up"
            dispatcher.utter_message(text=msg)
            return []
        # custom behavior
        msg = f"Plot {current_plot} received, commencing search"
        dispatcher.utter_message(text=msg)
        movie_guess=MovieTitleSearch(current_plot)
        msg = f"Is it {movie_guess} ?"
        dispatcher.utter_message(text=msg)
        return []


