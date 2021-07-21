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

plt.style.use('ggplot')


# Functions


def graph_random_embeddings(decade: int, sample: int = None, dim: int = 2, show_words: bool = False):
    '''
    Inputs: decade - chooses which decade to visualize
            sample - selects the number of words to visualize (Leave blank to visualize all words)
            dim - sets the output graph to either 2 or 3 dimensions
            show_words - determine whether or not to label each point
    Outputs: a graph of random word embeddings
    '''
    saved_model, = [model for model in glob('./embeddings_by_decade/*.model') if str(decade) in model]

    w2v = Word2Vec.load(saved_model)

    vectors = w2v.wv

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
                plt.text(x=reduced_vectors[i, 0] + 0.02, y=reduced_vectors[i, 1] + 0.02,
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


def graph_similarity(word1, word2, model):
    """
    computes the cosine similarity between two specified words using a given premade w2v model
    :param word1:
    :param word2:
    :param model:
    :return:
    """
    w2v = Word2Vec.load(model)
    word1_vec = w2v.wv[word1]
    word2_vec = w2v.wv[word2]

    sim_score = cosine(word1_vec, word2_vec)

    return sim_score


if __name__ == '__main__':
    graph_random_embeddings(1600, sample=10, dim=2, show_words=True)