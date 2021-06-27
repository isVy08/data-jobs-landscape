import ast
import time
import pandas as pd 
import numpy as np 
import scipy
import os
import pycountry as pcy
from itertools import chain

# Webdriver & HTML parsing 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Text processing
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams


# Adjust display settings 
pd.set_option('display.max_columns',500)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_colwidth',1000)