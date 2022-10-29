import math
import re

all_let = 0
spam_let = 0
dictionary = dict()


# P({′купите′}|спам) = # (спам–писем со словом ’купите’ + 1) / (спам–писем + 2)
# P({′купите′}|не спам) = # (спам–писем без слова ’купите’ + 1) / (спам–писем + 2)
def word_is_spam(num_spam_letters_with_word, num_all_spam_letters=all_let):
    return (num_spam_letters_with_word + 1) / (num_all_spam_letters + 2)


# log(P(спам)) + ∑log(P(𝑤𝑘|спам)) > log(P(не спам)) + ∑log(P(𝑤𝑘|не спам))
def is_spam(words):
    res_p = math.log(spam_let / all_let)
    res_q = math.log((all_let - spam_let) / all_let)
    for word in words:
        list = dictionary.get(word)
        if list is None:
            list = [1, 1]
        res_p += math.log(word_is_spam(list[1], spam_let))
        res_q += math.log(word_is_spam(list[0], spam_let))
    return res_p > res_q


def learn():
    global spam_let, all_let
    with open('learnCollection.txt', 'r', encoding='utf-8') as inp_file:
        inp_data = inp_file.read()
    letters = inp_data.split('\n')
    for i in range(len(letters)):
        tab = letters[i].split('\t', 1)
        words = set(re.findall(r'[A-Za-zÀ-ÿ0-9_&]+', tab[1].lower()))
        if tab[0] != 'ham':
            spam_let += 1
        for word in words:
            list = dictionary.get(word)
            if list is None:
                list = [0, 0]
            if tab[0] != 'ham':
                list[1] += 1
            else:
                list[0] += 1
            dictionary.update({word: list})
    all_let += len(letters)


def get_accuracy():
    well_amount = 0
    with open('checkCollection.txt', 'r', encoding='utf-8') as inp_file:
        inp_data = inp_file.read()
    letters = inp_data.split('\n')
    for i in range(len(letters)):
        tab = letters[i].split('\t', 1)
        words = set(re.findall(r'[A-Za-zÀ-ÿ0-9_&\']+', tab[1].lower()))
        if is_spam(words) == (tab[0] != 'ham'):
            well_amount += 1
    return well_amount / len(letters)


learn()
print(f"Точность {round(get_accuracy() * 100, 2)}%")
