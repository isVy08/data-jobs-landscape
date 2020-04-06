import requests
import re
import ast
import time
import unicodedata
import pandas as pd 
import numpy as np 
import pycountry as icy
from selenium import webdriver
from itertools import chain 
from bs4 import BeautifulSoup

#text processing package
#from contractions import CONTRACTION_MAP
#import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer

#nlp = spacy.load('en_core', parse=True, tag=True, entity=True)
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)
tokenizer = ToktokTokenizer()
nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('english')
#stopword_list.remove('no')
#stopword_list.remove('not')

pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)
