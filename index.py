#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.request
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import json
import collections
import math


# In[3]:


pip install import-ipynb


# In[9]:


import import_ipynb

from index_utils import preprocess, index_1, index_2


# In[ ]:


dic_index, listemot, listedoc = index_1() 
dic_index2, listemot2, listedoc2, doc_count_words = index_2()


# In[ ]:


#we store the dictionnary created above in a json file
with open('dic1.json', 'w') as json_file:
    json.dump(dic_index, json_file)
#we store the list of words
with open('dicvoc.json', 'w') as json_file:
    json.dump(listemot, json_file)
with open('listedoc.json', 'w') as json_file:
    json.dump(listedoc, json_file)


# In[ ]:


# we store out results in a json file
with open('dic2.json', 'w') as json_file:
    json.dump(dic_index2, json_file)
with open('listedoc2.json', 'w') as json_file:
    json.dump(listedoc2, json_file)
with open('dicvoc.json', 'w') as json_file:
    json.dump(listemot2, json_file)
with open('number_words_doc.json', 'w') as json_file:
    json.dump(doc_count_words, json_file)


# In[ ]:




