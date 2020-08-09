"""
learning tools for process train corpus for nlp model
and test corpus for lambda Coefficients for back off
"""

from collections import defaultdict
from pre_processing_tools import generate_n_gram
import random
from app_constants import MOST_COMMON
from functools import reduce
import math
from copy import deepcopy


# learning corpus
def learn(lines):
    unigrams = defaultdict(lambda: 0)
    bigrams = defaultdict(lambda: defaultdict(lambda: 0))
    trigrams = defaultdict(lambda: defaultdict(lambda: 0))
    text = ' '.join(lines)
    s = len(text)
    p_unigrams = defaultdict(lambda: 1 / s)
    p_bigrams = defaultdict(lambda: defaultdict(lambda: 1 / s))
    p_trigrams = defaultdict(lambda: defaultdict(lambda: 1 / s))
    words = set()
    for k in generate_n_gram(1, lines):
        unigrams[k[0]] += text.count(k[0])
        p_unigrams[k[0]] = unigrams[k[0]] / s
        words.add(k[0])
        assert (p_unigrams[k[0]] <= 1)

    print('unigrams computed')
    for k in generate_n_gram(2, lines):
        tmp = ' '.join(k)
        bigrams[k[0]][k[1]] += text.count(tmp)
        p_bigrams[k[0]][k[1]] = bigrams[k[0]][k[1]] / unigrams[k[0]]
        assert (p_bigrams[k[0]][k[1]] <= 1)

    print('bigrams computed')
    for k in generate_n_gram(3, lines):
        tmp = ' '.join(k)
        trigrams[(k[0], k[1])][k[2]] += text.count(tmp)
        p_trigrams[(k[0], k[1])][k[2]] = trigrams[(k[0], k[1])][k[2]] / bigrams[k[0]][k[1]]
        assert (p_trigrams[(k[0], k[1])][k[2]] <= 1)

    print('trigrams computed')
    return {
        'trigram': p_trigrams,
        'bigram': p_bigrams,
        'unigram': p_unigrams,
        'words': words,
        'size': s
    }


# predict words for blank spaces
def predict(words, model, real, some_random_words, landa):
    unigram, bigram, trigram = model['unigram'], model['bigram'], model['trigram']
    # a set for choose best word with highest probability
    predicts = set(
        list(trigram[(words[0], words[1])].keys()) + list(bigram[words[1]].keys()) + some_random_words).difference(
        MOST_COMMON)
    max_prob = -1
    best_pr = ''
    print(f'predict set has it : {real in predicts}\n')
    print(f'prediction set : {len(predicts)}\n')
    for pr in predicts:
        prob = get_prob(unigram, bigram, trigram, pr, words, landa)
        if prob > max_prob:
            max_prob = prob
            best_pr = pr

    return best_pr


# random lambda for testing performance
def get_random_landas(seed):
    random.seed(seed)
    arr = [random.randint(1, 100) for _ in range(3)]
    s = sum(arr)
    arr = list(map(lambda x: x / s, arr))
    return arr


# back off formula
def back_off(unigram, bigram, trigram, words, landa):
    return landa[0] * trigram[(words[0], words[1])][words[2]] + landa[1] * bigram[words[1]][words[2]] + landa[2] * \
           unigram[words[2]]


# calculate probability with back off model
def get_prob(unigram, bigram, trigram, pr, words, landa):
    tmp = [[words[0], words[1], pr], [words[1], pr, words[2]], [pr, words[2], words[3]]]
    prob = reduce(lambda x, y: x * y, [back_off(unigram, bigram, trigram, t, landa) for t in tmp])
    return prob


# random rare words for prediction set
def get_random_words(unigram):
    m = min(unigram.values())
    random_words = list(filter(lambda x: unigram[x] <= m, unigram.keys()))

    def select_random(seed=1):
        random.seed(seed)
        words = random.choices(random_words, k=100)
        return words

    return select_random


# distance from real probability
def cost_function(y_hat, y):
    return math.fabs(y_hat ** 2 - y ** 2)


# test random lambda for choosing best Coefficients
def learn_landas(lines_test, labels, model, num_iteration=100):
    all_landas = dict()
    tester = test(lines_test, labels, model)
    for i in range(num_iteration):
        landa = get_random_landas(i)
        print(f'---{i}--')
        count, cost = tester(landa)
        print(f'total cost: {cost} count: {count} Landa : {landa}')
        try:
            if all_landas[count][0] > cost:
                all_landas[count] = [cost, landa]
        except:
            all_landas[count] = [cost, landa]
        if i % 100 == 0:
            print(f'\n\n***min cost in {i} : {max(all_landas.keys())}***\n\n')
    ma = max(all_landas.keys())
    return all_landas[ma], ma


# test on test corpus
def test(lines, labels, model):
    lines_splited = [line.split() for line in lines]
    unigram, bigram, trigram = deepcopy(model['unigram']), deepcopy(model['bigram']), deepcopy(model['trigram'])
    pieces = [line[line.index('$') - 2:line.index('$')] + line[line.index('$') + 1:line.index('$') + 3] for line in
              lines_splited]

    random_selector = get_random_words(model['unigram'])

    print('testing started')

    def test_over_set(landa):
        counter = 0
        cost = 0
        real_word_probs = [get_prob(unigram, bigram, trigram, labels[i], pieces[i], landa) for i in range(len(labels))]
        for i in range(len(lines)):
            print('--------------------------------\n')
            print(f'sentence : {i}\n')
            print(pieces[i])
            r = random_selector(i)
            s = predict(pieces[i], model, labels[i], r, landa)
            if s == labels[i]:
                counter += 1
                print(
                    f"success : predicted : {s}:{unigram[s]} , real : {labels[i]} :{unigram[labels[i]]}\n")
                print(r)
            else:
                pass
                print(
                    f"failure : predicted : {s}:{model['unigram'][s]} , real : {labels[i]}: {model['unigram'][labels[i]]}\n")
            print(f"trained data has it: {labels[i] in model['words']}")
            real_word_prob = real_word_probs[i]
            predicted_word_prob = get_prob(model['unigram'], model['bigram'], model['trigram'], s, pieces[i], landa)
            cost += cost_function(real_word_prob, predicted_word_prob)

        print(f'total cost: {cost} count: {counter}')
        return counter, cost

    return test_over_set
