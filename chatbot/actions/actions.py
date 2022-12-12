from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# in any function

def MovieTitleSearch(plot):

    firefox_profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.maximize_window()
    time.sleep(5)
    driver.get("https://www.google.com/")
    driver.execute_script("window.scrollTo(0, 50)")
    button = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.ID, "L2AGLb"))).click()
    element = driver.find_element(By.XPATH,value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    time.sleep(2)
    element.send_keys('movie about ' + plot + ' wikipedia')
    element.send_keys(Keys.ENTER)
    time.sleep(4)
    movie=driver.find_element(By.TAG_NAME,'h3').text
    if " - Wikipedia" in movie:
        movie.replace("- Wikipedia",'')
    print(movie)
    return movie


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

        msg = f"Plot [{current_plot}]received, commencing search"
        dispatcher.utter_message(text=msg)
        movie_guess=MovieTitleSearch(current_plot)
        msg = f"Is it [{movie_guess}]"
        dispatcher.utter_message(text=msg)
        return []