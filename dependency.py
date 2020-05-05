import ast
import time
import pandas as pd 
import numpy as np 
import scipy
import os
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
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# visualize embeddings
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt 

# Adjust display settings 
pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)