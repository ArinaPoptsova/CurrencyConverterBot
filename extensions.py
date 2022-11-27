import requests
import json
from config import keys


class APIException(Exception):
    def __init__(self, message='APIException'):
        self.message = message

    def __str__(self):
        return self.message


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote not in keys:
            raise APIException(f'Неверное имя валюты: {quote}')

        if base not in keys:
            raise APIException(f'Неверное имя валюты: {base}')

        if quote == base:
            raise APIException('Нельзя конвертировать одинаковые валюты')

        if ',' in amount:
            raise APIException('Пожалуйста, используйте точку для записи дробного числового значения')

        if len(amount) > 15:
            raise APIException('Слишком длинное число')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Пожалуйста, введите числовое значение в качестве 3-го параметра')

        quote_ticker, base_ticker = keys[quote], keys[base]

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=f8e578eb5bb2525a289c6b65c3f96b95')
        total_base = float(json.loads(r.content)['data'][f'{quote_ticker}{base_ticker}']) * amount

        return round(total_base, 2)
