from typing import Dict

from inline.data import INLINE_DATA


class Searcher:
    data: Dict[str, str]

    def __init__(self):
        self.data = INLINE_DATA
        self.names = list(self.data)

    def parse_query(self, text: str) -> list:
        val = text.upper().strip()
        # TODO: нечёткий поиск
        return [name for name in self.names if val in name]

    def get_answer(self, title):
        answer = self.data[title]
        return answer



