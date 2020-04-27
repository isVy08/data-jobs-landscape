import ast
import time
import pandas as pd 
import numpy as np 
import scipy
#import pycountry as pcy
from itertools import chain

# Webdriver & HTML parsing 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# NLP
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams

# Gensim
from gensim.models import word2vec, doc2vec
from gensim.models.callbacks import CallbackAny2Vec


# Classifier
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# Adjust display settings 
pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)

