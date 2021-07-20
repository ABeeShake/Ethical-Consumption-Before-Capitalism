'''
Purpose: Create preprocessing functions to clean text

Author: Abhishek Devarajan
'''

import pandas as pd
import swifter
import string
import nltk
# nltk.download()
from nltk.corpus import stopwords

##Functions##

#remove punctuation:
def punct_remover(text:str):

    return ''.join([letter for letter in text if letter not in string.punctuation])

#tokenize text:

def tokenizer(text):

    return text.split()

#remove stopwords:

languages_to_filter = ['french','german','greek']
stops = stopwords.words('english')

for language in languages_to_filter:

    stops.append(stopwords.words(language))


def stopwords_remover(text: list[str]):

    return [word for word in text if word not in stops]

#Complete Preprocessing:

def preprocess(df):

    print('Beginning Preprocessing')
    print('Removing Punctuation')
    df['text'] = df['text'].swifter.apply(punct_remover)
    print('Tokenizing Texts')
    df['text'] = df['text'].swifter.apply(tokenizer)
    print('Removing Stopwords')
    df['text'] = df['text'].swifter.apply(stopwords_remover)

    print('Done Preprocessing')
    
    return df


if __name__ == '__main__':

    df = pd.read_csv('./A30_P5.csv')

    df.drop(['index','author','publisher','title'], axis = 1, inplace = True)

    df = preprocess(df)