import os

from currency_converter import CurrencyConverter
from telebot import TeleBot
from telebot.types import Message

from db_methods import insert, select

bot = TeleBot(os.environ.get('BOT_TOKEN'))

converter = CurrencyConverter(
    fallback_on_missing_rate=True, 
    fallback_on_wrong_date=True
)

current_message = []


@bot.message_handler(commands=['start'])
def start(message: Message):
    text = f"Hello, {message.from_user.first_name}.\n"
    text += "Enter /commands to see my possibilities"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['commands'])
def commands(message: Message):
    text = '/commands - list of commands\n'
    text += '/currencies - list of available currencies\n'
    text += '/convert - convert currencies\n'
    text += '/history - hystory of last converts'

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['currencies'])
def get_currencies(message: Message):
    text = ''

    for currency in converter.currencies:
        text += currency + '\n'

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['convert'])
def convert_from(message: Message):
    text = 'Enter amount and currency from /currencies\n(example: 56 USD)'

    bot.send_message(message.chat.id, text)


@bot.message_handler(regexp='\w+\s\w{3}')
def convert_to(message: Message):
    global current_message

    text = 'Enter currency from /currencies\n(example: USD)'

    try:
        current_message.extend(message.text.split())
    except:
        text = 'Enter the correct currency and amount separated by space\n'
        text += 'List of currensies: /currencies'

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['history'])
def history(messange: Message):
    try:
        text = ''
        rows = select(
            table='converts',
            columns='result, date_time, fk',
            user=f'{messange.from_user.username}'
        )
        for row in range(len(rows)):
            row = rows[row]
            text += str(row['result']) + ', ' + str(row['date_time']).split()[0] + '\n'
    except:
        text = 'history is empty'

    bot.send_message(messange.chat.id, text)


@bot.message_handler(regexp='\w{3}')
def calculate(message: Message):
    global current_message, converter
    current_message.append(message.text)

    result = converter.convert(
        amount=current_message[0],
        currency=current_message[1],
        new_currency=message.text
    )

    string = f"'{current_message[0]}{current_message[1].lower()} = "
    string += f"{round(result, 2)}{message.text.lower()}', 'curdate()', "
    string += f"'{message.from_user.first_name}'"

    insert(
        table='converts',
        columns='result, date_time, fk',
        values=string
    )
    try:
        if message.text:
            bot.send_message(message.chat.id, string)
            current_message.clear()
    except:
        bot.send_message(message.chat.id, 'Enter the correct currency from /currencies')


def main():
    bot.polling(
        non_stop=True,
        timeout=1440,
        long_polling_timeout=1440
    )


if __name__ == '__main__':
    main()