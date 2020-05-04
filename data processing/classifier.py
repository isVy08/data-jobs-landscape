#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vyvo

Detect whether a corpus is about Job description or Job requirement

"""

from dependency import * 
from cleantext import *

# Label text by headings

def labeling(title):
    
    # Load keywords 
    js_kw = pd.read_csv('job_responsibility.csv')
    jq_kw = pd.read_csv('job_requirement.csv')
    js_kw, jq_kw = js_kw.keyword, jq_kw.keyword 

    title = re.split('(\W+)',title.lower()) #tokenize
    
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

# Naive Bayes Classifier 

# prepare train and predict data 

    df = pd.read_csv('clean_data.csv')
    data = df.loc[(df.job_responsibility=='0')|(df.job_requirement=='0'),
                  ['description_v2','job_responsibility','job_requirement']]
    
    
    .apply(remove_html)
    text = text.apply(quick_clean_text)
    
    result = []
    for t in text:
        token = t.split(' ')
        result.append(' '.join(token[:round(len(token)/2)]))
        result.append(' '.join(token[round(len(token)/2):]))
    pd.Series(result).to_csv('predict_data.csv')
df.loc[(df.job_description=='0')&(df.job_requirement!='0'),'description_v2'].shape


def vectorize(input_data):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(input_data)
    X = X.toarray()
    return X
    

def nb():
    train = pd.read_csv('train_data.csv') 
    X = vectorize(train.text)
    X_train, X_test, y_train, y_test = train_test_split(X, train.label, test_size=0.3, random_state=20,stratify=train.label)
    clf = MultinomialNB().fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    return clf, accuracy_score(y_test, y_pred)

model, accuracy = nb()


    
input_data = prep()    
X_pred = vectorize(input_data)
label = model.predict(X_pred)
