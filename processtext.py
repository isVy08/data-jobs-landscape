#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:09:34 2020

@author: vyvo
"""

from dependency import *
from cleantext import * 

data = pd.read_csv("datafull.csv")

data.info() 

# Get title 


def to_title(x):
   global title 
   title = {
    "Machine Learning Engineer" : 'machine learning|nlp|natural language processing|recognition|image|computer vision',
    "Software Engineer" : r'(?=.*\bsoftware\b)(?=.*\bsengineer\b).*',    
    "Data Scientist" : r'(?=.*\bdata|\b)(?=.*\bscien\w*\b).*',
    "Data Engineer" : r'(?=.*\bdata|\b)(?=.*\bengineer|architect\b).*',
    "Analyst" : 'analyst|analysis|analytics|specialist',
    "Consultant" : 'consult|advisor',
    "Researcher" : "research\w*",
    "Big Data Developer" : r'(?=.*\bbig data|\b)(?=.*\bdevelop|program\w*\b).*',
    "Big Data Administrator" : r'(?=.*\bbig data|\b)(?=.*\badmin\w*\b).*',
    "Big Data Practitioner" : 'big data'
    
       }
   for k, val in title.items(): 
      val = re.compile(val)
      result = re.search(val,x.lower())
      if result is not None: 
          return k
   if 'big data' in x.lower():
       return 'Big Data Practitioner'
   else:
       return 'Others' 
        
data['gtitle'].value_counts()

