#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 21:22:32 2020

@author: vyvo
"""
from dependency import *
from word2vec import * 

# Hyperparameters
w2v=False
feature_size = 10
window_context = 5
gram = 2


# Get model & data for training 

result = t2v(feature_size=feature_size, window_context=window_context, epoch=31,w2v=w2v,gram=gram)
model, data = result
plot2D(model,100,2000,2000)

test = t2v(feature_size=feature_size, window_context=window_context, epoch=3,w2v=w2v,gram=gram)
model, data = result

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
    
    if w2v: 
        data['vec'] = data['corpus'].apply(vectorize)
    else: 
        data['vec'] = data['corpus'].apply(model.infer_vector)
        
    data.dropna(inplace=True)

# Split train test data 
prepare(data,w2v=w2v)
X_train, X_test, y_train, y_test = train_test_split(data['vec'], data['label'], test_size=0.3, random_state=18,stratify=data['label'])
X_train, X_test = np.vstack(np.array(X_train)), np.vstack(np.array(X_test))




# build model 

# KNN

def knn(n_neighbors):
    global X_train, X_test, y_train, y_test   
    neigh = KNeighborsClassifier(n_neighbors=n_neighbors,weights='distance',algorithm='kd_tree')
    neigh.fit(X_train,y_train)
    y_pred = neigh.predict(X_test)
    return accuracy_score(y_test, y_pred) 

knn(15)

# Naive Bayes






