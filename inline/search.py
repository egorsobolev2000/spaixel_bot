class Searcher:
    def __init__(self):
        self.titles = ['235', '3546']
        self.names = ['BTC', 'LTC']

    def parse_query(self, text: str) -> list:
        val = text.upper().strip()
        # TODO: нечёткий поиск
        return [name for name in self.names if val in name]

    def get_prices(self, names):
        """ Получить список цен для запрошенных валют
         """
        print(names)
