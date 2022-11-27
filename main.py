import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы узнать курс интересующей Вас валюты, пожалуйста, введит команду следующего формата: \n' \
           '<имя валюты> ' \
           '<валюта, в которую переводим> ' \
           '<количество первой валюты> \n' \
           'Список всех доступных валют: /values \n' \
           'Для записи дробного числового значения используем точку'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        vals = message.text.split(' ')

        if len(vals) != 3:
            raise APIException('Некорректный формат ввода')

        quote, base, amount = vals

        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: {e}')
    else:
        amount = float(amount)
        text = f'{"{:,.2f}".format(amount)} {keys[quote]} = {"{:,.2f}".format(total_base)} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()

# 0gdYmwHrQFNVnzL5bI1nOgdhPGQ01NGN
