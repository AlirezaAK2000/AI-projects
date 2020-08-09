"""
in this file we preprocess data to prepare and smooth for
learning
"""

import re
from app_constants import WEB_TAG, DIGIT_TAG, UNK_TAG


# read train set
def get_data(path):
    with open(path, '+r') as file:
        lines = format_data(file.readlines())
        lines = find_unk(lines)
        return lines


# replace rare words with <unk>
def find_unk(lines):
    curpus = ' ////// '.join(lines)
    words = set(curpus.split())
    for word in words:
        if curpus.count(word) == 1:
            curpus = curpus.replace(word, UNK_TAG)
    lines = curpus.split(' ////// ')
    return lines


def format_data(lines):
    # replace websites and links with <web>
    formatted_lines = list(map(
        lambda x: re.sub('https?\s*:\s*/\s*/\s*[^\s<>"]*|www\.[^\s<>"]*', WEB_TAG,
                         x), lines))
    # remove punctuation marks
    formatted_lines = list(map(lambda x: re.sub("[^a-zA-Z.0-9$]", ' ', x), formatted_lines))
    # replace digits with <num>
    formatted_lines = list(map(lambda x: re.sub('\d{1,}', f' {DIGIT_TAG} ', x), formatted_lines))
    # remove redundant white spaces
    formatted_lines = [' '.join(line.strip().lower().split()) for line in formatted_lines]
    # start and end tag for trigram model
    formatted_lines = ['<s> ' * 2 + line + ' <s/>' for line in formatted_lines]
    return formatted_lines


# generate ngram
def generate_n_gram(n, lines):
    grams = []
    for sentence in lines:
        words = sentence.split()
        for i in range(len(words) - n):
            gram = words[i:i + n]
            if gram not in grams:
                grams.append(gram)
    return grams


# read test sentences and labels
def read_test(pathes):
    with open(pathes[0], '+r') as file:
        lines = format_data(file.readlines())
    with open(pathes[1], '+r') as file:
        labels = list(map(lambda x: re.sub('[^a-zA-Z.$]', ' ', x), file.readlines()))
        labels = [' '.join(label.strip().lower().split()) for label in labels]
    return lines, labels
