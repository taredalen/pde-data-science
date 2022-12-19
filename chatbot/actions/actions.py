from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
from movie_title_fct import MoviePlotCSV

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
        msg = f"Plot received, commencing search through our databse"
        dispatcher.utter_message(text=msg)
        movie_guess=MoviePlotCSV(current_plot)
        dispatcher.utter_message(text=movie_guess)
        msg="Are any of those movies the one you were looking for ?"
        dispatcher.utter_message(text=msg)
        return []
        


