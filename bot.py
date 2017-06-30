import telebot
import os
from random import randint

f = open("bot.py", "r") 
src = f.read()

bot = telebot.TeleBot(os.environ['PP_BOT_TOKEN'])

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == '/roll':
        bot.send_message(message.chat.id, str(randint(1, 6)))
    elif message.text == '/src':
        bot.send_message(message.chat.id, src)
        
if __name__ == '__main__':
     bot.polling(none_stop=True)