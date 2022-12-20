import numpy as np
import pandas as pd
import os
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from tabulate import tabulate
from nltk import word_tokenize, WordNetLemmatizer
from nltk import pos_tag

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return 'v'
        #return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return 'n'
def preprocess(plot):
    #plot=plot.split()
    pos_tagged_plot=nltk.pos_tag(word_tokenize(plot))
    lemmatizer =WordNetLemmatizer()
    plot=[lemmatizer.lemmatize(word[0],get_wordnet_pos(word[1])) for word in pos_tagged_plot]
    return [word.lower() for word in plot]

stoplist = stopwords.words('english')
stop_punctuation = [':', '(', ')', '/', '|', ',',
                    '.', '*', '#', '"', '&', '~','...',
                    '-', '_', '\\', '@','?','!','\'']

def get_features_print(plot):
    return [ word for word in preprocess(plot) if word not in stoplist and word not in stop_punctuation]


def MoviePlotCSV(plot):
    pro_plot=get_features_print(plot)
    df_db= pd.read_csv( os.path.dirname(os.getcwd()) + "/csv/movie_plot_db.csv", sep=',')
    df_res = pd.DataFrame(data=None,columns=["Movie Title", "Accuracy",'Keywords found','Release Year'])
    df_res['Keywords found'] = df_db['Plot'].str.findall('|'.join(pro_plot))
    df_res['Movie Title']=df_db['Title']
    df_res['Release Year'] = df_db['Release Year']
    for i in range (len(df_res.index)):
        wordset=set(df_res.at[i,'Keywords found'])
        percent=100*(len(wordset)/len(set(pro_plot)))
        df_res['Accuracy'].loc[i]=percent
        df_res['Keywords found'].loc[i]=wordset
    df_res.sort_values(by='Accuracy', ascending=False,inplace=True,ignore_index=True)
    if (df_res['Accuracy'] == 0).all():
        return 1
    return tabulate(df_res[0:10], headers='keys', tablefmt='psql',showindex=False)
    



