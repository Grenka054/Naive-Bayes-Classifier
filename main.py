import math
import re

all_mails = 0
spam_mails = 0
dictionary = dict()


# P({′купите′}|спам) = # (спам–писем со словом ’купите’ + 1) / (писем со словом ’купите’ 2)
# P({′купите′}|не спам) = # (спам–писем без слова ’купите’ + 1) / (писем со словом ’купите’ + 2)
def p_word_is_spam(num_spam_mails_with_word, num_all_spam_mails):
    """
    Determines probability that the word is spam
    Parameters
    ----------
    num_spam_mails_with_word : int
        Number of spam emails with the word
    num_all_spam_mails : int
        Number of all spam emails with the word
    Returns
    -------
    (num_spam_mails_with_word + 1) / (num_all_spam_mails + 2) : float
        Probability that the word is spam
    """
    return (num_spam_mails_with_word + 1) / (num_all_spam_mails + 2)


# log(P(спам)) + ∑log(P(𝑤𝑘|спам)) > log(P(не спам)) + ∑log(P(𝑤𝑘|не спам))
def is_spam(words):
    """
    Determines if the given words is a spam
    Parameters
    ----------
    words : set
        Set of words from mail
    Returns
    -------
    res_p > res_q : bool
        Whether mail is spam
    """
    res_p = math.log(spam_mails / all_mails)
    res_q = math.log((all_mails - spam_mails) / all_mails)
    for word in words:
        list = dictionary.get(word)
        if list is None:
            list = [1, 1]
        res_p += math.log(p_word_is_spam(list[1], sum(list)))
        res_q += math.log(p_word_is_spam(list[0], sum(list)))
    return res_p > res_q


def learn():
    """
    Learn classificator
    """
    global spam_mails, all_mails
    with open('learnCollection.txt', 'r', encoding='utf-8') as inp_file:
        inp_data = inp_file.read()
    mails = inp_data.split('\n')
    for i in range(len(mails)):
        if mails[i] == "":
            break
        tab = mails[i].split('\t', 1)
        words = set(re.findall(r'[a-zà-ÿ0-9_&]+', tab[1].lower()))
        if tab[0] != 'ham':
            spam_mails += 1
        for word in words:
            list = dictionary.get(word)
            if list is None:
                list = [0, 0]
            if tab[0] != 'ham':
                list[1] += 1
            else:
                list[0] += 1
            dictionary.update({word: list})
    all_mails += len(mails)


def get_accuracy():
    """
    Check spam detection accuracy
    Returns
    -------
    well_amount / len(mails) : float
        Classifier accuracy
    """
    well_amount = 0
    with open('checkCollection.txt', 'r', encoding='utf-8') as inp_file:
        inp_data = inp_file.read()
    mails = inp_data.split('\n')
    for i in range(len(mails)):
        mail_is_spam(mails[i])
        tab = mails[i].split('\t', 1)
        words = set(re.findall(r'[а-яa-zà-ÿ0-9_&\']+', tab[1].lower()))
        if is_spam(words) == (tab[0] != 'ham'):
            well_amount += 1
    return well_amount / len(mails)


def mail_is_spam(mail):
    """
    Determines if the given string is a spam email
    Parameters
    ----------
    mail : str
        The text of the mail
    Returns
    -------
    is_spam(words) : bool
        The email is spam
    """
    words = set(re.findall(r'[а-яa-zÀ-ÿ0-9_&\']+', mail.lower()))
    return is_spam(words)


learn()
print(f"Точность {round(get_accuracy() * 100, 2)}%")
print(mail_is_spam("Had your contract mobile 11 Mnths? Latest Motorola, Nokia etc. all FREE! Double Mins & Text on "
                   "Orange tariffs. TEXT YES for callback, no to remove from records."))

