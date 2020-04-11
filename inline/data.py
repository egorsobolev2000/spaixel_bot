import re
from contextlib import contextmanager
from typing import List, Any, Union

INLINE_DATA = {

    'Отзывы': 'Наши <a href="https://vk.com/topic-157919190_41216100">'
              '<em><b>Отзывы</b></em></a>',

    'Портфолио': 'С портфолио и последними работами можно ознакомиться '
                 'здесь -> <a href="https://spaixel.com/portfolio">'
                 '<em><b>Портфолио</b></em></a>',

    'Стоимость': "Стоимость разработки сайта зависит от предоставляемых сроков, "
                 "уникальности дизайна и сложности необходимого функционала. "
                 "Минимальная цена за сайт 7000₽ и выше.",

    'Сроки': "Сроки разработки будут зависеть от требуемого функционала, "
             "сложности дизайна и загруженности разработчиков. "
             "В среднем, разработка занимает от 5 дней.",

    'Есть дизайн?': "Да, при условии, что Вы имеете все исходники макета "
              "(<em><b>ОБЯЗАТЕЛЬНО</b></em> либо в Figma либо в PSD), так же дизайн должен "
              "соответствоhonвать современным тенденциям и логически верен. "
              "В этом случае мы с радостью реализуем Ваш дизайн!",

    'Правки': "Без дополнительной оплаты могут быть внесены 5-10 изменений "
              "которые не затрагивают функциональную часть и не требуют более "
              "3 часов на реализацию одного изменения, а так же только то что "
              "было оговорено в рамках технического задания.",
}


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
    stopwords = STOP_LIST

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


def create_new_dict(old_dict):
    NEW_INLINE_DATA = {}
    # Прогоняю весь словарь данных через цикл фильтрации текста
    for k, v in old_dict.items():
        """ 1. Беру k-ключ и v-значение
            2. Записую в новый словарь: {
                k-старый ключ: 
                (вызываю функцию разбиения и очистки текста
                (передаю[старый словать][текущий ключ]))[запрашиваю значение из полученного словаря]
                }
                """
        NEW_INLINE_DATA.update({k: (clear_text_func(old_dict[k]))[v]})
    return NEW_INLINE_DATA


def get_potential_options(di, regex):
    potential_options = []
    for k in list(di):
        for v in di[k]:
            if re.findall(regex.lower(), v) and k not in potential_options:
                potential_options.append(k)
                print(f'KEY -- {k}')
                print(f'VALUE -- {v}')
    return potential_options


#cnd = create_new_dict(INLINE_DATA)
#NEW_DICT = make_indices(cnd)
#t = get_potential_options(NEW_DICT, 'от')
#for _ in t:
#    print(_)















