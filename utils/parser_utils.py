from bs4 import BeautifulSoup


# We need this function to separate some proper names that will appear in some values of the dictionary,
# for example the value associated to the key "Starring"
def SepName(s):

    for i in range(1, len(s)):
        if s[i].isupper() and s[i - 1] != " ":
            s = s[:i] + " " + s[i:]

    return s


# This function parses the intro
def Intro( html, dic):

    # We start from the table because the intro is always on the same level of the table
    start = html.find( "table", {"class" : "infobox vevent"} )

    tag = "p"
    intro = ""

    # Then we add all the intro paragraphs text in the string "intro";
    # when the first tag different from "p" is found, the loop ends.
    # There is always an intro so we don't need to set the intro to NA in advance
    while tag == "p":

        paragraph = start.find_next_sibling()
        tag = paragraph.name

        if tag == "p":
            intro += paragraph.text

        start = paragraph

    dic["Intro"] = intro


# This function parses the plot
def Plot( html, dic):

    dic["Plot"] = "NA"

    # Here we start from "span" {"class": "mw-headline"} because it indicates the title of a new Wikipedia section
    start = html.find("span", {"class": "mw-headline"})

    # If there is a section linked to the plot, we take it; otherwise we leave the value set to NA and we do nothing
    # in the exception with "pass"
    try:

        # We scroll through all the sections until we find one named in the following way.
        # These are all the possible titles of the sections linked to the plot, found by examining all the files
        while start["id"] != "Plot" and start["id"] != "Plot_summary" and start["id"] != "Premise" and start[
            "id"] != "Summary":
            start = start.find_next("span", {"class": "mw-headline"})

        # We go back up the hierarchy of a level because the paragraphs containing the plot are on the same level
        # as the "h2" tags, which contain "span": this because later we want to scroll the siblings
        # in the same way proposed in Plot function
        start = start.find_parent()
        tag = "p"
        plot = ""

        while tag == "p":

            paragraph = start.find_next_sibling()
            tag = paragraph.name

            if tag == "p":
                plot += paragraph.text

            start = paragraph

        dic["Plot"] = plot

    except:
        pass


# This function parses the info box
def Info( html, dic):

    # Here we start from the info box itself
    info_box = html.find("table", {"class": "infobox vevent"})

    # The first content with the "tr" tag is always the name of the movie
    start = info_box.find("tr")
    dic["Film name"] = start.text

    # We find the next "th" tags because they are the ones containing the requested information:
    # usually there is an image of the movie poster that in this way is skipped since it has tag "td"
    start = start.find_next("th")
    start = start.find_parent()
    tag = "tr"

    # We set all values ​​to NA in advance
    dic["Director"] = dic["Producer"] = dic["Writer"] = dic["Starring"] = dic["Music"] = dic["Release date"] = dic[
        "Runtime"] = dic["Country"] = dic["Language"] = dic["Budget"] = "NA"

    # Here too we scroll all the "tr" tags and analyze their content
    while (tag == "tr"):

        line = start.find_next_sibling()

        # Instead the information is always contained at a lower level than the variable "line".
        # If these informations are somehow not contained in the html file,
        # we risk an infinite loop: the exception is for this
        try:
            info = line.find_next()
        except:
            break

        tag = line.name
        start = line

        # We save the information of interest in the dictionary
        if info.text == "Directed by":
            dic["Director"] = SepName(info.find_next("td").text)

        elif info.text == "Produced by":
            dic["Producer"] = SepName(info.find_next("td").text)

        elif info.text == "Written by":
            dic["Writer"] = SepName(info.find_next("td").text)

        elif info.text == "Starring":
            dic["Starring"] = SepName(info.find_next("td").text)

        elif info.text == "Music by":
            dic["Music"] = SepName(info.find_next("td").text)

        elif info.text == "Release date":
            dic["Release date"] = info.find_next("td").text

        elif info.text == "Running time":
            dic["Runtime"] = info.find_next("td").text

        elif info.text == "Country":
            dic["Country"] = info.find_next("td").text

        elif info.text == "Language":
            dic["Language"] = SepName(info.find_next("td").text)

        elif info.text == "Budget":
            dic["Budget"] = info.find_next("td").text


