
def is_spam(words, ): # P(спам|{′купите′, ′наш′,′товар′})
    return (p_letter_is_spam(words) /
            (p_letter_is_spam(words) * p_spam(get_num_all_spam_letters(), get_all()) +
             p_letter_is_not_spam(words) * p_spam(get_num_all_no_spam_letters(), get_all())))\
           > 0.5

# P(не спам|{′купите′, ′наш′,′товар′})
def p_spam(spam, all):
    return spam / all

def p_not_spam(norm, all):
    return norm / all

def word_is_spam(num_spam_letters_with_word, num_all_spam_letters): # P({′купите′|спам)
    return (num_spam_letters_with_word+1) / (num_all_spam_letters+2)

def word_is_not_spam(num_spam_letters_without_word, num_all_spam_letters): # P({′купите′|не спам)
    return (num_spam_letters_without_word+1) / (num_all_spam_letters+2)

def get_all(): # всех писем
    return 1 # ?

def get_num_spam_letters_with_word(): # спам–писем со словом ’купите’
    return 1 # ?

def get_num_spam_letters_without_word():  # спам–писем без слова ’купите’
    return 3 # ?

def get_num_all_spam_letters(): # спам–писем
    return 4 # ?

def get_num_all_no_spam_letters(): # не спам–писем
    return get_all() - get_num_all_spam_letters()

def p_letter_is_spam(words): # P({′купите′, ′наш′,′товар′}|спам)
    res = 1
    for word in words:
        num_spam_letters_with_word = get_num_spam_letters_with_word()
        num_all_spam_letters = get_num_all_spam_letters()
        res *= word_is_spam(num_spam_letters_with_word, num_all_spam_letters)
    return res

def p_letter_is_not_spam(words): # P({′купите′, ′наш′,′товар′}|не спам)
    res = 1
    for word in words:
        res *= word_is_not_spam(get_num_spam_letters_without_word(), get_num_all_spam_letters())
    return res
