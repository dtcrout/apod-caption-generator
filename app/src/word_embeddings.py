"""Word Embeddings.

I guess we can assume we will be using different types of word
embeddings so we can make a class here to make what we need...
"""

from collections import Counter
import numpy as np
from os import path
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# Resources directory
RESOURCES_DIR = path.dirname(path.abspath(__file__)) + '/../resources/'


def make_onehot_dict(words):
    """Make onehot vector mapping given a word corpus."""
    words_dict = Counter(words)
    words_list = [key for key in words_dict.keys()]

    # Assign integer labels to words
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(words_list)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)

    # Create onehot vectors with integer labels
    onehot_encoder = OneHotEncoder(sparse=False)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

    # Create mapping
    onehot_dict = dict(zip(words_list, onehot_encoded))

    return onehot_dict


class WordEmbeddings():
    """Word embeddings."""

    def __init__(self):
        """Init variables."""
        self.corpus = pickle.load(open(RESOURCES_DIR + 'corpus.pkl', 'rb'))
        self.onehot_mapping = make_onehot_dict(self.corpus)

    def onehot_encode(self, words):
        embeddings = np.array([self.onehot_mapping[w] for w in words \
                               if w in self.onehot_mapping.keys()])
        return embeddings


if __name__ == "__main__":
    we = WordEmbeddings()
    a = ['hello', 'world', 'this', 'is', 'mars']
    print(we.onehot_encode(a))
