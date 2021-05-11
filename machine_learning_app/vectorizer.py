"""
This file gets the concatenated CSV and creates numpy files about it.
"""

import collections
import pandas as pd
import numpy as np
import re
import os

from keras import utils
from keras.preprocessing import sequence

class Vectorizer:
    
    def __init__(self, filename, max_vocab, max_length):
        print("Processing: {}".format(filename))

        self.MAX_VOCABULARY = max_vocab
        self.MAX_LENGTH = max_length
        self.filename = filename

        self.word_freqs = collections.Counter()
        self.word2index = {}
        self.index2word = {}

        self.dataset = pd.read_csv(filename, sep='^', header=None)

        num_recs = self.dataset.shape[0]

        self.X = np.empty((num_recs, ), dtype=list)
        self.y = np.zeros((num_recs, ))

    def collectVocab(self):
        """This method counts the occurrence of words"""

        for i in range(self.dataset.shape[0]):

            samples = self.dataset.iloc[i,0].split()

            for word in samples:
                self.word_freqs[word] +=1

        print("Vocabulary has been created.")      
        
    def createLookupTables(self):
        """This method creates lookup tables for words and POS tags"""
        
        # The size of vocabulary + QPOS + QUNKN
        vocab_size = min(self.MAX_VOCABULARY, len(self.word_freqs)+2)

        print("For file :{}".format(self.filename))
        print("Vocab size: {}".format(vocab_size))

        self.word2index = {x[0]: i+2 for i, x in enumerate(self.word_freqs.most_common(vocab_size))}
        self.word2index['QPAD'] = 0
        self.word2index['QUNKN'] = 1

        self.index2word = {v : k for k,v in self.word2index.items() }

        print("Lookup tables have been created.")

    def createVectors(self):
        """This method creates vectors using the occurrence of words and labels"""
        maxlen = 0
        
        for i in range(self.dataset.shape[0]):
    
            labels = self.dataset.iloc[i,-1]

            samples = self.dataset.iloc[i,0].split()

            seqs = []
    
            for word in samples:
        
                if word in self.word2index:
                    w = self.word2index[word] 
                else:
                    w = self.word2index['QUNKN']
        
                seqs.append(w)    

            if len(seqs) > maxlen:    
                maxlen = len(seqs)

            seql = min(len(seqs), self.MAX_LENGTH)

            seqs = seqs[0:seql]
    
            self.X[i] = seqs  
            self.y[i] = labels

        self.X = sequence.pad_sequences(self.X, maxlen=self.MAX_LENGTH)
        
        print("Vectorizing has been accomplished.")
    
    def saveVectorAs(self, name):
        """This method saves the vector into numply files"""
        np.save(name+"X.npy", self.X)
        np.save(name+"y.npy", self.y)
        
        print("File {} and {} have been saved.".format(name+"X.npy", name+"y.npy"))


if __name__ == '__main__':
    dataset = pd.read_csv('tanulo_adatok/AST/concatenated_titled.csv', sep='^', header=None)
    search_maxlength = []
    for i in range(dataset.shape[0]):
            samples = dataset.iloc[i,0].split()
            search_maxlength.append(len(samples))
    search_maxlength.sort()
    
    myvectorizer = Vectorizer('tanulo_adatok/AST/concatenated_titled.csv', 2000, search_maxlength[90])
    myvectorizer.collectVocab()
    myvectorizer.createLookupTables()
    myvectorizer.createVectors()
    myvectorizer.saveVectorAs('test')
    
    myvectorizer = Vectorizer('tanulo_adatok/AST/toimport_vulnerabilities_ast.csv', 2000, search_maxlength[90])
    myvectorizer.collectVocab()
    myvectorizer.createLookupTables()
    myvectorizer.createVectors()
    myvectorizer.saveVectorAs('toimport')