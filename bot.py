import os
from flask import Flask, request
import telepot

try:
    from Queue import Queue
except ImportError:
    from queue import Queue
    
from random import randint

f = open("bot.py", "r") 
src = f.read()

app = Flask(__name__)
TOKEN = os.environ['PP_BOT_TOKEN']
SECRET = '/bot' + TOKEN
URL = 'https://mylittledicebot.herokuapp.com/' #  paste the url of your application

UPDATE_QUEUE = Queue()
BOT = telepot.Bot(TOKEN)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    BOT.sendMessage(chat_id, 'hello!')

BOT.message_loop({'chat': on_chat_message}, source=UPDATE_QUEUE)  # take updates from queue

@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
    UPDATE_QUEUE.put(request.data)  # pass update to bot
    return 'OK'

BOT.setWebhook() # unset if was set previously
BOT.setWebhook(URL + SECRET)