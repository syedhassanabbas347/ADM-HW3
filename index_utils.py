#!/usr/bin/env python
# coding: utf-8

# In[4]:


import urllib.request
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import json
import collections
import math


# In[2]:


import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
def preprocess(k):
    
    
    k = k.lower() # make all the word turn into lower case
    tokenizer = RegexpTokenizer(r'\w+')
    result = tokenizer.tokenize(k)
    stop_words = set(stopwords.words('english'))
    text = result
    new_sentence =[]
    for w in text:
        if w not in stop_words: 
            new_sentence.append(w) #drop the stopwords of our string
    ps = PorterStemmer()
    final = []
    for word in new_sentence:
        final.append(ps.stem(word)) #get the root form of each word
    return(final)


# In[6]:


# here we create the index 
def index_1():

    listemot = [] #will contain the words 
    listedoc = [] # will be a list of lists. Each list in this list is link to a unique word, and will contain the document in which the word appears

    for k in range(0,29982):
        if k%100 == 0 : 
            print(k) # indicator to see at which step we are during the computing
        try : 
            nbr = str(k)
            with open(r'C:\Users\danyl\OneDrive\Documents\tsv\document_'+nbr+'.tsv', encoding = 'utf8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                for row in reader:
                    if len(row)>0:
                        a = row[1] # we get the intro
                        b = row[2] #we get the plot
            b = preprocess(b) # we drop the stopwords, ponctuation, and turn words into root form
            a = preprocess(a)
            for element in b: #we iterering over the words in the plot
                if element in listemot: #we check if the word is already in the list
                    i = listemot.index(element) #if it is, we get its index 
                    if nbr not in listedoc[i]: #we check if we don't already refer that the word is in this document
                        listedoc[i].append(nbr) #we save the tsv number in a list which is link to this specific word.
                else : 
                    listemot.append(element) #we add the word in the list if it is not already in
                    ldoc = [nbr] #we store the number of the tsv file
                    listedoc.append(ldoc) # we store the new list in the list of document
            for element in a: #we do the same thing we the intro, with the same logic
                if element in listemot:
                    i = listemot.index(element)
                    if nbr not in listedoc[i]:
                        listedoc[i].append(nbr)
                else : 
                    listemot.append(element)
                    ldoc = [nbr]
                    listedoc.append(ldoc)
        except:
            pass
    
    a = {}
    # we create a dictionnary. the keys of the dictionnary is the index of each word, and the value is a list of document in which the word appears
    for k in range(0,len(listemot)):
        a[k] = listedoc[k]
    
    return(a,listemot, listedoc)
            
            

        


# In[7]:


# this code is similar to the code we have done to build the first index. We just have two difference
def index_2():
    listemot2 = []
    listedoc2 = []
    dic_words_doc = {} # will contain, for each document, the number of words it contain

    for k in range(0,29982):
        if k%100 == 0:
            print(k)
        try : 
            nbr = str(k)
            with open(r'C:\Users\danyl\OneDrive\Documents\tsv\document_'+nbr+'.tsv', encoding = 'utf8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                for row in reader:
                    if len(row)>0:
                        a = row[1]
                        b = row[2]
            b = preprocess(b)
            a = preprocess(a)
            for element in b: 
                if element in listemot2:
                    i = listemot2.index(element)
                    listedoc2[i].append(nbr) #the difference is that even if we have already stored the document that contain the word, we are going to store it again if we have the same word several time in the same document. So we have informations on the occurence of each word in each document
                else : 
                    listemot2.append(element)
                    ldoc = [nbr]
                    listedoc2.append(ldoc)
            for element in a: 
                if element in listemot2:
                    i = listemot2.index(element)
                    listedoc2[i].append(nbr)
                else : 
                    listemot2.append(element)
                    ldoc = [nbr]
                    listedoc2.append(ldoc)
            dic_words_doc[k] = len(a) + len(b) # here we store the number of words in the intro+plot
        
        except : 
            pass
    listeinverted = []

    # here we want to create a dictionnary in which the key will be the index of the word, and the value will be a dictionnary (key = document, value = tf-idf)

    for k in range(len(listedoc2)): #listedoc2 contain lists of documents link a unique word
        i = collections.Counter(listedoc2[k]) # We now have a dictionnary (key = document, value = occurence of the word in this document)
        dic = {} 
        for key, value in i.items(): # we go into the dictionnary i we created
            number = dic_words_doc[int(key)] # we get the number of words of the document which is the key of the dictionnary
            dic[key] = (value/number)*(1+math.log(float(29981/(len(i))))) # we calculate the tf-idf of each document
        listeinverted.append(dic) #we store the dic that refers to a word and that containt (key = document, value = tf_idf) in a list
    

    # here we create the dictionnary (key = index_word, value = dictionnary(key = document, value = tf-idf))
    dicInverted = {}

    for k in range(0,len(listemot2)):
        dicInverted[k] = listeinverted[k]
    return(dicInverted, listemot2, listedoc2, dic_words_doc)
    
    
            
            

        


# In[ ]:




