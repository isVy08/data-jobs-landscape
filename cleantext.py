#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:21:32 2020

@author: vyvo
"""

import unicodedata 
from googletrans import Translator
from bs4 import BeautifulSoup


#Remove accented characters 
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, ' ', text)
    return text

def remove_html(text):
    parse = BeautifulSoup(text,'lxml')
    return parse.get_text()

#Translate to English using Google API (but with Limit!)   
def to_eng(x):
    trans = Translator()
    try: 
        return(trans.translate(x,dest='en').text)
    except:
        return(np.nan)
    
#extract excel file of text to be translated 

def get_file(df,filename): #text is a DataFrame of columns = attributes to be translated
    df.to_excel(filename,index=False)

