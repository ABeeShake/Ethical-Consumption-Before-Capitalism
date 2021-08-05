"""
Purpose: Create reproducable code that can be used to generate useful word embedding visualizations
author: Abhishek Devarajan
"""

from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from glob import glob
from scipy.spatial.distance import cosine
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import combinations

plt.style.use('ggplot')


# Functions


def load_model(decade):

    model_list = glob(r'C:\Users\abhis\PycharmProjects\Cosine Similarity\embeddings_by_5_year_group/*.model')

    saved_model, = [model for
                    model in
                    model_list if
                    str(decade) in
                    model]

    w2v = Word2Vec.load(saved_model)

    vectors = w2v.wv

    return vectors

def graph_random_embeddings(decade: int, sample: int = None, dim: int = 2, show_words: bool = False):
    '''
    Inputs: decade - chooses which decade to visualize
            sample - selects the number of words to visualize (Leave blank to visualize all words)
            dim - sets the output graph to either 2 or 3 dimensions
            show_words - determine whether or not to label each point
    Outputs: a graph of random word embeddings
    '''
    vectors = load_model(decade)

    indices = list(vectors.key_to_index.values())

    sampled_indidices = np.random.choice(indices, size=sample) if sample else indices

    sampled_words = [vectors.index_to_key[idx] for idx in sampled_indidices]

    sampled_vectors = np.array(vectors[sampled_indidices])

    reduced_vectors = PCA(random_state=0).fit_transform(sampled_vectors)[:, :dim]

    # print(sampled_words)

    if dim == 2:

        fig = plt.figure(figsize=(10, 10))
        sns.scatterplot(x=reduced_vectors[:, 0], y=reduced_vectors[:, 1])

        if show_words:
            for i in range(reduced_vectors.shape[0]):
                plt.text(x=reduced_vectors[i, 0] + 0.01, y=reduced_vectors[i, 1] + 0.01,
                         s=sampled_words[i],
                         fontdict=dict(color='black', size=10),
                         bbox=dict(facecolor='yellow', alpha=0.5))
        plt.title(f'Embeddings of {sample if sample else len(indices)} Random Words from {decade}s')
        plt.show()

    elif dim == 3:

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(xs=reduced_vectors[:, 0],
                   ys=reduced_vectors[:, 1],
                   zs=reduced_vectors[:, 2])
        plt.title(f'Embeddings of {sample if sample else len(indices)} Random Words from {decade}s')
        plt.show()


def cosine_similarity(pair, vectors):

    '''
    Word2Vec.wv.similarity(word1,word2)
    '''
    word1, word2 = pair

    sim = vectors.similarity(word1,word2)

    return sim


def generate_heatmap_matrix(lexicon,decade):

    vectors = load_model(decade)

    pairs = list(combinations(lexicon, 2))

    sim_scores = [cosine_similarity(pair, vectors) for pair in pairs]

    sim_df = pd.DataFrame({'pair': pairs, 'similarity': sim_scores})

    sim_df['word1'] = sim_df['pair'].apply(lambda x: lexicon.index(x[0]))
    sim_df['word2'] = sim_df['pair'].apply(lambda x: lexicon.index(x[1]))

    sim_df['pair'] = list(zip(sim_df.word1, sim_df.word2, sim_df.similarity))

    df_hm = pd.DataFrame({'word1': range(len(lexicon)),
                          'word2': range(len(lexicon)),
                          'similarity': pd.Series(np.ones(len(lexicon)))})

    df_hm = df_hm.pivot(index='word1', columns='word2').fillna(0)

    for row, col, similarity in sim_df.pair:

        df_hm.iloc[col,row] = similarity

    return df_hm


def plot_heatmap(lexicon, decade):

    df_hm = generate_heatmap_matrix(lexicon,decade)

    mask = np.zeros_like(df_hm)
    mask[np.triu_indices_from(mask)] = True

    # print(df_hm)
    sns.set_style('ticks')

    sns.heatmap(df_hm,
                mask = mask,
                xticklabels = lexicon,
                yticklabels = lexicon,
                annot = True)
    plt.xlabel('word 1')
    plt.ylabel('word 2')
    plt.title(f'Cosine Similarity Between Word-Pairs ({decade})')
    plt.show()

if __name__ == '__main__':

    lexicon = ['christ','god','church', 'king', 'lord', 'ale']

    plot_heatmap(lexicon, 1600)

    '''
    queen = king - man + woman
    '''