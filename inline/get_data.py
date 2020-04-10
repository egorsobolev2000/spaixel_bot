import re
from contextlib import contextmanager

from inline.data import INLINE_DATA


@contextmanager
def managed_file(name):
    try:
        f = open(name, 'r')
        yield f

    finally:
        f.close()


def clear_text_func(text):
    text_to_terms = {}

    # Получаю список стоп-слов
    with managed_file('stopwords.txt') as f:
        stopwords = f.read().splitlines()

    for w in text:
        word_re = re.compile(r'[\W_]+')
        symbols_re = re.compile(r'[<.*?>]|[</a-z>]|\d+|[#%!@*\"\':;=+\-()*?%$#@!]')
        text_to_terms[text] = text.lower()
        text_to_terms[text] = word_re.sub(' ', text_to_terms[text])
        text_to_terms[text] = symbols_re.sub('', text_to_terms[text])
        re.sub(r'[\W_]+', '', text_to_terms[text])
        text_to_terms[text] = text_to_terms[text].split()

        text_to_terms[text] = [w for w in text_to_terms[text] if w not in stopwords]

    return text_to_terms


def index_one_file(termlist):
    file_index = {}
    for index, word in enumerate(termlist):
        if word in file_index.keys():
            file_index[word].append(index)
        else:
            file_index[word] = [index]
    return file_index


def make_indices(termlists):
    total = {}
    for filename in termlists.keys():
        total[filename] = index_one_file(termlists[filename])
    return total


NEW_INLINE_DATA = {}

# Прогоняю весь словарь данных через цикл фильтрации текста
for k, v in INLINE_DATA.items():
    """ 1. Беру k-ключ и v-значение
        2. Записую в новый словарь: {
            k-старый ключ: 
            (вызываю функцию разбиения и очистки текста
            (передаю[старый словать][текущий ключ]))[запрашиваю значение из полученного словаря]
            }
            """
    NEW_INLINE_DATA.update({k: (clear_text_func(INLINE_DATA[k]))[v]})


print(make_indices(NEW_INLINE_DATA))