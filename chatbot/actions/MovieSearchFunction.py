"""from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from movie_title_fct import *


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
    element.send_keys('movie about ' + plot + 'wikipedia')
    element.send_keys(Keys.ENTER)
    time.sleep(4)
    movie=driver.find_element(By.TAG_NAME,'h3').text
    wiki= " Wikipedia "
    if wiki in movie:
        movie.replace(wiki,'')
    print(movie)
    return movie"""
