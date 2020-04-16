#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:55:07 2020

@author: vyvo
"""
import gc 
gc.collect()

from dependency import *
from cleantext import * 

data = pd.read_csv("datafull.csv")
# Handle Null values & Duplication
data.fillna('Not Applicable',inplace=True)
idx = data[data.duplicated(subset=['company','description_v2'])].index 
data = data.drop(idx,axis=0).reset_index()

subdata = data[data.title_v3.isin(['Data Scientist','Data Analyst'])]


# =============================================================================
# # Create subset for Tableau visualization
# data[['list_time','title_v3','country','area','exp_level_v2','job_type_v2']].to_excel("vizdata.xlsx",index=False)
# 
# # Aggregate INDUSTRY for Tableau visualization 
# subdata['industry_v2'] = subdata['industry_v2'].map(lambda x: ast.literal_eval(x) if x!= "Not Applicable" else [x])
# col = list(subdata.industry_v2)
# col = pd.Series(chain(*col))
# nrow = subdata.shape[0]
# 
# keep = col.value_counts().head(21).index 
# col = col.map(lambda x: x if x in keep else 'Others').value_counts()/nrow
# pd.DataFrame(col,columns=['Industry']).to_excel('vizindustry.xlsx')
# 
# =============================================================================



subdata['raw_desc'] = subdata['description_v2'].apply(remove_html)

# Derive MIN_EXP
 
def exp(x):
    if x in ('Entry level','internship'):
        return 'Entry level'
    elif x in ('mid-senior level','director'):
        return 'Senior'
    else: 
        return x.capitalize() 
subdata['exp_level_v3'] = subdata.exp_level_v2.apply(exp)

    # Remove relatives of Year 
p = re.compile('years old|yearly|year-round')
subdata['exp_year'] = subdata['raw_desc'].str.replace(p,'')
subdata['exp_year'] = subdata['raw_desc'].str.extract(r'(\d+\s*-\s*\d+|\d+\+?)(?= year)')

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
            return int(low) 
    except: 
        return np.nan
    
subdata['exp_year'] = subdata['exp_year'].apply(check_invalid)        
subdata['exp_year'].groupby(subdata['title_v3']).median()


# Derive MIN DEGREE
def min_degree(x):
    pattern = ['bachelor|undergraduate','master','phd','postgraduate']
    i = 0 
    m = None 
    while m is None and i < len(pattern): 
        p = re.compile(pattern[i])
        m = re.search(p,x)
        i +=1
    if m is None: 
        return "Not mention"
    else: 
        result = m.group().capitalize() 
        if result == "Postgraduate": 
            return "Master"
        elif result == "Undergraduate":
            return "Bachelor"
        else: 
            return result
        
subdata['min_degree'] = subdata['raw_desc'].apply(min_degree)
subdata['min_degree'].groupby(subdata.exp_level_v3).value_counts()

file = subdata[['title_v3','exp_level_v3','exp_year','min_degree']]
file.to_csv('extraviz.csv',index=False) 

