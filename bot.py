import os

from flask import Flask, request

import dices
import magic
# import rm
import telebot
from random import randint

import requests

TOKEN = os.environ['PP_BOT_TOKEN']
URL = os.environ['PP_BOT_URL']
REPO = os.environ['PP_BOT_REPO']
SECRET = '/' + TOKEN


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Cheer, ' + message.from_user.first_name)
    bot.send_message(message.chat.id, message.from_user.id)
    
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

@bot.message_handler(commands=['magic'])
def roll(message):
    msg = message.text.replace('/magic','').lstrip(' ')
    botAns = magic.magicBall[randint(0, len(magic.magicBall) - 1)]
    botMsg = botAns
    if msg != "":
        botMsg = "\"" + msg + "\": " + botAns
    bot.send_message(message.chat.id, botMsg)

@bot.message_handler(commands=['chatID'])
def roll(message):  
    bot.send_message(message.chat.id,  str(message.chat.id))

@bot.message_handler(commands=['sendMessage'])
def roll(message):  
    msgSplit = message.text.replace('/sendMessage','').lstrip(' ').lsplit(" ", 1)
    bot.send_message(message.chat.id, len(msgSplit))
    if len(msgSplit) == 2:
        chatId = msgSplit[0]
        msg = msgSplit[1]
        bot.send_message(message.chat.id, chatId)
        bot.send_message(message.chat.id, msg)
        bot.send_message(chatId, msg)
    else:
        bot.send_message(message.chat.id,"ERROR")                

@bot.message_handler(commands=['src'])
def src(message):
    bot.send_message(message.chat.id, REPO)
        
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
