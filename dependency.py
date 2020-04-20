import ast
import time
import pandas as pd 
import numpy as np 
import pycountry as pcy
from itertools import chain

# Webdriver & HTML parsing 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Clean text 
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import WordNetLemmatizer

# Adjust display settings 
pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)
