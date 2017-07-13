import os
from flask import Flask, request

import dices
import telebot
from random import randint

TOKEN = os.environ['PP_BOT_TOKEN']
URL = os.environ['PP_BOT_URL']
REPO = os.environ['PP_BOT_REPO']
SECRET = '/' + TOKEN


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Cheer, ' + message.from_user.first_name)
    
@bot.message_handler(commands=['roll'])
def roll(message):
    bot.send_message(message.chat.id, str(randint(1, 6)))
    
@bot.message_handler(commands=['rolldice'])
def rolldice(message):
    rand_val = randint(1, 6)
    dise_text = dices.dice_lib[rand_val]
    bot.send_message(message.chat.id, dise_text)
    
@bot.message_handler(commands=['rollsticker'])
def rollsticker(message):
    rand_val = randint(1, 6)
    sticker_id = dices.dice_id_lib[rand_val]
    bot.send_sticker(message.chat.id, sticker_id)
    
@bot.message_handler(commands=['src'])
def src(message):
    bot.send_message(message.chat.id, REPO)
    
#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message):
#    if message.text == '/src':
#        bot.send_message(message.chat.id, src)
        
@server.route(SECRET, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200
       
@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=URL+SECRET)
    return "CONNECTED", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))       
