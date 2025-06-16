from readability import Readability
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
from nltk.corpus import stopwords
import string

def flesch_score(text):
    r = Readability(text)
    score = r.flesch()
    return score

def sentence_length(text):
    '''
    Returns mean_length, median_length of sentences (in number of words).
    '''
    # Tokenize sentences
    sentences = sent_tokenize(text)

    # Function to count words (excluding punctuation)
    def count_words(sentence):
        words = word_tokenize(sentence)
        words = [word for word in words if word.isalnum()]  # Excludes punctuation
        return len(words)

    # Compute sentence lengths
    sentence_lengths = [count_words(sentence) for sentence in sentences]

    # Compute mean and median
    mean_length = np.mean(sentence_lengths)
    median_length = np.median(sentence_lengths)
    return mean_length, median_length

if __name__=='__main__':
    file_path = os.path.join(os.getcwd(), "downloaded_files", "CONTRIBUTING_transformers.md")
    # filename = '/downloaded_files/flutter_CONTRIBUTING.md'
    with open(file_path, 'r') as text_file:
        content = text_file.read()
    print("Flesch Readability Score = ")
    print(flesch_score(content))
    print("Sentences length = ")
    print(sentence_length(content))