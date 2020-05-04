#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:20:06 2020

@author: vyvo
"""

from dependency import *
from cleantext import *

# Data Cleaning  
train = pd.read_csv('train_data.csv',converters={'label':pd.to_numeric})



# Feature Extraction: Doc2Vec / Word2Vec Model 
class callback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        print('Loss after epoch {}: {}'.format(self.epoch, loss))
        self.epoch += 1


def t2v(feature_size, window_context, epoch, min_word_count=10, sample=1e-3, gram=5,w2v=True):

    global train  
    train.text = train.text.apply(quick_clean_text) # clean 
    # tokenize entire data 
    train_corpus = [tokenizer.tokenize(document) for document in train.text]
    
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

# visualize embeddings 
def plot2D(model,topn=50,restrict_x=0,restrict_y=0): #restrict the domain display closely related words only, e.g., X, Y between -2000 and 2000
    df = pd.DataFrame(model.wv.index2word,columns=['words'])
    df['freq'] = df['words'].map(lambda x: model.wv.vocab[x].count)
    df = df.sort_values(by=['freq'],ascending=False).head(topn)
   
    
    # only visualize topn most frequently occuring keywords
    wvs = model.wv[df['words']]
    
    tsne = TSNE(n_components=2, random_state=0, n_iter=5000, perplexity=2)
    np.set_printoptions(suppress=True)
    T = tsne.fit_transform(wvs)
    df['x'],df['y'] = T[:,0],T[:,1]
    df = df.where((df.x >= -restrict_x) & (df.x <= restrict_x) & (df.y >= -restrict_y) & (df.y <= restrict_y))
    
    plt.figure(figsize=(12, 6))
    plt.scatter(df.x, df.y, c='orange', edgecolors='r')
    for label, x, y in zip(df.words, df.x, df.y):
        plt.annotate(label, xy=(x+1, y+1), xytext=(0, 0), textcoords='offset points')
    plt.show()



#model.wv.most_similar(['programming'],topn=20)


