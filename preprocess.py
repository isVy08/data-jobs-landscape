#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:50:04 2020

@author: vyvo
"""
import re
import pandas as pd 
import numpy as np
import pycountry as pcy
import unicodedata
from googletrans import Translator
import ast

pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)


#1. read dataset
data = pd.read_csv('dsjob_final.csv')


#2.Remove records where description = 0 & set other '0' as null values  
data = data[data.description!='0'].reset_index()

for col in ['exp_level','job_func','industry','job_type']: 
    data[col] = data[col].map(lambda x: np.nan if x=='0' else x)
        
#3. LOCATION: get Country & Area

#extract Country from Link 
data['iso'] = data['link'].str.extract(r'https://([a-z]+)')
data['iso'] = data['iso'].map(lambda x: 'us' if x=='www' else x)

def to_country(x):
    if x == 'www':
        return 'United States'
    elif x == 'uk':
        return 'United Kingdom'
    else: 
        return (pcy.countries.get(alpha_2=x.upper()).name)

data['Country'] = data['Country'].apply(to_country)

#extract Area (State / City)  from Location 

nrow = data.shape[0]
loc = data['location'].str.split(', ') #split into list

for i in range(nrow): 
    #print(loc[i])
    if data['Country'][i] in loc[i] and len(loc[i])>1:
        loc[i].remove(data['Country'][i]) #remove 'Country' from the value

us_state = {
    'CA':'California','OR':'Oregon','GA':'Georgia','NY':'New York','MA':'Massachusetts',
    'PA':'Pennsylvania','AZ':'Arizona','TX':'Texas', 'IL':'Illinois','MN':'Minnesota'
    }
#normalize values of area 
def to_area(x): 
    if len(x) == 2:
        return us_state[x]
    elif 'Metropolitan' in x: 
        p = re.compile(r'(.*) Metropolitan') 
        return p.findall(x)[0]
    else: 
        return x
  
loc = loc.map(lambda x: x[-1])   
data['Area'] = loc.apply(to_area)

#4. EXP LEVEL/ JOB FUNC / INDUSTRY / JOB TYPE

#convert to List & get unique values for JOB FUNC / INDUSTRY 

data['job_func'] = data['job_func'].map(lambda x: ast.literal_eval(x) if x is not np.nan else x)
data['industry'] = data['industry'].map(lambda x: ast.literal_eval(x) if x is not np.nan else x)

func = []
inds = []

for i in range(nrow):
   try:
       func.extend(data['job_func'][i])
       inds.extend(data['industry'][i])
   except:
       pass             


#detect language 

foreign = ['China','Japan','France','Germany','Italy','Netherlands','Spain','Sweden','Switzerland']
d = {}
for country in foreign: 
    try:
        d[country] = []
        df = data[data.Country == country]
        for col in ['exp_level','job_func','job_type','industry']:
            try:
                d[country].extend(df[col].unique())
            except: 
                for val in df[col]:
                    l = list(filter(lambda x: x not in d[country],val))
                    d[country].extend(l)
    except:  
       pass

for country in foreign: 
    name = country+'.xlsx'
    pd.DataFrame(d[country]).to_excel(name,index=False)


#Translate to English using Google API (but with Limit!)   
def to_eng(x):
    trans = Translator()
    try: 
        return(trans.translate(x,dest='en').text)
    except:
        return(np.nan)


 


