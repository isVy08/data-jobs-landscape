#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vyvo

Detect whether a corpus is about Job description or Job requirement

"""

from dependency import * 
from cleantext import *



# Label text by headings

def group_text(html_text): #must be html text 
    """
    If text contains bullet points with bold sub-titles, group them by these titles. 
    Otherwise, return chunked text
    """
    parse = BeautifulSoup(html_text,'lxml') #parse html text
    extr = parse.find_all(['strong','p','li'])
    split_index = [] #get locations of tags of bold titles <strong>
    for i, val in enumerate(extr):
         if '<strong>' in str(val):
             split_index.append(i)
    if len(split_index) < 2: 
        return extr #if the description not structured by bold titles, get the whole text 
            
    else: 
        result = [extr[k : j] for k, j in zip([0] + split_index, split_index + [None])] #split & group elements under same bold titles 
        result = list(filter(lambda x: len(x) > 1,result)) #remove items with zero or one values 
        return result  

def labeling(title):
    path = os.getcwd()
    
    # Load keywords 
    js_kw = pd.read_csv(path+'/data processing/job_responsibility.csv')
    jq_kw = pd.read_csv(path+'/data processing/job_requirement.csv')
    js_kw, jq_kw = js_kw.keyword, jq_kw.keyword
    
    title = remove_special_characters(title).lower()
    title = tokenizer.tokenize(title)
    
    #get labels
    i = 0
    j = 0
    result = False
    while result == False and j < len(js_kw): 
        if i >= len(jq_kw):
            result = all(s in title for s in js_kw[j].split(' '))
            j +=1 
        else: 
            result = all(s in title for s in jq_kw[i].split(' '))
            i+=1 
    if i < len(jq_kw): 
        return 1 # requirement
    elif i >= len(jq_kw) and j < len(js_kw): 
        return 0 # responsiblity
    else: 
        return 2 # others
    

def to_text(corpus): 
    if isinstance(corpus,list):
        corpus  = list(map(lambda t: t.get_text().lower(),corpus))
        return ' '.join(corpus)
    else: 
        return corpus.get_text().lower()
        
def prepare(): # create train and predict data 
    data = pd.read_csv('clean_data.csv')
    data['clean_description'] = data['description_v2'].apply(group_text)
    df = data[['clean_description','description_v2']].explode('clean_description')
    
    df.dropna(inplace=True)
    df.reset_index(inplace=True) 
    df['label'] = df['clean_description'].map(lambda x: labeling(x[0].get_text()) if isinstance(x,list) else 3)
    df['text'] = df['clean_description'].apply(to_text)
    df = df.loc[df.text!= '',:] # remove null text   
    df = df.reset_index(drop=True)
    df = df.rename(columns={'index':'id'})
    
    train = df.loc[df.label<3,['id','text','label']]
    df.to_csv('label_data.csv',index=False)
    train.to_csv('train_data.csv',index=False)


data['new_text']  = data.groupby(['id','label'])['text'].transform(lambda x: ' '.join(x))
a = data.drop_duplicates('new_text')

# Naive Bayes Classifier 


def vectorize(input_data):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(input_data)
    X = X.toarray()
    return X

data = pd.read_csv('label_data.csv')
data.dropna(inplace=True)
data.reset_index(drop=True,inplace=True)
data['text'] = data['text'].map(lambda x: quick_clean_text(x,remove_digits=False))
X = vectorize(data.text)    

train = data[data.label<3]
train_input = X[train.index]

predict = data[data.label==3]
predict_input = X[predict.index]

    

def nb():
    X_train, X_test, y_train, y_test = train_test_split(train_input, train.label, test_size=0.3, random_state=18,stratify=train.label)
    clf = MultinomialNB().fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)
    return clf, accuracy_score(y_test, y_pred)

model, accuracy = nb()

