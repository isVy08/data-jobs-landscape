#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 21:22:32 2020

@author: vyvo
"""
from dependency import *
from word2vec import * 

# Hyperparameters 
w2v = True
feature_size = 10
window_context = 5
gram = 5
n_neighbors = 5

# Get model & data for training 

result = t2v(w2v=w2v)
model = result[0]
data = result[1]

model.wv.most_similar(['analyze'])


def vectorize(token):  
    global model
    result = []
    for word in token:
        try: 
            result.append(model.wv[word])
        except: 
            pass 
    result = np.average(np.array(result),axis=0)
    return result

def prepare(data,w2v):
    new_train = data.copy()
    
    if w2v: 
        new_train['vec'] = new_train['corpus'].apply(vectorize)
    else: 
        new_train['vec'] = new_train['corpus'].apply(model.infer_vector)
        
    new_train.dropna(inplace=True)
    return new_train 

# Split train test data 
new_train = prepare(data,w2v=w2v)
X_train, X_test, y_train, y_test = train_test_split(new_train['vec'], new_train['label'], test_size=0.3, random_state=18,stratify=new_train['label'])
X_train, X_test = np.vstack(np.array(X_train)), np.vstack(np.array(X_test))



# build model 

def knn(n_neighbors):
    global X_train, X_test, y_train, y_test   
    neigh = KNeighborsClassifier(n_neighbors=n_neighbors)
    neigh.fit(X_train,y_train)
    y_pred = y_pred = neigh.predict(X_test)
    return accuracy_score(y_test, y_pred) 

knn(7)

