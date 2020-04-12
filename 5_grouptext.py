#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:09:34 2020

@author: vyvo
"""

import gc
gc.collect()

from dependency import *
from cleantext import * 

data = pd.read_csv("datafull.csv")
# Replace null value with Not Applicable 
data.fillna('Not Applicable',inplace=True)


# Categorize title 

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
        
data['title_v3'] = data['title_v2'].apply(to_title) 

f#or var in ['title_v3','country','exp_level_v2','job_type_v2']:
  #  print(data[data['title_v3']=='Data Scientist'][var].value_counts())

# Clean text 

def clean_text(text,html=False): 
    if html: 
        text = remove_html(text)
    text = remove_accented_chars(text)
    text = remove_special_characters(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    return text 

# Group text by each dimension TITLE / COUNTRY / EXP LEVEL / JOB TYPE: TEMPORARY+CONTRACT
 
def collect_text(data,attr,by,value): 
    """Returns a text of an attribute group by the value of another attribute"""
    s = data.loc[data[by]==value,attr]
    s = ' '.join(s)
    return s 

# Create non-null datasets 
df1 = data[data['job_description']!='0'][['title_v3','country','exp_level_v2','job_type_v2','job_description']]
df2 = data[data['job_requirement']!='0'][['title_v3','country','exp_level_v2','job_type_v2','job_requirement']]
df3 = data[(data['job_requirement']=='0')&(data['job_description']=='0')][['title_v3','country','exp_level_v2','job_type_v2','description_v2']]

df1['job_description'] = df1['job_description'].apply(clean_text) 
df2['job_requirement'] = df2['job_requirement'].apply(clean_text) 
df3['general'] = df3['description_v2'].map(lambda x: clean_text(x,html=True)) 

# Create an empty excel sheet first 
for sheet in ('title_v3','country','exp_level_v2','job_type_v2'):
    d = {}
    for val in data[sheet].unique():
        d[val] = []
        d[val].append(collect_text(df1,'job_description',sheet,val))
        d[val].append(collect_text(df2,'job_requirement',sheet,val))
        d[val].append(collect_text(df3,'general',sheet,val))
        finaldf = pd.DataFrame(d).T.rename(columns={0:'decription',1:'requirement',2:'general'})
    with pd.ExcelWriter('desc_text.xlsx',mode='a') as writer:
        finaldf.to_excel(writer,sheet_name=sheet)
