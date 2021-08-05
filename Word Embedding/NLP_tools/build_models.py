### Imports ###
# sentiment analysis tools
from gensim.models import Word2Vec
import pandas as pd
from scipy.spatial.distance import cosine
from glob import glob
from NLP_tools.preprocessing import preprocess


### Create Dataset ###


def gather_files(dir):
    """
    gathers csv files from current directory to create a dataframe
    :return: dataframe
    """

    files = glob(dir + '/*.csv')

    df = pd.concat([pd.read_csv(file) for file in files])

    return df


def make_dataset(dir):
    """
    reformats dataframe
    :param df: dataframe to reformat
    :return: cleaned dataframe
    """
    df = gather_files(dir)

    df.drop(['index', 'author', 'publisher', 'title'], axis=1, inplace=True)

    df.drop_duplicates(inplace=True)

    df.reset_index(drop=True, inplace=True)

    df = preprocess(df)

    print(df.shape)

    return df


### Create Embeddings ###


def embed_by_year_group(df, group):
    w2v = Word2Vec(sentences=df[df['5_year_group'] == group]['text'], min_count=1, window=5, workers=6)

    w2v.save(rf'C:\Users\abhis\PycharmProjects\Cosine Similarity\embeddings_by_decade\{group}.model')


if __name__ == "__main__":

    build_model = True

    print('Building Model' if build_model else 'Skipping Build')

    df = make_dataset(dir = r'C:\Users\abhis\PycharmProjects\TextCleaning')

    print('Finished Building Dataset')