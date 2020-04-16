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

# Fill null values and delete duplications 
data = pd.read_csv("datafull.csv")
data.fillna('Not Applicable',inplace=True)
idx = data[data.duplicated(subset=['company','description_v2'])].index 
data = data.drop(idx,axis=0).reset_index()


data['industry_v2'] = data['industry_v2'].map(lambda x: ast.literal_eval(x) if x!= "Not Applicable" else [x])



# Convert to Raw text 
data['raw_desc'] = data['description_v2'].apply(remove_html)

# --------- Define functions ----------------

def clean_text(text): 
    text = remove_accented_chars(text)
    text = remove_special_characters(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    return text 

 
def collect_text(data,attr,by,value): 
    """Returns a text of an attribute group by the value(s) of another attribute"""
    if isinstance(value,list):
        s = data.loc[data[by].isin(value),attr]
    else:
        s = data.loc[data[by]==value,attr]
    s = ' '.join(s)
    return s 

def word_count(text,is_str=False): #text can be list or str
    if is_str:
        wordlist = text.split(" ")
    else: 
        wordlist = text 
    wordict = dict((x,wordlist.count(x)) for x in set(wordlist))
    freq = pd.DataFrame(wordict.values(),index = wordict.keys(),columns=["freq"])
    return freq 

# Combine exp level
def exp(x):
    if x in ('Entry level','internship'):
        return 'Entry level'
    elif x in ('mid-senior level','director'):
        return 'Senior'
    else: 
        return x.capitalize() 
    
def merge_word_count(text1,text2,max_freq=300):
    text1_count = word_count(text1,is_str=True)
    top = text1_count.sort_values(by="freq",ascending=False).head(max_freq)
    gen = text2.split(" ")
    gen = list(filter(lambda x: x in top.index,gen))
    gen = word_count(gen,is_str=False)
    finaldf = top.append(gen).sum(level=0)
    return finaldf
    
def subset(df1,df2,df3,df4,by='title_v3',valueList=['Data Scientist','Data Analyst']):
    df1 = df1[df[by].isin(valueList)]
    df2 = df2[df[by].isin(valueList)]
    df3 = df3[df[by].isin(valueList)]
    df4 = df4[df[by].isin(valueList)]
    return df1,df2,df3,df4 

# ---------------------------------------
# Combine exp level 
data['exp_level_v3'] = data.exp_level_v2.apply(exp)


# Create non-null datasets 
df1 = data[data['job_description']!='0'][['exp_level_v3','title_v3','job_description']]
df2 = data[data['job_requirement']!='0'][['exp_level_v3','title_v3','job_requirement']]
df3 = data[data['job_description']=='0'][['exp_level_v3','title_v3','raw_desc']]
df4 = data[data['job_requirement']=='0'][['exp_level_v3','title_v3','raw_desc']]

df1['job_description'] = df1['job_description'].apply(clean_text) 
df2['job_requirement'] = df2['job_requirement'].apply(clean_text) 
df3['general'] = df3['raw_desc'].apply(clean_text)  
df4['general'] = df4['raw_desc'].apply(clean_text)  




# All dataset 
# Job Description + General 3 
text1 = ' '.join(df1.job_description)
text2 = ' '.join(df3.general)
finaldf = merge_word_count(text1, text2)

with pd.ExcelWriter('desc_text.xlsx',mode="w") as writer:
    finaldf.to_excel(writer,sheet_name='description')

# Job Requirement + General 4 
text3 = ' '.join(df2.job_requirement)
text4 = ' '.join(df4.general)
finaldf2 = merge_word_count(text3, text4)

with pd.ExcelWriter('desc_text.xlsx',mode="a") as writer:
    finaldf2.to_excel(writer,sheet_name='requirement')


# Group by attribute
def aggregate(df1,df2,df3,df4,attribute,level,filepath1,filepath2,subset=False):  
    if subset:
        df1,df2,df3,df4 = subset() 
    for i in level:
        text1 = ' '.join(df1[df1[attribute] == i].job_description)
        text2 = ' '.join(df3[df3[attribute] == i].general) 
        text3 = ' '.join(df2[df2[attribute] == i].job_requirement)
        text4 = ' '.join(df4[df4[attribute] == i].general)
        finaldf = merge_word_count(text1, text2)
        finaldf2 = merge_word_count(text3, text4)
        if i == level[0]: 
            with pd.ExcelWriter(filepath1,mode="w") as writer:
                finaldf.to_excel(writer,sheet_name=i)
            with pd.ExcelWriter(filepath2,mode="w") as writer:
                finaldf2.to_excel(writer,sheet_name=i)
        else: 
            with pd.ExcelWriter(filepath1,mode="a") as writer:
                finaldf.to_excel(writer,sheet_name=i)
            with pd.ExcelWriter(filepath2,mode="a") as writer:
                finaldf2.to_excel(writer,sheet_name=i)

titlelevel = ['Data Scientist','Data Analyst','Data Engineer','Machine Learning Engineer']
aggregate(df1,df2,df3,df4,attribute='title_v3',level=titlelevel,filepath1='t_desc.xlsx',filepath2='t_reqr.xlsx')

level = data.exp_level_v3.unique()
aggregate(df1,df2,df3,df4,attribute='exp_level_v3',level=level,filepath1='e_desc.xlsx',filepath2='e_reqr.xlsx',subset=True)

