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


# In[5]:


import import_ipynb
from collector_utils1 import file_to_parse


# In[ ]:


# we go into each url, we get the content and we save it in html file

df = file_to_parse(3)

for row in df[0:].iterrows():
    response = urllib.request.urlopen(row[1][0])
    webContent = response.read()
    nbr = str(row[0])
    filename = 'article_10000000'
    f = open(filename + ".html", 'wb')
    f.write(webContent)
    f.close


# In[ ]:




