"""# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# This is a simple example for a custom action which utters "Hello World!"
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
git push --set-upstream origin movie_finder
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class MovieSearch(Action):
    def name(self) -> Text:
        return "action_movie_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_plot = next(tracker.get_latest_entity_values("plot"), None)

        if not current_plot:
            msg = "It seems you haven't written any plot for me to look up"
            dispatcher.utter_message(text=msg)
            return []
        # custom behavior
        msg = f"Plot [{current_plot}]received, commencing search"
        dispatcher.utter_message(text=msg)
        return []
