import requests
import ast
import time
import pandas as pd 
import numpy as np 

import pycountry as pcy
from selenium import webdriver
from itertools import chain 
from bs4 import BeautifulSoup

import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import WordNetLemmatizer

#from contractions import CONTRACTION_MAP

#import spacy
#nlp = spacy.load('en_core', parse=True, tag=True, entity=True)
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)


pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)
