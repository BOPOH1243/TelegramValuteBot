import json
import extensions
import requests
import telebot
import config
#https://www.cbr-xml-daily.ru/daily_json.js получение курса валют цб в json
TOKEN = config.BOT_TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в формате \n<знак валюты>\<в какую валюту перевести>\<количество переводимой валюты> например "USD BGN 16" \nУвидеть список всех валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные валюты'
    json_values = extensions.request_cbr_course()
    for key in json_values['Valute']:
        text='\n'.join((text, f"{json_values['Valute'][key]['Name']}, ({key})"))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.upper().split(' ')
        if len(values) != 3:
            raise extensions.ConvertionException('неверное количество параметров')
        quote, base, amount = values
        total_base = extensions.Converter.convert(quote,base,amount)
    except extensions.ConvertionException as e:
        bot.reply_to(message,f'ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
