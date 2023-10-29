import requests
from config import currency, API_KEY


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, target, amount):
        if base == target:
            raise APIException('При переводе необходимо указывать разные валюты')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Данная валюта не поддерживается: {base}')

        try:
            target_ticker = currency[target]
        except KeyError:
            raise APIException(f'Данная валюта не поддерживается: {target}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Недопустимое количество: {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_ticker}/{target_ticker}/{amount}')
        last_updated = r.json()['time_last_update_utc']
        result = r.json()['conversion_result']
        return result, last_updated
