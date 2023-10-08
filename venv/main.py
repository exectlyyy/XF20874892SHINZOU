import telebot
import os

from random import choice
from telebot import types

bot = telebot.TeleBot('6629693845:AAEenGeuPtat7ERXlEVFHE_sS7BRXHT27y0')


def udarenie(slovo):
    var = []
    slovo = [i for i in slovo]
    for i in range(len(slovo)):
        if slovo[i] in 'уеэоаыяию':
            new = [j for j in slovo]
            new[i] = slovo[i].upper() 
            var.append(''.join(new))
    return var

@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.from_user.id, 'Привет')


user_data = []
actual_word = ''

@bot.message_handler(commands=['go'])
def test(message):
    global actual_word
    with open(r'Data/u.txt') as f:
        l = f.readlines()
        l = [i[:-1] for i in l]
        a = choice(l)
        print(udarenie(a.lower()))
        markup = types.ReplyKeyboardMarkup()
        var = udarenie(a.lower())
        actual_word = a
        for i in var:
            markup.add(i)
        bot.send_message(message.from_user.id, a.lower(), reply_markup=markup)
        markup = types.ReplyKeyboardRemove(selective=False)
        var = []


@bot.message_handler(content_types=['text'])
def main(message):
    global actual_word, user_data
    file = f'''{message.from_user.id}.txt'''
    folder = '/Users/ivanyburov/Documents/GitHub/XF20874892SHINZOU/User_Data'
    path = os.path.join(folder, file)
    if not os.path.isfile(path):
        file = open('/Users/ivanyburov/Documents/GitHub/XF20874892SHINZOU/User_Data/file.txt', 'x')
        file.close()
        os.rename('/Users/ivanyburov/Documents/GitHub/XF20874892SHINZOU/User_Data/file.txt',
                  f'''/Users/ivanyburov/Documents/GitHub/XF20874892SHINZOU/User_Data/{message.from_user.id}''')
    if message.from_user.id not in user_data:
        user_data.append(message.from_user.id)
        bot.send_message(message.from_user.id, 'Стартуем') #Дописать что бы кнопка на старт была    
    else:
        if message.text == actual_word:
            bot.send_message(message.from_user.id, 'верно')
        else:
            bot.send_message(message.from_user.id, 'ты даун')
    print(user_data)
    
bot.infinity_polling(1080)
