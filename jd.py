#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Create new features 'jod_desc' and 'job_req' from feature 'description' 
import pandas as pd 
from bs4 import BeautifulSoup
import re

data = pd.read_csv('dsjob_final.csv')

data.head()
data.info()


#If text contains bullet points with bold sub-titles, group them by these titles. Otherwise, return the whole text 
content = []
for desc in data.description: 
    parse = BeautifulSoup(desc,'lxml')
    extr = parse.find_all(['strong','p','li'])
    split_index = []
    for i, val in enumerate(extr):
         if '<strong>' in str(val):
             split_index.append(i)
    if len(split_index) == 0: 
        content.append(parse.get_text().lower())
            
    else: 
        result = [extr[k : j] for k, j in zip([0] + split_index, split_index + [None])] 
        result = list(filter(lambda x: len(x) > 1,result)) #remove items with zero or one value 
        content.append(result) 

#Insert as new feature 
data['description_v2'] = content 

#Create new feature with only elements as grouped para 
data['description_v3'] = data['description_v2'].map(lambda x: list(filter(lambda y: '<strong>' in str(y[0]),x))) 

#Filter para about job description 
jd_kw = pd.read_csv('job_description.csv')
jr_kw = pd.read_csv('job_requirement.csv')
jd_kw, jr_kw = jd_kw.keyword, jr_kw.keyword 

        

def labeling(data,jd_kw,jr_kw,html_content=False): 
    #1: Job responsibility, 2: Requirements, 3: Others 
    # data is job description in html with each element is a list / paragraph 
    d = {} 
    for inst in data: 
        #get content in raw text 
        if html_content: #want to convert html to text 
            txt = inst[0].get_text().lower()
        else: 
            txt = inst[0].lower() 
        txt = re.split('(\W+)',txt) #split txt into lists 
        #get labels
        i = 0
        j = 0
        result = False
        while result == False and j < len(jd_kw): 
            if i >= len(jr_kw):
                result = all(s in txt for s in jd_kw[j].split(' '))
                j +=1 
            else: 
                result = all(s in txt for s in jr_kw[i].split(' '))
                i+=1 
        idx = data.index(inst)
        if i < len(jr_kw): 
            d[idx] = 2
        elif i >= len(jr_kw) and j < len(jd_kw): 
            d[idx] = 1
        else: 
            d[idx] = 3
    return d

inst = test[0]

test = data['description_v3'][10]
labeling(test,jd_kw,jr_kw,html_content=True)

data['classify'] = data['description_v3'].map(lambda x: labeling(x,jd_kw,jr_kw,html_content=True) if len(x)>0 else 0)

def categorize(paraList,indexDict,catId): #catID -> 1: Job responsibility, 2: Requirements, 3: Others
    indexList = [i for i,val in indexDict.items() if val==catId]
    if len(indexList)==0:
        return 0
    else: 
        result = []
        for k in indexList: 
            result.extend(paraList[k])
        result = list(map(lambda x: x.get_text(),result))
        return '.'.join(result).lower()
       
paraList = test 
indexDict = data['classify'][10]

categorize(paraList,indexDict,catId=2)

jdesc = [] 
jreq = []
for a in range(data.shape[0]):
    if isinstance(data['classify'][a],dict):
        g1 = categorize(data['description_v3'][a],data['classify'][a],catId=1)
        jdesc.append(g1)
        g2 = categorize(data['description_v3'][a],data['classify'][a],catId=2)
        jreq.append(g2)
    else: 
        jdesc.append(0)
        jreq.append(0)
        
data['job_description'] = jdesc 
data['job_requirement'] = jreq

data.loc[(data['job_description']!=0)&(data['job_requirement']!=0)].shape

data.to_csv('test.csv',index=False)


