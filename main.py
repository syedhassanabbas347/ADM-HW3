#!/usr/bin/env python
# coding: utf-8

# In[32]:


import urllib.request
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import json
import collections
import math
# we write routines functions that will clean our data


# In[44]:


# we load the dictionnary we just created
with open('dic1.json') as json_file:
    data = json.load(json_file)
with open('dicvoc.json') as json_file:
    listemot = json.load(json_file)
with open('dic2.json') as json_file:
    dicInverted = json.load(json_file)
with open('listedoc2.json') as json_file:
    listedoc2 = json.load(json_file)
with open('dicvoc.json') as json_file:
    listemot2 = json.load(json_file)
with open('number_words_doc.json') as json_file:
    dic_words_doc = json.load(json_file)
import import_ipynb

from index_utils import preprocess
from collector_utils1 import file_to_parse
df = file_to_parse(3)


# In[45]:



def search_engine1(query):
    query = preprocess((query)) #we preprocess it
    listedocuments = [] 
    tfidf_query = collections.Counter(query) #turn our query into a dictionnary (key = word, value = occurence)
    for key in tfidf_query.keys():
        if key not in listemot2:
            print("Word(s) in your query does not exist")
            return
    

    for element in query: # we preprocess the query, and we iterring into the words
            if element in listemot: #we check if the word is in the list of words 
                i = listemot.index(element) # we get the index of the word
                listedocuments.append(data[str(i)]) # we go into the dictionnary to get the documents that contain the word

    #we do the intersection of all the list to get the document that contain all the word of the query       
    result = list(set(listedocuments[0]).intersection(*listedocuments[:len(listedocuments)]))
    if len(result) == 0:
        print('No document contains all your words')
        return
    
    listetitle = []
    listeintro = []
    listeurl = []
    for element in result: #element is a number of tsv document
        with open(r'C:\Users\danyl\OneDrive\Documents\tsv\document_'+element+'.tsv', encoding = 'utf8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                for row in reader:
                    if len(row)>0:
                        a = row[0] #we get the title
                        b = row[1] #get the intro
                listetitle.append(a)
                listeintro.append(b)
                listeurl.append(df.iloc[int(element)][0]) #we get the url using the dataframe of the beginning
            
    dfresult = pd.DataFrame(list(zip(listetitle, listeintro,listeurl)), 
                   columns =['Title', 'Intro', 'URL']) #we group the result in a dataframe
    return(dfresult)




def search_engine_2(query):
    query = preprocess((query)) #we preprocess it
    listedocuments = [] 
    tfidf_query = collections.Counter(query) #turn our query into a dictionnary (key = word, value = occurence)
    for key in tfidf_query.keys():
        if key not in listemot2:
            print("Word(s) in your query does not exist")
            return
        
    for key,values in tfidf_query.items():
        tf = values/len(query) #for each word in the query we calculate the tf-idf
        tfidf_query[key] = tf*(1+math.log(float(29981/len(dicInverted[str(listemot2.index(key))]))))

    # as we have done in the first part, we get the documents that contains all we words of the query
    listedocuments = []
    for element in query:
            if element in listemot2:
                i = listemot2.index(element)
                listedocuments.append(dicInverted[str(i)].keys())
    
    results = list(set(listedocuments[0]).intersection(*listedocuments[:len(listedocuments)]))
    if len(results) == 0:
        print('No document contains all your words')
        return
     
        
 

    
    #we create a dictionnary (key = document, value = dictionnary (key = words in query, value = tf-idf))
    dic_final = {}
    for result in results :
        dic_result = {}
        for element in query:
            i = listemot2.index(element)
            dic_result[element] = dicInverted[str(i)][str(result)]
        dic_final[result] = dic_result
    # we compute the cosine similary which is just a formula, using the tf-idf of each word with respect to the documents, and the tf-idf of the query
    dic_cosine = {}
    for keys, values in dic_final.items():
        dot_prod = 0
        norm_query = 0
        norm_doc = 0
        for key in tfidf_query.keys():
            dot_prod = dot_prod + values[key] * tfidf_query[key]
            norm_query = norm_query + tfidf_query[key]**2
            norm_doc = norm_doc + values[key]**2
        norm_query = math.sqrt(norm_query)
        norm_doc = math.sqrt(norm_doc)
        cosine_similarity = dot_prod/(norm_query*norm_doc)
        dic_cosine[keys] = cosine_similarity

    #we store the cosine_similarity of each document with the query in a dictionnary (key = document, value = cosine_similarity
    
    pd.options.display.max_colwidth = 50

    #we compute the same code we used in the first part
    listetitle = []
    listeintro = []
    listeurl = []
    listecosine = []
    for element in results:
        with open(r'C:\Users\danyl\OneDrive\Documents\tsv\document_'+element+'.tsv', encoding = 'utf8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                for row in reader:
                    if len(row)>0:
                        a = row[0]
                        b = row[1]
                listetitle.append(a)
                listeintro.append(b)
                listeurl.append(df.iloc[int(element)][0])
                listecosine.append(round(dic_cosine[element],2)) #we just add the calcul of the cosine similarity of each document
            
    dfresult = pd.DataFrame(list(zip(listetitle, listeintro,listeurl,listecosine)), 
                   columns =['Title', 'Intro', 'URL','Similarity']) 
    dfresult = dfresult.sort_values(by=['Similarity'], ascending = False)
    return(dfresult)
    
    
    


# In[46]:


nbr = int(input("Choose the search engine (1 or 2)"))
query = str(input("Enter your query"))

if nbr == 1:
    result = search_engine1(query)
else: 
    result = search_engine_2(query)

result


# In[ ]:




