from bs4 import BeautifulSoup
import csv
import os

def SepName(s):

    for i in range(1, len(s)):
        if s[i].isupper() and s[i - 1] != " ":
            s = s[:i] + ' ' + s[i:]

    return s

cwd_path =os.getcwd()

for i in range(10000):

    try:
        with open( cwd_path+"/data3/article_"+str(i)+".html", "r") as file_html:
            html = BeautifulSoup( file_html, "html.parser" )
    except FileNotFoundError:
        continue

    dic = {}

    start = html.find( "table", {"class" : "infobox vevent"} )

    if start == None:
        continue

    dic["Title"] = html.title.text[0:-12]

    tag = "p"
    intro = ""

    while tag=="p":

        paragraph =  start.find_next_sibling()
        tag = paragraph.name

        if tag=="p":
            intro += paragraph.text

        start = paragraph

    dic["Intro"] = intro

    dic["Plot"] = "NA"
    start = html.find("span", {"class": "mw-headline"})

    try:
        while start["id"] != "Plot" and start["id"] != "Plot_summary" and start["id"] != "Premise" and start["id"] != "Summary":
            start = start.find_next("span", {"class": "mw-headline"})

        start = start.find_parent()
        tag = "p"
        plot = ""

        while tag=="p":

            paragraph =  start.find_next_sibling()
            tag = paragraph.name

            if tag=="p":
                plot += paragraph.text

            start = paragraph

        dic["Plot"] = plot

    except:
        pass

    info_box = html.find("table", {"class": "infobox vevent"})
    start = info_box.find("tr")
    dic["Film name"] = start.text

    start = start.find_next("th")
    start = start.find_parent()
    tag = "tr"

    dic["Director"] = dic["Producer"] = dic["Writer"] = dic["Starring"] = dic["Music"] = dic["Release date"] = dic[
        "Runtime"] = dic["Country"] = dic["Language"] = dic["Budget"] = "NA"

    while (tag == "tr"):

        line = start.find_next_sibling()

        try:
            info = line.find_next()
        except:
            break

        tag = line.name
        start = line

        if info.text == "Directed by":
            dic["Director"] = SepName( info.find_next("td").text )

        elif info.text == "Produced by":
            dic["Producer"] = SepName( info.find_next("td").text )

        elif info.text == "Written by":
            dic["Writer"] = SepName( info.find_next("td").text )

        elif info.text == "Starring":
            dic["Starring"] = SepName( info.find_next("td").text )

        elif info.text == "Music by":
            dic["Music"] = SepName( info.find_next("td").text )

        elif info.text == "Release date":
            dic["Release date"] = info.find_next("td").text

        elif info.text == "Running time":
            dic["Runtime"] = info.find_next("td").text

        elif info.text == "Country":
            dic["Country"] = info.find_next("td").text

        elif info.text == "Language":
            dic["Language"] = SepName( info.find_next("td").text )

        elif info.text == "Budget":
            dic["Budget"] = info.find_next("td").text


    with open( cwd_path+"/datatsv/document_" + str(i) + ".tsv", "wt", encoding="utf8") as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(["Title", "Intro", "Plot", "Director", "Producer",
                             "Writer", "Starring", "Music", "Release date", "Runtime",
                             "Country", "Language", "Budget"])
        tsv_writer.writerow([dic["Film name"], dic["Intro"], dic["Plot"], dic["Director"],
                             dic["Producer"], dic["Writer"], dic["Starring"], dic["Music"],
                             dic["Release date"], dic["Runtime"], dic["Country"],
                             dic["Language"], dic["Budget"]])
