import os
import time
import random
import pandas as pd
from itertools import chain
from operator import itemgetter

from dotenv import load_dotenv
from tmdbv3api import TMDb, Movie, Discover, Search, Person

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import numpy as np
import os
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('corpus')
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from tabulate import tabulate
from nltk import word_tokenize, WordNetLemmatizer
from nltk import pos_tag


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

df_db = pd.read_csv(os.getcwd() + "/csv/movie_plot_pro.csv", sep=',')
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

def get_scores(score):
    rating = ''
    if score > 4.5:
        rating = '⭐️⭐️⭐️⭐️⭐️'
    if (score < 4.5) and (score >= 3.5):
        rating = '⭐️⭐️⭐️⭐️'
    if (score < 3.5) and (score >= 2.5):
        rating = '⭐️⭐️⭐️'
    if (score < 2.5) and (score >= 1.5):
        rating = '⭐️⭐️️'
    if score < 1.5:
        rating = '⭐️'
    return rating

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
            score = round(similar['vote_average'] / 10 * 5, 2)
            ratings = get_scores(score)

            if similar['poster_path'] is None:
                poster = 'https://www.themoviedb.org/assets/2/v4/glyphicons/basic/glyphicons-basic-38-picture-grey-c2ebdbb057f2a7614185931650f8cee23fa137b93812ccb132b9df511df1cfac.svg'
            else:
                poster = 'https://image.tmdb.org/t/p/original' + similar['poster_path']

            item = {'id': similar['id'], 'image': poster, 'title': title, 'ratings': ratings, 'score': score}
            recommendations.append(item)

        time.sleep(2)

        data = {'payload': 'cardsCarousel', 'data': sorted(recommendations, key=itemgetter('score'), reverse=True)}
        dispatcher.utter_message(json_message=data)


class ActionDirector(Action):
    def name(self) -> Text:
        return 'action_get_movie_recommendation_director_based'

    def run(self, dispatcher, tracker, domain):
        director_movies = []
        print('------------------------------')
        print(tracker.get_slot('director'))
        x = "query=" + tracker.get_slot('director')
        print(x)
        print('------------------------------')
        director = search.people({"query":tracker.get_slot('director')})
        director_credits = person.combined_credits(director[0]['id'])

        for credit in director_credits['crew']:
            if credit['job'] == 'Director':
                score = round(credit['vote_average'] / 10 * 5, 2)
                ratings = get_scores(score)

                if 'title' in credit:
                    title = credit['title']
                else:
                    title = credit['name']

                if credit['poster_path'] is None:
                    poster = 'https://www.themoviedb.org/assets/2/v4/glyphicons/basic/glyphicons-basic-38-picture-grey-c2ebdbb057f2a7614185931650f8cee23fa137b93812ccb132b9df511df1cfac.svg'
                else:
                    poster = 'https://image.tmdb.org/t/p/original' + credit['poster_path']

                item = {'id': credit['id'], 'image': poster, 'title': title, 'ratings': ratings, 'score': score}
                director_movies.append(item)

        time.sleep(2)
        data = {'payload': 'cardsCarousel', 'data': sorted(director_movies, key=itemgetter('score'), reverse=True)}
        dispatcher.utter_message(json_message=data)


class ActionInformation(Action):
    def name(self) -> Text:
        return 'action_get_movie_information'

    def run(self, dispatcher, tracker, domain):
        selected = movie.details(tracker.get_slot('id'))
        title = selected.title
        overview = selected.overview
        trailers = list(filter(lambda genre: genre['type'] == 'Trailer', selected.trailers['youtube']))
        link = 'https://youtube.com/embed/' + trailers[0]['source']
        response = "Title: {} \n\nOverview: {}\n".format(title, overview)
        time.sleep(2)

        msg = {"type": "video", "payload": {"title": "Link name", "src": link}}
        dispatcher.utter_message(text=response, attachment=msg)


class ActionGetCinemaNear(Action):
    def name(self) -> Text:
        return "action_get_cinema_near"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        confirm_address = tracker.get_slot("confirm_address")
        if confirm_address == False:
            dispatcher.utter_message("Do you want to restart ?")
            return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None),
                    SlotSet("confirm_address", None)]

        country = tracker.get_slot("country")
        city = tracker.get_slot("city")
        address = tracker.get_slot("address")

        geolocator = Nominatim(user_agent="pde-data-science")
        location = geolocator.geocode(f"{address}, {city}, {country}")
        if location == None:
            dispatcher.utter_message("I am sorry, I could not find where you live, maybe you made a mistake ?")
            return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None),
                    SlotSet("confirm_address", None)]

        df = pd.read_csv(os.getcwd() + "/csv/data.csv", delimiter=";")
        dispatcher.utter_message(
            "I am looking for the nearest cinema to your location, this can take a bit of time, please be patient")
        cinema_near = []

        for i in range(df.shape[0]):
            try:
                dist = geodesic((df.loc[i, "Y"], df.loc[i, "X"]), (location.latitude, location.longitude)).km
            except:
                continue

            if dist <= 5:
                cinema = geolocator.reverse(f"{df.loc[i, 'Y']}, {df.loc[i, 'X']}")
                cinema_near.append((dist, cinema, df.loc[i, 'website']))

        cinema_near.sort(key=lambda x: x[0])

        nearest = cinema_near[:8]

        if len(nearest) == 0:
            dispatcher.utter_message("I am sorry, there are no cinema near you")
            return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None),
                    SlotSet("confirm_address", None)]

        data = []

        for cinema in nearest:
            # dispatcher.utter_message(f"This cinema is near:\n{cinema[1]}\n{cinema[2]}")
            data.append(
                {"title": cinema[1].raw["display_name"].split(',')[0], "description": cinema[1].raw["display_name"]})

        message = {"payload": "collapsible", "data": data}

        dispatcher.utter_message(text="Here are the cinemas, from nearest to farthest:\n", json_message=message)

        return [SlotSet("country", None), SlotSet("city", None), SlotSet("address", None),
                SlotSet("confirm_address", None)]


# ----------------------------------------------------------------------------------------------------------------------

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return 'v'
        # return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return 'n'


def preprocess(pre_plot):
    # plot=plot.split()
    tokenizer = RegexpTokenizer(r'\w+')
    pos_tagged_plot = nltk.pos_tag(tokenizer.tokenize(pre_plot))
    lemmatizer = WordNetLemmatizer()
    l_plot = [lemmatizer.lemmatize(word[0], get_wordnet_pos(word[1])) for word in pos_tagged_plot]
    plot = [word.lower() for word in l_plot]
    stoplist = stopwords.words('english')
    return [word for word in plot if word not in stoplist and word not in stoplist]


def MoviePlotCSV(plot):
    pro_plot = preprocess(plot)
    print(pro_plot)
    #df_db = pd.read_csv(os.getcwd() + "/csv/movie_plot_pro.csv", sep=',')
    df_db['Keywords found'] = df_db['Pro Plot'].str.findall('|'.join(pro_plot))
    movies_found = []
    for i in range(len(df_db.index)):
        wordset = set(df_db.at[i, 'Keywords found'])
        percent = round(100 * (len(wordset) / len(set(pro_plot))), 2)
        df_db['Accuracy'] = percent
        name = df_db.at[i, 'Title']
        year = df_db.at[i, 'Release Year']
        wiki = df_db.at[i, 'Wiki Page']
        movies_found.append((str(percent), name, str(year), wiki))
        movies_found.sort(key=lambda x: x[0], reverse=True)
    acc_movies = movies_found[:8]
    return acc_movies


class MoviePlotSearch(Action):
    def name(self) -> Text:
        return "action_movie_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_plot = tracker.latest_message.get("text")
        if not current_plot or current_plot == '':
            msg = "It seems you haven't written any plot for me to look up"
            dispatcher.utter_message(text=msg)
            return []
        movies = MoviePlotCSV(current_plot)
        data = []
        for movie in movies:
            # dispatcher.utter_message(f"This cinema is near:\n{cinema[1]}\n{cinema[2]}")
            data.append(
                {"Title: ": movie[1] + ", " + movie[2] + ", Match: " + movie[0] + "%", "Description: ": movie[3]})

        message = {"payload": "collapsible", "data": data}
        dispatcher.utter_message(text="Here are the movies i found, from most accurate to least:\n",
                                 json_message=message)
        dispatcher.utter_message("Are any of those movies the one you were looking for ?")
        return []

