import telebot
from random import choice
from telebot import types


bot = telebot.TeleBot('6629693845:AAEenGeuPtat7ERXlEVFHE_sS7BRXHT27y0')
actual_users = []
user_status = {}
questions_number = {}
actual_word = {}
waiting_answer = {}
correct_answers = {}
wrong_answers = {}
wrong_words = {}


def new_user(message):
    actual_users.append(message.from_user.id)
    user_status[message.from_user.id] = 'Waiting'
    questions_number[message.from_user.id] = '0'
    actual_word[message.from_user.id] = ''
    correct_answers[message.from_user.id] = 0
    wrong_answers[message.from_user.id] = 0
    waiting_answer[message.from_user.id] = False
    wrong_words[message.from_user.id] = []
    



def udarenie(slovo):
    var = []
    slovo = [i for i in slovo]
    for i in range(len(slovo)):
        if slovo[i] in 'уеэоаыяиюё':
            new = [j for j in slovo]
            new[i] = slovo[i].upper() 
            var.append(''.join(new))
    return var

@bot.message_handler(commands=['start'])

def start(message):
    new_user(message)
    bot.send_message(message.from_user.id, 'Привет, этот бот поможет выучить ударения ЕГЭ, напиши /help для полного списка команд')
@bot.message_handler(commands=['help'])   

def help(message):
      bot.send_message(message.from_user.id, '''/go - начать тест
/theory - теория
/stop - закончить тест
/oshibki - посмотреть свои ошибки
/ogo - пройти тест по ошибкам''')





@bot.message_handler(commands=['stop'])
def stop(message):
    if user_status[message.from_user.id] == 'Doing a test':
        bot.send_message(message.from_user.id, f'''Тест окончен!
Ваш результат: {correct_answers[message.from_user.id]}/{wrong_answers[message.from_user.id] + correct_answers[message.from_user.id]}''')
    user_status[message.from_user.id] = 'Waiting'
    questions_number[message.from_user.id] = '0'
    actual_word[message.from_user.id] = ''
    waiting_answer[message.from_user.id] = False
    correct_answers[message.from_user.id] = 0
    wrong_answers[message.from_user.id] = 0
    wrong_words[message.from_user.id] = []
   
def end(message):
    user_status[message.from_user.id] = 'Waiting'
    questions_number[message.from_user.id] = '0'
    actual_word[message.from_user.id] = ''
    waiting_answer[message.from_user.id] = False
    correct_answers[message.from_user.id] = 0
    wrong_answers[message.from_user.id] = 0

@bot.message_handler(commands=['go'])
def go(message):
    global user_status
    user_status[message.from_user.id] = 'Starting a test'
    bot.send_message(message.from_user.id, 'Количество вопросов в тесте?')
    

def test(message):
    global waiting_answer, actual_word, questions_number, correct_answers, wrong_answers, wrong_words
    if waiting_answer[message.from_user.id] ==  True:
        if message.text == actual_word[message.from_user.id]:
            bot.send_message(message.from_user.id, 'Верно')
            correct_answers[message.from_user.id] += 1
        else:
            bot.send_message(message.from_user.id, 'Неверно')
            wrong_words[message.from_user.id].append(actual_word[message.from_user.id])
            wrong_answers[message.from_user.id] += 1
            print(wrong_words)
    with open(r'Data/u.txt') as file:
        list = file.readlines()
        list = [i[:-1] for i in list]
        word = choice(list)
        print(udarenie(word.lower()))
        markup = types.ReplyKeyboardMarkup()
        var = udarenie(word.lower())
        actual_word[message.from_user.id] = word
        for i in var:
            markup.add(i)
        bot.send_message(message.from_user.id, word.lower(), reply_markup=markup)
        markup = types.ReplyKeyboardRemove(selective=False)
        var = []
    if questions_number[message.from_user.id] == 0:
            waiting_answer[message.from_user.id] = False 
    else:
        waiting_answer[message.from_user.id] = True



@bot.message_handler(commands=['theory'])
def theory(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.from_user.id, f'''Теория и лайфхаки ударения ЕГЭ''', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message):
    global user_status, questions_number, actual_word, correct_answers, wrong_answers, actual_users
    if message.from_user.id in actual_users:
        if user_status[message.from_user.id] == 'Waiting':
            bot.send_message(message.from_user.id, '/help')
        elif user_status[message.from_user.id] == 'Starting a test':
            if message.text.isdigit():
                if int(message.text) > 0:
                    user_status[message.from_user.id] = 'Doing a test'
                    questions_number[message.from_user.id] = int(message.text)
                    test(message)
                else:
                    bot.send_message(message.from_user.id, 'Ведите корректное число вопросов.')
            else:
                bot.send_message(message.from_user.id, 'Ведите корректное число вопросов.')
        elif user_status[message.from_user.id] == 'Doing a test':
            questions_number[message.from_user.id] -= 1
            if questions_number[message.from_user.id] > 0 or not waiting_answer[message.from_user.id]:
                test(message)
            else:
                if waiting_answer[message.from_user.id] ==  True:
                    if message.text == actual_word[message.from_user.id]:
                        bot.send_message(message.from_user.id, 'Верно')
                        correct_answers[message.from_user.id] += 1
                else:
                    bot.send_message(message.from_user.id, 'Неверно')
                    wrong_answers[message.from_user.id] += 1
                bot.send_message(message.from_user.id, f'''Тест окончен!
    Ваш результат: {correct_answers[message.from_user.id]}/{wrong_answers[message.from_user.id] + correct_answers[message.from_user.id]}''')
                end(message)
        print(questions_number, waiting_answer)
    else:
        start(message)
        
        

    print(user_status)


bot.infinity_polling(1080)
