import telebot
import requests
import json
class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        request_course = request_cbr_course()['Valute']
        try:
            quote_ticker = request_course[quote]['Value']
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = request_course[base]['Value']
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'не удалось обработать количество {amount}')

        return (quote_ticker/base_ticker)*amount

def request_cbr_course():
    request = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    result = json.loads(request.content)
    result['Valute'].update({'RUB':{'Name':'Российский рубль','Value':1}})
    return result

class ConvertionException(Exception):
    pass