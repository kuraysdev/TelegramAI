import telebot;
from telebot import types;
import threading;
from aitextgen import aitextgen;
from functions import *;
from config import TOKEN;
import psutil;
import os;
pid = os.getpid()
py = psutil.Process(pid)

queue = []

ai = aitextgen(model_folder="model")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Поддержать", callback_data="support"))
    bot.send_message(id, "Привет! \nЯ бот который с помощью нейросети генерирует анекдоты. Пиши \"Давай анек\". \n Поддержать бота: https://donationalerts.com/r/kurays", reply_markup=markup)


@bot.message_handler(commands=['go'])
def go(message):
    id = message.chat.id
    if queue.count(id) > 0:
            bot.send_message(id, "Спокойно спокойно жди когда догенерю!")
            return
        
    bot.send_message(id, "Генерю нейроанекдот")
    to_queue(queue, id)
    if check_queue(queue, id): bot.send_message(id, "Ваша позиция в очереди " + get_index(queue, id))
    threading.Thread(target = start_waiting, args = [bot, queue, ai, id]).start()
    

@bot.message_handler(commands=['queue'])
def check(message):
    id = message.chat.id
    if queue.count(id) == 0:
        bot.send_message(id, "Вас нет в очереди")
        return
    bot.send_message(id, "Ваша позиция в очереди " + get_index(queue, id))


@bot.message_handler(commands=['stat'])
def stats(message):
    id = message.chat.id
    bot.send_message(id, 
    "RAM USAGE BY BOT: {} GB".format(round(py.memory_info()[0]/2.**30),2) + "\n" +
    "RAM: {0}/{1} GB".format(round(psutil.virtual_memory().used/1024/1024/1024),round(psutil.virtual_memory().total/1024/1024/1024)) + "\n" +
    "CPU LOAD: {}%".format(psutil.cpu_percent(interval=0.5)) + "\n" +
    "QUEUE: {}".format(len(queue))
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Пока это не записываем к сожалению")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Пока это не записываем к сожалению")
    elif call.data == "cb_next":
        id = call.message.chat.id 
        if queue.count(id) > 0:
            bot.send_message(id, "Спокойно спокойно жди когда догенерю!")
            return
        bot.send_message(id, "Идем делать следующий :)")
        to_queue(queue, id)
        if check_queue(queue, id): bot.send_message(id, "Ваша позиция в очереди " + get_index(queue, id))
        threading.Thread(target = start_waiting, args = [bot, queue, ai, id]).start()



bot.polling(none_stop=True, interval=0)