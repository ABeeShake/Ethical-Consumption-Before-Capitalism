'''
Purpose: Create preprocessing functions to clean text
Author: Abhishek Devarajan
'''

import pandas as pd
import re
import swifter
import string
import nltk
#nltk.download()
from nltk.corpus import stopwords


##Functions##

# remove punctuation:
def punct_remover(text: str):
    return text.translate(str.maketrans('','', string.punctuation))

# remove stopwords:

languages_to_filter = ['french', 'german', 'greek']
stops = stopwords.words('english')

for language in languages_to_filter:
    stops.append(stopwords.words(language))


def stopwords_remover(text:str):
    en = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    fr = re.compile(r'\b(' + r'|'.join(stopwords.words('french')) + r')\b\s*')
    ge = re.compile(r'\b(' + r'|'.join(stopwords.words('german')) + r')\b\s*')
    text = en.sub('', text)
    text = fr.sub('',text)
    text = ge.sub('',text)

    return text

# tokenize text:


def tokenizer(text):
    return text.split()

# Fix Dates:


def date_cleaner(date:str or int):

    if type(date) == str:
        return int(date[2:6]) if date[2:6] not in 'Date Not Found' else 0
    else:
        return date


def make_5year_groups(date:int):

    mod = date % 10
    decade = (date // 10) * 10

    if mod < 5:
        return f'{decade} - {decade + 4}'
    else:
        return f'{decade + 5} - {decade + 9}'

# Complete Preprocessing:

def preprocess(df):
    print('Beginning Preprocessing')
    print('Fixing Dates')

    df['date'] = df['date'].swifter.apply(date_cleaner)
    df = df.loc[(df['date'] <= 1660) & (df['date'] >= 1500)]

    print('Creating 5 Year Groups')
    df['5_year_group'] = df['date'].swifter.apply(make_5year_groups)
    print('Removing Punctuation')
    df['text'] = df['text'].swifter.apply(punct_remover)
    print('Removing Stopwords')
    df['text'] = df['text'].swifter.apply(stopwords_remover)
    print('Tokenizing Texts')
    df['text'] = df['text'].swifter.apply(tokenizer)

    print('Done Preprocessing')

    return df


if __name__ == '__main__':
    df = pd.read_csv(r'C:\Users\abhis\PycharmProjects\Cosine Similarity\A0_P4.csv')

    df.drop(['index', 'author', 'publisher', 'title'], axis=1, inplace=True)

    df = preprocess(df)