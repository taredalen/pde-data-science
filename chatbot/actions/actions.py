# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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
from typing import Any, Text, Dict, List


from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import os

class ActionGetCinemaNear(Action):
    def name(self) -> Text:
        return "action_get_cinema_near"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        confirm_address = tracker.get_slot("confirm_address")
        if confirm_address == False:
            dispatcher.utter_message("Do you want to restart ?")
            return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None), SlotSet("confirm_address", None)]

        country = tracker.get_slot("country")
        city = tracker.get_slot("city")
        address = tracker.get_slot("address")

        geolocator = Nominatim(user_agent="pde-data-science")
        location = geolocator.geocode(f"{address}, {city}, {country}")
        if location == None:
            dispatcher.utter_message("I am sorry, I could not find where you live, maybe you made a mistake ?")
            return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None), SlotSet("confirm_address", None)]
            
        df = pd.read_csv(os.getcwd() + "/csv/data.csv", delimiter=";")
        dispatcher.utter_message("I am looking for the nearest cinema to your location, this can take a bit of time, please be patient")
        cinema_near = []

        for i in range(df.shape[0]):
            try: 
                dist = geodesic((df.loc[i, "Y"], df.loc[i, "X"]), (location.latitude, location.longitude)).km
            except:
                continue
            
            if dist <= 5:
                cinema = geolocator.reverse(f"{df.loc[i, 'Y']}, {df.loc[i, 'X']}")
                cinema_near.append((dist, cinema, df.loc[i, 'website']))


        cinema_near.sort(key= lambda x: x[0])

        nearest = cinema_near[:8]

        if len(nearest) == 0:
            dispatcher.utter_message("I am sorry, there are no cinema near you")
            return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None), SlotSet("confirm_address", None)]

        data = []

        for cinema in nearest:
            #dispatcher.utter_message(f"This cinema is near:\n{cinema[1]}\n{cinema[2]}")
            data.append({"title": cinema[1].raw["display_name"].split(',')[0], "description":cinema[1].raw["display_name"]})

        message = {"payload": "collapsible", "data": data}

        dispatcher.utter_message(text="Here are the cinemas, from nearest to farthest:\n",json_message=message)

        return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None), SlotSet("confirm_address", None)]