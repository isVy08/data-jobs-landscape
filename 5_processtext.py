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

# Delete duplicated entries with dulicated company & description 

idx = data[data.duplicated(subset=['company','description_v2'])].index #in case of no dups, index is null 
data = data.drop(idx,axis=0).reset_index()

# Convert to Raw text 
data['raw_desc'] = data['description_v2'].apply(remove_html)

# Get Years of Experience 
    # Remove relatives of Year 
p = re.compile('years old|yearly|year-round')
data['exp_year'] = data['raw_desc'].str.replace(p,'')
data['exp_year'] = data['raw_desc'].str.extract(r'(\d+\s*-\s*\d+|\d+\+?)(?= year)')

def check_invalid(x):
    try: 
        if '-' in x:
            low = re.match(r'(\d+)(?=\s?-)',x).group()
            upper = re.search(r'(\d+)',x.replace(low,'')).group()
        else: 
            upper = "0"
            low = re.search(r'(\d+)',x).group()
        
        if int(low) >  15 or int(upper) > 15:
            return np.nan 
        else: 
            return x 
    except: 
        if x is None:
            return np.nan
        else: 
            return x
    
        
data['exp_year'] = data['exp_year'].apply(check_invalid)        
        
s = data['exp_year'].apply(check_invalid)       
s.unique()
data[data['exp_year']=='20161-2']['raw_desc']


data.raw_desc[9610]


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

















# Clean text 

def clean_text(text): 
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
df3 = data[(data['job_requirement']=='0')&(data['job_description']=='0')][['title_v3','country','exp_level_v2','job_type_v2','raw_desc']]

df1['job_description'] = df1['job_description'].apply(clean_text) 
df2['job_requirement'] = df2['job_requirement'].apply(clean_text) 
df3['general'] = df3['description_v2'].apply(clean_text)  

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


# Word count 

data = pd.read_excel('desc_text.xlsx',sheet_name = 0,index_col=0)


data.loc['Data Scientist']



















