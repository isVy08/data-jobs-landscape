import requests
import ast
import time
import pandas as pd 
import numpy as np 
import pycountry as pcy
from selenium import webdriver
from itertools import chain 
from bs4 import BeautifulSoup

#text processing package
#from contractions import CONTRACTION_MAP


pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)
