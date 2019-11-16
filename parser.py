# I wrote this code with PyCharm to better organize all the material:
# I created a "utils" python package, containing a single "parser_utils.py" file,
# from which I import all the functions I need

from bs4 import BeautifulSoup
import csv
import os
from utils.parser_utils import Intro
from utils.parser_utils import Plot
from utils.parser_utils import Info

# I take the current working directory path to open all the html files
cwd_path = os.getcwd()

for i in range(10000):

    # Some files have not been found in the download phase, in that case I skip to the next file
    try:
        with open( cwd_path+"/data3/article_"+str(i)+".html", "r") as file_html:
            html = BeautifulSoup( file_html, "html.parser" )
    except FileNotFoundError:
        continue

    # I only consider files containing an info-box because the files without info box are few,
    # about 200-300 for each "moviesn.html" file, so only 2% -3% of the total
    start = html.find("table", {"class": "infobox vevent"})

    if start == None:
        continue

    # I create the dictionary where I will go to save all the information required for the single film
    # I save the title but then I will use the title that appears in the infobox because it is cleaner
    dic = {}

    dic["Title"] = html.title.text[0:-12]

    # See the functions from parser_utils.py
    Intro( html, dic)

    Plot( html, dic)

    Info( html, dic)

    # I save all the information contained in the dictionary in a .tsv file related to the single film
    with open( cwd_path+"/datatsv/document_" + str(i) + ".tsv", "wt", encoding="utf8") as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        tsv_writer.writerow(["Title", "Intro", "Plot", "Director", "Producer",
                             "Writer", "Starring", "Music", "Release date", "Runtime",
                             "Country", "Language", "Budget"])

        tsv_writer.writerow([dic["Film name"], dic["Intro"], dic["Plot"], dic["Director"],
                             dic["Producer"], dic["Writer"], dic["Starring"], dic["Music"],
                             dic["Release date"], dic["Runtime"], dic["Country"],
                             dic["Language"], dic["Budget"]])