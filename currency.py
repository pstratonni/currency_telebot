import telebot

from config import TOKEN, currencies
from extensions import APIEception, CurrencyConvert

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helps(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список доступных валют:/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in currencies.keys():
        text += f'\n{key}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    value = message.text.split()
    try:
        if len(value) > 3:
            raise APIEception('Слишком много параментров')
        elif len(value) < 3:
            raise APIEception('Слишком мало параметров')
        quote, base, quantity = value
        response, quantity = CurrencyConvert.get_price(quote, base, quantity)
    except APIEception as e:
        bot.reply_to(message,f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message,f'Неудалось обработать команду\n{e}')
    else:
        price = response[currencies[base]]/response[currencies[quote]] * quantity
        text = f'Цена {quantity} {quote} в {base} - {price}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
