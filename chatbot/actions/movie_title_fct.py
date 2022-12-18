import numpy as np
import pandas as pd
#Import nltk packages to manipulate text
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.metrics import ConfusionMatrix
from nltk.stem.snowball import SnowballStemmer

from nltk import word_tokenize, WordNetLemmatizer, PorterStemmer
from nltk import NaiveBayesClassifier, classify
from nltk import pos_tag
from nltk import ngrams
#***
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('omw-1.4')

from nltk import word_tokenize,sent_tokenize

# Let's add a path containing some useful nltk data
nltk.data.path += ['/mnt/share/nltk_data']
def get_wordnet_pos(pos_tag):
    """
    Modifies pos_tag to get a more general nature of word
    """
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
    stemmer = SnowballStemmer('english')
    return [stemmer.stem(word.lower()) for word in plot]

stoplist = stopwords.words('english')
stop_punctuation = [':', '(', ')', '/', '|', ',',
                    '.', '*', '#', '"', '&', '~','...',
                    '-', '_', '\\', '@','?','!','\'']

def get_features_print(plot):
    return [ word for word in preprocess(plot) if word not in stoplist and word not in stop_punctuation]

def MoviePlotCSV(plot):
    l_film=[]
    pro_plot=get_features_print(plot)
    print(pro_plot)
    df= pd.read_csv("wiki_movie_plots_deduped.csv", sep=',')
    df_s = pd.DataFrame(data=None, columns=df.columns)
    pattern = '|'.join(pro_plot)
    res=df["Plot"].str.contains(pattern)
    for i in range (len(res)):
        if res[i]==True:
            print(df.loc[i])
            l_film.append(df["Title"].loc[i])
    print(l_film)
