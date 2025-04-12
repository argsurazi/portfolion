import os
import random
import time
from _datetime import datetime
import telebot
from pytubefix import YouTube
from pytubefix.cli import on_progress

bot = telebot.TeleBot('Your_token') #use a token from BotFather

@bot.message_handler(commands=['start']) #start bot
def starting(message):
    timestamp = datetime.now()
    timestamp = timestamp.strftime('%d.%m.%Y %H:%M')
    userinfo = [message.chat.first_name, message.chat.last_name, message.chat.username, message.chat.id, timestamp] #for knowing who used service
    with open('userinfo', 'a', encoding='utf-8') as file:
        file.write(f'{userinfo}\n')
    start_message = bot.send_message(message.chat.id, 'For download video send me url like "https://youtu.be/5e6JkYzYHxY?si=pSzHkhZOVedDSD36" \nAND no longer that +-20 pls tnx \n</b>If you using me, I collect your data like id, name ect</b>')
    bot.register_next_step_handler(start_message, returning) #after this bot wait message with Youtube url
@bot.message_handler()
def returning(message):
    bot.send_message(message.chat.id,'Just a minute...') #downloading starts

    try:
        url = message.text
        video = YouTube(
            proxies={"http": "your port", #your proxy if you are in Russia
                     "https": "your port"},
            url=url,
            on_progress_callback=on_progress,
        )
        default_name = video.title #saving of original title for user
        print('Title:', video.title)
        video.title = str(random.randint(1,100) + random.randint(1,100) + random.randint(1,100)) #change videos title for excepting any errors with titles

        stream = video.streams.get_lowest_resolution() #cose bots can use only 50 mb data for one request, use low quality, but you can change it
        stream.download()
        time.sleep(20)
        with open(f'{video.title}.mp4', 'rb') as video_file: #saving video
            bot.send_video(
                chat_id=message.chat.id,
                video=video_file,
                supports_streaming=True
            )
        bot.send_message(message.chat.id, default_name) #sending video
        time.sleep(10) #for 100% result
        os.remove(f'{video.title}.mp4') #removing video from your server

    except Exception as e: #if someone gone wrong
        bot.send_message(message.chat.id, f'maybe it is SO long(>50mb)')
        os.remove(f'{video.title}.mp4') #removing
        print(e) #errors name
bot.polling(non_stop=True)

