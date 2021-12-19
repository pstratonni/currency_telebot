import json

import requests

from config import currencies, URL, API_KEY


class APIEception(Exception):
    pass


class CurrencyConvert:
    @staticmethod
    def get_price(quote, base, quantity):
        if quote == base:
            raise APIEception("Валюты не должны совпадать")

        try:
            quantity = float(quantity)
        except ValueError:
            raise APIEception(f'Не удалось обработать колисество "{quantity}"')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIEception(f'Не удалось обработать валюту "{base}"')
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIEception(f'Не удалось обработать валюту "{quote}"')

        response = requests.get(
            f'{URL}{API_KEY}&symbols={quote_ticker},{base_ticker}')

        return json.loads(response.content)['rates'], quantity
