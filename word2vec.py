#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:20:06 2020

@author: vyvo
"""

from dependency import *
from cleantext import *

# Data Cleaning  
global train
train = pd.read_csv('train.csv',converters={'label':pd.to_numeric})

def clean_text(text): 
    text = remove_special_characters(text,True)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    return text 

train.text = train.text.apply(clean_text) # clean 
# tokenize entire data 
train_corpus = [tokenizer.tokenize(document) for document in train.text]

# Feature Extraction: Doc2Vec / Word2Vec Model 
class callback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        print('Loss after epoch {}: {}'.format(self.epoch, loss))
        self.epoch += 1


def t2v(feature_size=10, window_context=5, min_word_count=5, epoch=30, sample=1e-3, gram=5,w2v=True):

    global train_corpus, train  
    
    # transform dataset by gram 
    train['corpus'] = train['text'].map(lambda text: list(ngrams(text.split(' '),gram)))
    new_train = train.explode('corpus').reset_index(drop=True).dropna()
    
    if w2v: # build word2vec model 
        model = word2vec.Word2Vec(train_corpus, size=feature_size, 
                          window=window_context, min_count=min_word_count,
                          sample=sample, iter=epoch,callbacks=[callback()])
    
    else: #build doc2vec model 
        docgram = list(new_train['corpus'])
        model = doc2vec.Doc2Vec(vector_size=feature_size, min_count=min_word_count, epochs=epoch)
        vocab = list(doc2vec.TaggedDocument(y,[x]) for x, y in enumerate(docgram)) 
        model.build_vocab(vocab) # Build vocabulary 
        model.train(vocab, total_examples=model.corpus_count, epochs=model.epochs)
    return model, new_train[['corpus','label']] 






