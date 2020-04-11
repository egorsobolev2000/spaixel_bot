import re
from typing import Dict

from inline.data import INLINE_DATA
from inline.stopwords import STOP_LIST


class Searcher:
    """ Класс умного поиска по запросу """
    data: Dict[str, str]

    def __init__(self):
        self.data = INLINE_DATA
        self.titles = list(self.data)

    @staticmethod
    def __clear_text_func__(text):
        """ Предварительная очистка текста от стоп-слов """
        text_to_terms = {}

        for w in text:
            # Разбиение слов
            word_re = re.compile(r'[\W_]+')
            # Очистка от мусора
            symbols_re = re.compile(r'[<.*?>]|[</a-z>]|\d+|[#%!@*\"\':;=+\-()*?%$#@!]')
            text_to_terms[text] = text.lower()
            text_to_terms[text] = word_re.sub(' ', text_to_terms[text])
            text_to_terms[text] = symbols_re.sub('', text_to_terms[text])
            re.sub(r'[\W_]+', '', text_to_terms[text])
            text_to_terms[text] = text_to_terms[text].split()
            # Очитска от стоп-слов
            text_to_terms[text] = [w for w in text_to_terms[text] if w not in STOP_LIST]

        return text_to_terms

    @staticmethod
    def __index_one_file__(termlist):
        """ Подготовка к индексации и индексация ключевых слов """
        file_index = {}
        for index, word in enumerate(termlist):
            if word in file_index.keys():
                file_index[word].append(index)
            else:
                file_index[word] = [index]
        return file_index

    def __make_indices__(self, termlists):
        """ Индексация всех полученных полезных слов """
        total = {}
        for filename in termlists.keys():
            total[filename] = self.__index_one_file__(termlists[filename])
        return total

    def __create_new_dict__(self, old_dict):
        """ Непосредственное создание индексированного набора данных
        с приминением функций фильтрации """
        NEW_INLINE_DATA = {}
        for k, v in old_dict.items():
            """ 1. Беру k-ключ и v-значение
                2. Записую в новый словарь: {
                    k-старый ключ: 
                    (вызываю функцию разбиения и очистки текста
                    (передаю[старый словать][текущий ключ]))[запрашиваю значение из полученного словаря]
                    }
            """
            NEW_INLINE_DATA.update({k: (self.__clear_text_func__(old_dict[k]))[v]})
        return NEW_INLINE_DATA

    @staticmethod
    def __get_potential_options__(di, regex):
        """ Прогон по индексированному словарю с
        поиском савпадения условий поиска """
        potential_options = []
        for k in list(di):
            for v in di[k]:
                if re.findall(regex.lower(), v) and k not in potential_options:
                    potential_options.append(k)
                    from colors import ColorsPrint
                    # print(ColorsPrint(f'KEY -- {k}', 'inf').do_colored())
                    # print(ColorsPrint(f'VALUE -- {v}', 'inf').do_colored())
        return potential_options

    def parse_query(self, val) -> object:
        """ Получение пользовательского ввода и
        оттдача потенциально возможных вариатов
        ответа на клиентский запрос"""
        cnd = self.__create_new_dict__(INLINE_DATA) # создаю очищ. набор данных
        NEW_DICT = self.__make_indices__(cnd) # индексирую очищ. набор
        return [title for title in self.__get_potential_options__(NEW_DICT, val)]

    def get_answer(self, title):
        """ Получаю пользовательский выбор и отдаю значение
        соответствующие этому запросу/ключу """
        answer = self.data[title]
        return answer

