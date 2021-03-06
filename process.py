# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:28:49 2016

@author: Rok
"""

import collections
import re
import numpy as np
import os
from sklearn.preprocessing import Normalizer

#This module is made to work with preprocesed datasets by Ana Cardoso-Cachopo used in her thesis 
#"Improving Methods for Single-label Text Categorization". 
#http://web.ist.utl.pt/~acardoso/datasets/

#iterates trough all lines (representing documents in a file) and get the vocabulary
def get_words(filepath, n=False):
    cnt = collections.Counter() #instantiate a counter
    #Count the words in the entire corpus - all the documents
    file = open(filepath, encoding="Latin-1")
    for row in file: #Count the words in a (text) file                  
        for word in row.partition('\t')[2].split(' '): #skip the first word (it represents labels)
            cnt[word] += 1
    file.close()
    words = [] #Get the n words that appear most frequently in a text (corpus) as a list of strings
    if n: d2 = cnt.most_common(n)
    d2 = cnt.most_common() #take all words
    for key, value in d2: words.append(key)
#    if n: np.savetxt(str(n) + "_words.txt", words, fmt="%s")
#    np.save("words", words)
    return words

#Iterate over lines(texts) in the file and present each text with a n-dimensional vector according to provided list words
#If the k-th vector has a value i on j-th place it means the word words[j] appears i times in this k-th text
#Also exports the ground trouth labels 
def get_M(filepath, words):
    n = len(words)
    M = []
    label_names = []
    labels = []
    file = open(filepath, encoding="Latin-1")
    for row in file: #Count the words in a line
        vector = np.zeros(n) #a vector representation of the text file  
        label = row.partition('\t')[0] #first word of a line is a label
        if label in label_names: labels.append(label_names.index(label))
        else:
            label_names.append(label)
            labels.append(label_names.index(label))                         
        for word in row.partition('\t')[2].split(' '):
            if word in words: #if word appears in words list 
                vector[words.index(word)] += 1 #add 1 to appropriate dimension
        M.append(vector) #add the vector to the M matrix
    file.close()
    M = np.array(M)
    labels = np.array(labels)
#    np.save("M", M)
#    np.save("labels", labels)
    return (M, labels)

#takes an M matrix generated by get_M and returns a tf_idf matrix
def get_tf_idf_M(M, tf = ["bin", "raw", "log", "dnorm"], idf = ["c", "smooth", "max", "prob"], norm_samps=False):
    N = len(M)
    if tf == "raw":
        tf_M = np.copy(M) #just the frequency of the word in a text
#    #TODO: check if dnorm is implemented OK
#    elif tf == "dnorm":
#        tf_M = 0.5 + 0.5*(M/(np.amax(M, axis=1).reshape((N,1))))
    if idf == "c":
        idf_v = []
        for i in range(M.shape[1]): #get the number of texts that contain a word words[i]
            idf_v.append(np.count_nonzero(M[:,i])) #count the non zero values in columns of matrix M
        idf_v = np.array(idf_v)
        idf_v = np.log(N/idf_v)
    tf_idf_M = tf_M*idf_v
    if norm_samps:
        normalizer = Normalizer()
        tf_idf_M = normalizer.fit_transform(tf_idf_M)
#    np.save("tf_idf_M", tf_idf_M)
    return tf_idf_M