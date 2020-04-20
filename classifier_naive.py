#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vyvo

Classify if a block of text is about Job description or Job requirement by heading 

"""

from dependency import * 

# Load keywords 
js_kw = pd.read_csv('job_responsibility.csv')
jq_kw = pd.read_csv('job_requirement.csv')
js_kw, jq_kw = js_kw.keyword, jq_kw.keyword 

def labeling(title,js_kw,jq_kw):
    title = re.split('(\W+)',title.lower()) #title must be a string, split it into list of words 
    #get labels
    i = 0
    j = 0
    result = False
    while result == False and j < len(js_kw): 
        if i >= len(js_kw):
            result = all(s in title for s in js_kw[j].split(' '))
            j +=1 
        else: 
            result = all(s in title for s in jq_kw[i].split(' '))
            i+=1 
    if i < len(jq_kw): 
        return 'Requirement'
    elif i >= len(jq_kw) and j < len(js_kw): 
        return 'Responsibility'
    else: 
        return 'Unclassified'