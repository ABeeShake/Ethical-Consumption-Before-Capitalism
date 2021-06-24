from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import os

"""
Created on 6/18/2021

@author: erika
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


def clean_text():
    bodies = soup.find_all('div1')
    text = ''
    for i in bodies:
      text += i.get_text()
      #print(text)

    text1 = text.replace("\n", " ")
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

def find_date():
    dates = soup.find_all('date')
    datelist = [date.get_text() for date in dates]
    date1 = min(set([(re.search(r'[1][0-9]{3}', date)).group()
                  for date
                  in datelist
                  if re.search(r'[1][0-9]{3}', date)
                  is not None]))

    return date1


# extract information from file
def parse_xml():
    '''infile = open(file1, "r")
    contents = infile.read()
    soup = BeautifulSoup(contents, 'xml')'''

    titles = soup.find_all('title')
    title = list(set([t.get_text()
                      for t 
                      in titles
                      if 'Early English books online' not in t.get_text()]))

    authors = soup.find_all('author')
    author = list(set([a.get_text() for a in authors]))
    if len(author) == 0:
      author.append('No Author')

    publishers = soup.find_all('publisher')

    publisher = [publishers[-1].get_text()]

    date1 = [find_date()]
    text1 = clean_text()

    return title, author, publisher, date1, text1



def make_csv(file_name, title, author, publisher, date1, text1, output_folder):
    rows = {'title': [title], 'author': [author], 'publisher':[publisher], 'date': [date1], 'text': [text1]}
    df = pd.DataFrame.from_dict(rows)
    df.to_csv(os.path.join(output_folder, file_name) + '.csv')
''''
def make_text(file_name, title, author, publisher, date1, text1, output_folder): 
  rows = {'title': [title], 
          'author': [author],
          'publisher': [publisher], 
          'date': [date1], 
          'text': [text1]}
  df = pd.DataFrame.from_dict(rows)
  #df.to_csv(output_folder + '/' + file_name + '.csv')

  np.savetxt(output_folder + '/' + file_name + '.txt',
            df.values, 
            fmt = '%s', 
            delimiter = '\n')
'''

if __name__ == '__main__':

  file_dir = './Test Files A'
  output_dir = './Testing Output'

  #file = 'A50002.P4.xml'
  #with open(os.path.join(file_dir, file), 'r') as f:
    #contents = f.read()
    #soup = BeautifulSoup(contents, 'html.parser')
    #t, auth, d, txt = parse_xml()
    #make_text(file[:-4], t, auth, d, txt, output_dir)

  for file in os.listdir(file_dir):
    print(file)
    with open(os.path.join(file_dir, file), 'r') as f:
      contents = f.read()
      soup = BeautifulSoup(contents, 'html.parser')
      t, auth, p, d, csv = parse_xml()
      make_csv(file[:-4], t, auth, p, d, csv, output_dir)