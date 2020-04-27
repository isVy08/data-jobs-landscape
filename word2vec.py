#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:20:06 2020

@author: vyvo
"""

from dependency import *
from cleantext import *
from gensim.models import word2vec 
from nltk.util import ngrams

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report




# 1. Data Cleaning  
train = pd.read_csv('train.csv',converters={'label':pd.to_numeric})

def clean_text(text): 
    text = remove_special_characters(text,True)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    return text 

train.text = train.text.apply(clean_text)


# 2. Feature Extraction: Word2Vec Model 
tokenized_corpus = [tokenizer.tokenize(document) for document in train.text]

# Set values for various parameters
feature_size = 10    # Word vector dimensionality  
window_context = 5  # Context window size                                                                                    
min_word_count = 5   # Minimum word count                        
sample = 1e-3   # Downsample setting for frequent words

w2v_model = word2vec.Word2Vec(tokenized_corpus, size=feature_size, 
                          window=window_context, min_count=min_word_count,
                          sample=sample, iter=50)

# return training loss 
training_loss = w2v_model.get_latest_training_loss()
print(training_loss)

w2v_model.wv['data'] # return vectors 
w2v_model.wv.most_similar(['analyze']) # return most similar words 

# 3. Classifier: KNN 

# prepare data 

def vectorize(token): 
    result = []
    for word in token:
        try: 
            result.append(w2v_model.wv[word])
        except: 
            pass 
    result = np.average(np.array(result),axis=0)
    return result 

def transform(data,gram=20):
    data['corpus'] = data['text'].map(lambda text: list(ngrams(text.split(' '),gram)))
    data = data.explode('corpus').reset_index(drop=True).dropna()
    data['vec'] = data['corpus'].apply(vectorize)
    return data[['vec','label']] 

new_train = transform(train)

# split train test data 
X_train, X_test, y_train, y_test = train_test_split(new_train['vec'], new_train['label'], test_size=0.3, random_state=18,stratify=new_train['label'])
X_train, X_test = np.array(list(X_train)),np.array(list(X_test))

# build model 

def knn(n_neighbors):
    global X_train, X_test, y_train, y_test   
    neigh = KNeighborsClassifier(n_neighbors=n_neighbors)
    neigh.fit(X_train,y_train)
    y_pred = y_pred = neigh.predict(X_test)
    target_names = ['jd','jr']
    return classification_report(y_test, y_pred, target_names=target_names) #change this 

knn(15)

