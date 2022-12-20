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
        if not current_plot or current_plot=='':
            msg = "It seems you haven't written any plot for me to look up"
            dispatcher.utter_message(text=msg)
            return []
        dispatcher.utter_message("Plot received, commencing search through our database. This can take a bit of time.")
        movie_guess=MoviePlotCSV(current_plot)
        if movie_guess==1:
            dispatcher.utter_message("I'm sorry but there appears to be not movie in our database that match your plot. Do you want to give up?")
            return []
        dispatcher.utter_message(text=movie_guess)
        dispatcher.utter_message("Are any of those movies the one you were looking for ?")
        return []
        


