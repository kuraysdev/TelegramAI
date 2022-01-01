import time;
from telebot import types;

def to_queue(queue, id):
    queue.append(id)



def check_queue(queue, id):
    if queue == [id]: return False
    else: return True

def get_index(queue, id):
    return str(queue.index(id)+1)


def start_waiting(bot, queue, ai, chid): 
    while True:
        if queue[0] != chid: 
            time.sleep(1)
            print("Waiting...")
            continue
        id = queue[0]
        start = time.time()
        print("Genering...")
        text = ai.generate_one(min_length=128)
        print("Generated!")
        end = time.time()
        ping = round(end - start)
        pingstr = str(ping)
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(types.InlineKeyboardButton("🎰 Крутой анек", callback_data="cb_yes"),
                        types.InlineKeyboardButton("🤝 Плохой анек", callback_data="cb_no"),
                        types.InlineKeyboardButton("🤝 Давай новый", callback_data="cb_next"))
        bot.send_message(id, text + "\n\n" + "Время гена: " + pingstr  + " сек.", reply_markup=markup)
        queue.pop(0)
        break