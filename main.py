import math
import re

all_let = 0
spam_let = 0
dictionary = dict()


def is_spam(words):  # P(спам|{′купите′, ′наш′,′товар′})
    res_p = math.log(spam_let / all_let)
    res_q = math.log(get_num_all_no_spam_letters() / all_let)
    for word in words:
        res_p += math.log(word_is_spam(get_num_letters_with_word(word, 1), spam_let))
        res_q += math.log(word_is_spam(get_num_letters_with_word(word, 0), spam_let))
    return res_p > res_q


def word_is_spam(num_spam_letters_with_word, num_all_spam_letters=all_let):  # P({′купите′}|спам) or P({′купите′}|не спам)
    return (num_spam_letters_with_word + 1) / (num_all_spam_letters + 2)


# spam=1 - спам–писем со словом word, spam=0 - спам-писем без слова word
def get_num_letters_with_word(word, spam=0):  # спам–писем со словом ’купите’
    list = dictionary.get(word)
    if list is None:
        return 1
    return list[spam]


def get_num_all_no_spam_letters():  # не спам–писем
    return all_let - spam_let


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
