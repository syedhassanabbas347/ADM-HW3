#!/usr/bin/env python
# coding: utf-8

# In[9]:


import urllib.request
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import json
import collections
import math


# In[10]:


# we know that we have 3 documents to parse. This function get the URL of the 3 documents provided, and store them in liste2
#we store the url in a dataframe to let us drop the url that does not work
def file_to_parse(number_of_file_to_parse):    
    liste2 = []
    for k in range(1, number_of_file_to_parse+1):
        i = str(k)
        url = 'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies'+i+'.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for par in soup.select('a'):
            liste2.append(par.text)
    df= pd.DataFrame(liste2)
    df = df.drop(df.index[[9429, 9671,15520,15576,17725,18100,21267,23664,25240,25873,27675,27721,27768,28053,28180,28273,28378,29229]])
    df = df.reset_index()
    return(df)
    


# In[ ]:





# In[5]:





# In[ ]:





# In[ ]:




