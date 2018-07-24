"""Make Corpus.

Make corpus from explanations from metadata files then save the
corpus as a pickle file.
"""

import json
from nltk.corpus import stopwords as sw
from nltk.tokenize import RegexpTokenizer
import os
from os import path
import pickle

# Metadata directory
METADATA_DIR = path.dirname(path.abspath(__file__)) + '/../resources/metadata/'

# Resources directory
RESOURCES_DIR = path.dirname(path.abspath(__file__)) + '/../resources/'


def get_explanations():
    """Gather all explanations from metadata files."""
    explans = []
    for file in os.listdir(METADATA_DIR):
        with open(METADATA_DIR + file, 'r') as f:
            metadata = json.load(f)
            for m in metadata:
                explans.append(m['explanation'])
    return explans


if __name__ == "__main__":
    print('Making corpus...')

    # Get explanations from metadata files
    explans = get_explanations()

    word_list = []

    tokenizer = RegexpTokenizer(r'\w+')

    # Tokenize sentences, remove non-alphanumeric characters
    # and make lower case
    for e in explans:
        for word in tokenizer.tokenize(e):
            word = word.lower()
            word_list.append(word)

    # Remove stopwords
    words = [word for word in word_list if word not in sw.words('english')]

    pickle.dump(words, open(RESOURCES_DIR + 'corpus.pkl', 'wb'))

    print('Saved corpus to resources directory.')
