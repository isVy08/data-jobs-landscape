#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:35:43 2020

@author: vyvo
"""

import pandas as pd 
from bs4 import BeautifulSoup


data = pd.read_csv('dsjob_final.csv')

data.head()
data.info()

#ger raw text 
l = []
for desc in data.description:    
    parse = BeautifulSoup(desc,'lxml')
    extr = parse.find_all(['p','li'])
    result = [t.get_text().lower() for t in extr]
    result = '. '.join(result)
    try:
        if len(extr) < 3 or result.isalpha() == False: 
            l.append(parse.get_text().lower())
        else:
            l.append(result)            
    except: 
        l.append('Error')


l = pd.Series(l) 
l[l=='Error']
data['job_description'] = l 

data.info()
data.to_csv('linkedIn_dsjob.csv',index=False)


