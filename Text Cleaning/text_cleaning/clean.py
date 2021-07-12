from bs4 import BeautifulSoup
import pandas as pd
import re
import os

"""
Created on 6/18/2021
"""
# structural garbage
pageA = re.compile('Page Â')
pageUn1 = re.compile(r'Page  \[unnumbered]')
pageUn2 = re.compile(r'Page \[unnumbered]')
# PageNum = re.compile(r'Page  [0123456789]')
pageNum = re.compile(r'page  [0123456789]', re.IGNORECASE)
Un = re.compile(r'\[unnumbered]')
illust = re.compile(r'\[illustration]', re.IGNORECASE)
# Illust = re.compile(r'\[Illustration]')
# Chapter = re.compile('Chapter [0123456789]')
chapter = re.compile('chapter [0123456789]', re.IGNORECASE)
# Chapt1 = re.compile(r'Chapt\. [0123456789]')
chapt1 = re.compile(r'chapt\. [0123456789]', re.IGNORECASE)
# Chapt = re.compile('Chapt [0123456789]')
chapt = re.compile('chapt [0123456789]', re.IGNORECASE)
structural_garbage = [pageA, pageUn1, pageUn2, pageNum, Un, illust, chapter,
                      chapt1, chapt]

# some punctuation
amper = re.compile('&amp')
dash = re.compile('—')
line = re.compile('∣')
# etc.
etc = re.compile('&amp;c')

# text accents
above = re.compile('̄')
a = re.compile('[àáâãäå]')
A = re.compile('[ÀÁÂÃÄÅ]')
e = re.compile('[ęèéêë]')
E = re.compile('[ÈÉÊË]')
ii = re.compile('[ìíîï]')
II = re.compile('[ÌÍÎÏ]')
o = re.compile('[òóôõö]')
O = re.compile('[ÒÓÔÕÖ]')
u = re.compile('[ùúûü]')
U = re.compile('[ÙÚÛÜ]')
c = re.compile('ç')
C = re.compile('Ç')
ae = re.compile('æ')
AE = re.compile('Æ')
oe = re.compile('œ')
thorn = re.compile('[þÞ]')
B = re.compile('ß')

# finally, everything else (except hyphens and apostrophes)
everything = re.compile(r"[^a-zA-Z'\- ]")

# then, attempt to get rid of roman numerals (except those containing exactly one I)
roman = re.compile(r"\b((?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?(I{0}|I{2,})))\b",
                   re.IGNORECASE)

# finally, remove extra spaces
spaces = re.compile(r" {2,}")


def clean_text(txt):
    '''
    inputs: soup - texts scraped from xml files using beautiful soup
    output: cleaned_texts - list containing the cleaned text elements in the following order:
                            1. body text, 2. title, 3. author, 4. publisher
    '''

    text1 = txt.replace("\n", " ")
    temp = text1
    for trash in structural_garbage:
        temp = trash.sub("", temp)
    temp = amper.sub("and", temp)
    temp = dash.sub(" ", temp)
    temp = above.sub("", temp)
    temp = a.sub("a", temp)
    temp = A.sub("A", temp)
    temp = e.sub("e", temp)
    temp = E.sub("E", temp)
    temp = ii.sub("i", temp)
    temp = II.sub("I", temp)
    temp = o.sub("o", temp)
    temp = O.sub("O", temp)
    temp = u.sub("u", temp)
    temp = U.sub("U", temp)
    temp = c.sub("c", temp)
    temp = C.sub("C", temp)
    temp = ae.sub("ae", temp)
    temp = AE.sub("AE", temp)
    temp = oe.sub("oe", temp)
    temp = thorn.sub("th", temp)
    temp = B.sub("B", temp)

    # remove everything else, except for hyphens, apostrophes, letters, and spaces
    temp = everything.sub("", temp)

    # replace 'andc' artifact with &c
    # delete roman numerals (except for I)
    temp = etc.sub("etc", temp)
    temp = roman.sub("", temp)
    temp = spaces.sub(" ", temp)
    temp = temp.lower()

    return temp


def find_body(soup,body_tag):
    bodies = soup.find_all(body_tag)
    body = ''
    for i in bodies:
        body += i.get_text()

    body = clean_text(body)

    return body


def find_title(soup):
    titles = soup.find_all('title')
    title = titles[-1].get_text()

    title = clean_text(title)

    return title


def find_author(soup):
    authors = soup.find_all('author')
    author = list(set([a.get_text() for a in authors]))
    if len(author) == 0:
        author = 'No Author'
    else:
        author = author[-1]

    author = clean_text(author)

    return author


def find_publisher(soup):
    publishers = soup.find_all('publisher')
    publisher = publishers[-1].get_text()

    publisher = clean_text(publisher)

    return publisher


def find_date(soup):
    dates = soup.find_all('date')
    datelist = [date.get_text() for date in dates]
    date1 = set([(re.search(r'[1][0-9]{3}', date)).group()
                     for date
                     in datelist
                     if re.search(r'[1][0-9]{3}', date)
                     is not None])

    if len(date1) == 0:
        date1 = 'Date Not Found'
    else:
        date1 = int(min(date1))

    return date1


# extract information from file
def parse_xml(soup,body_tag):
    '''infile = open(file1, "r")
    contents = infile.read()
    soup = BeautifulSoup(contents, 'xml')'''

    title = find_title(soup)
    author = find_author(soup)
    publisher = find_publisher(soup)
    date = find_date(soup)
    body = find_body(soup,body_tag)

    return title, author, publisher, date, body


def make_csv(new_row,folder_name, output_folder):
    """
    inputs: folder_name - name of the folder from which the texts were extracted
            output_folder - where to output the csv
    """
    cols = ['index','title', 'author', 'publisher', 'date', 'text']
    df = pd.DataFrame(dict(zip(cols,new_row)), columns=cols)
    df.to_csv(os.path.join(output_folder, folder_name) + '.csv', index = False)


if __name__ == '__main__':

    with open(r'C:\Users\abhis\Documents\CollegeDocs\Data+\B2_P4\B2\B21478.P4.xml', 'rb') as f:
        contents = f.read()
        Soup = BeautifulSoup(contents, 'html.parser')
        doc_elements = parse_xml(Soup)
    print(doc_elements[1])