import os

from flask import Flask, request

import dices
import magic
# import rm
import telebot
import giphypop
from random import randint
import search_google.api

import requests

TOKEN = os.environ['PP_BOT_TOKEN']
URL = os.environ['PP_BOT_URL']
REPO = os.environ['PP_BOT_REPO']
SECRET = '/' + TOKEN
SEACHID = os.environ['PP_BOT_SEARCH_ID']
SEARCHAPI = os.environ['PP_BOT_SEARCH_API_KEY']

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
def magic(message):
    msg = message.text.replace('/magic','').lstrip(' ')
    botAns = magic.magicBall[randint(0, len(magic.magicBall) - 1)]
    botMsg = botAns
    if msg != "":
        botMsg = "\"" + msg + "\": " + botAns
    bot.send_message(message.chat.id, botMsg)

@bot.message_handler(commands=['chatID'])
def chatID(message):  
    bot.send_message(message.chat.id,  str(message.chat.id))

@bot.message_handler(commands=['botMessage'])
def botMessage(message):  
    msgSplit = message.text.replace('/botMessage','').lstrip(' ').split(" ", 1)
    if len(msgSplit) == 2:
        chatId = msgSplit[0]
        msg = msgSplit[1]
        bot.send_message(chatId, msg)
    else:
        bot.send_message(message.chat.id,"ERROR")    

@bot.message_handler(commands=['gif'])
def rGif(message):  
    msg = message.text.replace('/gif','').lstrip(' ')
    if msg != "":
        g = giphypop.Giphy()
        gr = g.screensaver(msg)
        bot.send_message(message.chat.id, str(gr.url))   

@bot.message_handler(commands=['test'])
def test(message):  
    buildargs = {
        'serviceName': 'customsearch',                        
        'version': 'v1',                                 
        'developerKey': SEARCHAPI        
    }

    # Define cseargs for search
    cseargs = {
        'searchType': 'image',
        'q': 'cat',
        'cx': SEACHID,
        'num': 3
    }

    results = search_google.api.results(buildargs, cseargs)
    bot.send_message(message.chat.id, results.links[0]) 

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
