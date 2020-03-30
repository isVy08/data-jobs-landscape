#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Task: Generate 2 new features 'jod_description' and 'job_requirement' from feature 'description' (in html format) 
import pandas as pd 
from bs4 import BeautifulSoup
import re

#import raw data 
data = pd.read_csv('dsjob_final.csv')

#quick look at data 
data.info()


#1. Text Grouping: If text contains bullet points with bold sub-titles, group them by these titles. Otherwise, return the whole text 
def group_text(html_text): #must be html text 
    parse = BeautifulSoup(html_text,'lxml') #parse html text
    extr = parse.find_all(['strong','p','li'])
    split_index = [] #get locations of tags of bold titles <strong>
    for i, val in enumerate(extr):
         if '<strong>' in str(val):
             split_index.append(i)
    if len(split_index) == 0: 
        return (parse.get_text().lower()) #if the description not structured by bold titles, get the whole text 
            
    else: 
        result = [extr[k : j] for k, j in zip([0] + split_index, split_index + [None])] #split & group elements under same bold titles 
        result = list(filter(lambda x: len(x) > 1,result)) #remove items with zero or one values 
        return result  

data['clean_description'] = data['description'].apply(group_text)

#2. Text Extraction: Extract grouped content only  
data['main_description'] = data['clean_description'].map(lambda x: list(filter(lambda y: '<strong>' in str(y[0]),x))) #ungrouped content return empty list []

#3. Text Labeling: Classify content as 1: Job responsibility, 2: Requirements, 3: Others based on title keywords    

def labeling(title,jd_kw,jr_kw):
    title = re.split('(\W+)',title.lower()) #title must be a string, split it into list of words 
    #get labels
    i = 0
    j = 0
    result = False
    while result == False and j < len(jd_kw): 
        if i >= len(jr_kw):
            result = all(s in title for s in jd_kw[j].split(' '))
            j +=1 
        else: 
            result = all(s in title for s in jr_kw[i].split(' '))
            i+=1 
    if i < len(jr_kw): 
        return 2
    elif i >= len(jr_kw) and j < len(jd_kw): 
        return 1
    else: 
        return 3

#Load keywords manually updated 
jd_kw = pd.read_csv('job_description.csv')
jr_kw = pd.read_csv('job_requirement.csv')
jd_kw, jr_kw = jd_kw.keyword, jr_kw.keyword 

#Generate new feature 'label'
data['label'] = data['main_description'].map(lambda x: [labeling(title=p[0].get_text(),jd_kw=jd_kw,jr_kw=jr_kw) for p in x] if len(x)>0 else 0)

#Categorize Text Group
def categorize(paraList,labelList,catId): #catID -> 1: Job responsibility, 2: Requirements, 3: Others
    indexList = [i for i,val in enumerate(labelList) if val==catId]
    if len(indexList)==0:
        return 0
    else: 
        result = []
        for k in indexList: 
            result.extend(paraList[k])
        result = list(map(lambda x: x.get_text(),result))
        return '.'.join(result).lower()

#Create new features
    
jdesc = [] 
jreq = []
for row in range(data.shape[0]):
    if isinstance(data['label'][row],list):
        g1 = categorize(data['main_description'][row],data['label'][row],catId=1)
        jdesc.append(g1)
        g2 = categorize(data['main_description'][row],data['label'][row],catId=2)
        jreq.append(g2)
    else: 
        jdesc.append(0)
        jreq.append(0)
        
data['job_description'] = jdesc 
data['job_requirement'] = jreq

data.to_csv('datafull.csv',index=False)


