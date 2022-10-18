import math

all = 40
spam = 4

def is_spam(words):  # P(спам|{′купите′, ′наш′,′товар′})
    res_p = math.log(p_spam(get_num_all_spam_letters(), get_all()))
    res_q = math.log(p_spam(get_num_all_no_spam_letters(), get_all()))
    for word in words:
        res_p += math.log(word_is_spam(get_num_spam_letters_with_word(), get_num_all_spam_letters()))
        res_q += math.log(word_is_not_spam(get_num_spam_letters_without_word(), get_num_all_spam_letters()))
    return res_p > res_q


# без погрешностей (не используется)
def bayes(words):  # P(спам|{′купите′, ′наш′,′товар′})
    return (p_letter_is_spam(words) /
            (p_letter_is_spam(words) * p_spam(get_num_all_spam_letters(), get_all()) +
             p_letter_is_not_spam(words) * p_spam(get_num_all_no_spam_letters(), get_all()))) \
           > 0.5


def p_spam(spam, all):
    return spam / all


def p_not_spam(norm, all):
    return norm / all


def word_is_spam(num_spam_letters_with_word, num_all_spam_letters):  # P({′купите′|спам)
    return (num_spam_letters_with_word + 1) / (num_all_spam_letters + 2)


def word_is_not_spam(num_spam_letters_without_word, num_all_spam_letters):  # P({′купите′|не спам)
    return (num_spam_letters_without_word + 1) / (num_all_spam_letters + 2)


def get_all():  # всех писем
    return all  # all++


def get_num_spam_letters_with_word():  # спам–писем со словом ’купите’
    return 1  # dictionary[i]?


def get_num_all_spam_letters():  # спам–писем
    return spam  # spam++


def get_num_spam_letters_without_word():  # спам–писем без слова ’купите’
    return get_num_all_spam_letters() - get_num_spam_letters_with_word()


def get_num_all_no_spam_letters():  # не спам–писем
    return get_all() - get_num_all_spam_letters()


def p_letter_is_spam(words):  # P({′купите′, ′наш′,′товар′}|спам)
    res = 1
    for word in words:
        res *= word_is_spam(get_num_spam_letters_with_word(), get_num_all_spam_letters())
    return res


def p_letter_is_not_spam(words):  # P({′купите′, ′наш′,′товар′}|не спам)
    res = 1
    for word in words:
        res *= word_is_not_spam(get_num_spam_letters_without_word(), get_num_all_spam_letters())
    return res
