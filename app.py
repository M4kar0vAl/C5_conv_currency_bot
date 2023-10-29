import telebot

from config import TOKEN, currency
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def who_am_i(message: telebot.types.Message):
    text = 'Бот для перевода валют.\
    \nЧтобы перевести валюты, введите боту команду в формате (без кавычек):\
    \n"название валюты" "в какую валюту перевести" "количество".\
    \nРегистр неважен!\
    \nПример:\
    \nдоллар евро 10 или ДоЛлАр ЕвРо 10 и т.д.\
    \nУзнать валюты доступные для перевода: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def currencies(message: telebot.types.Message):
    cur_str = '\n'.join([key for key in currency])
    bot.send_message(message.chat.id, f'Доступные валюты:\n{cur_str}')


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split()
        if len(values) != 3:
            raise APIException('Необходимо ввести 3 параметра через пробел')

        base, target, amount = values

        result, last_updated = CurrencyConverter.get_price(base, target, amount)
    except APIException as e:
        bot.reply_to(message, e)
    except Exception:
        bot.reply_to(message, 'Ошибка на сервере. Пожалуйста, повторите попытку.')
    else:
        text = f'{amount} {base}({currency[base]}) => {target}({currency[target]}): {result} {currency[target]}.\
        \nАктуально на {last_updated}'
        bot.reply_to(message, text)


bot.polling()
