# -*- coding: utf-8 -*-
from django.contrib import admin
import telebot
from telebot import types
import tg_analytic
from telebot.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db import *
import time


TOKEN = "TG_TOKEN"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

admins = [361637610] # id of admin

media_path = "../filmsBot/media/"
code = "🔐 Код 🔐"
random = "🔀 Рандом 🔀"
recommendation = "📌 Рекомендации 📌"
search = "🔎 Поиск 🔍"
welcome = ". Я помогу тебе выбрать фильм на вечер. Если тебе понравился фильм с нашего __TikTok__ то нажми на кнопку *" + code + "* и введи его из описания тиктока. Если ты просто не знаешь что посмотреть нажми *" + random + "* и я предложу тебе случайный фильм для просмотра или нажми на *" + recommendation +"* и я подберу тебе фильм по жарну или ищи любимый фильм по названию нажав на кнопку *" + search + "*. Если нужна помощь введи /help."
help = "Если тебе понравился фильм с нашего __Tiktok__ то нажми на кнопку *" + code + "* и введи его из описания TikTok-a. Если ты просто не знаешь что посмотреть нажми *" + random + "* и я предложу тебе случайный фильм для просмотра или нажми на *" + recommendation +"* и я подберу тебе фильм по жарну или ищи любимый фильм по названию нажав на кнопку *" + search + "*."


def gen_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.row_width = 1
    markup.add(KeyboardButton(code),
    KeyboardButton(random),
    KeyboardButton(recommendation),
    KeyboardButton(search))
    return markup


def gen_link(link):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Смотреть фильм 🎥", url=link))
    return markup


def gen_link_ad(link):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🔗 Ссылка 🔗", url=link))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    tg_analytic.statistics(message.chat.id, message.text)
    name = message.from_user.first_name
    initiate_user_start(message.from_user, message.chat.id)
    photo = open('how_to.png', 'rb')
    bot.send_photo(message.chat.id, photo, "Привет, " + name + welcome, parse_mode='Markdown', reply_markup=gen_markup())
    photo.close()


@bot.message_handler(commands=['help'])
def send_help(message):
    tg_analytic.statistics(message.chat.id, message.text)
    update_last_day_active(message.from_user.id, message.chat.id)
    photo = open('how_to.png', 'rb')
    bot.send_photo(message.chat.id, photo, help, parse_mode='Markdown', reply_markup=gen_markup())
    photo.close()


@bot.message_handler(commands=['send_ad'])
def newsletter(message):
    if message.from_user.id in admins:
        users = get_all_users()
        count = 0
        for i, user in enumerate(users):
            try:
                send_newsletter_ad(user[0])
                count += 1
            except Exception as e:
                bot.send_message(message.from_user.id, "Не смог отправить сообщение юзеру " + str(user[0]))
                print(e)
            if i % 20 == 0:
                time.sleep(1)
        bot.send_message(message.from_user.id, "Закончил рассылку на " + str(count) + " пользователей!")


@bot.message_handler(commands=['send_mess'])
def send_mess(message):
    if message.from_user.id in admins:
        s = message.text.split(' ')
        text = ''
        sent = False
        for i in range(2, len(s)):
            text += s[i] + ' '
        try:
            bot.send_message(int(s[1]), text, parse_mode='Markdown', reply_markup=gen_markup())
            sent = True
        except Exception as e:
            bot.send_message(message.from_user.id, "Не смог отправить сообщение")
        if sent:
            bot.send_message(message.from_user.id, "Отправлено сообщение " + text)


@bot.message_handler(func=lambda m:True)
def main_menu(message):
    tg_analytic.statistics(message.chat.id, message.text)
    update_last_day_active(message.from_user.id, message.chat.id)
    if message.text[:10] == 'статистика' or message.text[:10] == 'Cтатистика':
        st = message.text.split(' ')
        if 'txt' in st or 'тхт' in st:
            tg_analytic.analysis(st,message.chat.id)
            with open('%s.txt' %message.chat.id ,'r',encoding='UTF-8') as file:
                bot.send_document(message.chat.id,file)
                tg_analytic.remove(message.chat.id)
        else:
            messages = tg_analytic.analysis(st,message.chat.id)
            bot.send_message(message.chat.id, messages)
    elif message.text.isdigit():
        info = None
        if message.text.isdigit():
            info = get_film_by_code_from_db(int(message.text))
        send_film(message, info)
    elif message.text[:3] == "Код" or message.text[:3] == "код":
        text = message.text.split(' ')
        if len(text) > 1:
            if text[1].isdigit():
                info = None
                info = get_film_by_code_from_db(int(text[1]))
                send_film(message, info)
        else:
            bot.send_message(message.chat.id, "Нажми кнопку код и потом отправь мне его!")
    elif message.text == code:
        msg = bot.send_message(message.chat.id, "Отправь код фильма увиденного в TikTok.", reply_markup=gen_markup())
        bot.register_next_step_handler(msg, find_film_by_code)
    elif message.text == random:
        bot.send_message(message.chat.id, "Сейчас выберу тебе фильм.")
        info = get_random_film_from_db()
        send_film(message, info)
    elif message.text == recommendation:
        genre_markup = ReplyKeyboardMarkup()
        genre_markup.row_width = 1
        genres = get_all_genres()
        for gen in genres:
            genre_markup.add(gen[1])
        msg = bot.send_message(message.chat.id, "Выбери жанр из списка", reply_markup=genre_markup)
        bot.register_next_step_handler(msg, find_film_by_genre)
    elif message.text == search:
        msg = bot.send_message(message.chat.id, "Отправь название фильма")
        bot.register_next_step_handler(msg, search_film_by_name)
    else:
        bot.send_message(message.chat.id, "Не знаю такую команду!", reply_markup=gen_markup())


def find_film_by_code(message):
    info = None
    tg_analytic.statistics(message.chat.id, message.text)
    if message.text.isdigit():
        info = get_film_by_code_from_db(int(message.text))
    send_film(message, info)
    

def find_film_by_genre(message):
    tg_analytic.statistics(message.chat.id, message.text)
    info = get_random_film_by_genre_from_db(message.text)
    send_film(message, info)


def search_film_by_name(message):
    tg_analytic.statistics(message.chat.id, message.text)
    info = get_film_by_name(message.text)
    send_list_of_films(message, info)


def send_ad(id):
    info = get_random_ad_from_db()
    if info != None:
        text = '*'+info[1]+'*\n'+info[2]
        if info[5] != '':
            video = open(media_path+info[5], 'rb')
            bot.send_video(id, video)
            bot.send_message(id, text, parse_mode='Markdown', reply_markup=gen_link_ad(info[3]))
            video.close()
        else:
            photo = open(media_path+info[4], 'rb')
            bot.send_photo(id, photo, text, parse_mode='Markdown', reply_markup=gen_link_ad(info[3]))
            photo.close()


def send_newsletter_ad(id):
    info = get_last_ad_from_db()
    if info != None:
        text = '*'+info[1]+'*\n'+info[2]
        if info[5] != '':
            video = open(media_path+info[5], 'rb')
            bot.send_video(id, video)
            bot.send_message(id, text, parse_mode='Markdown', reply_markup=gen_link_ad(info[3]))
            video.close()
        else:
            photo = open(media_path+info[4], 'rb')
            bot.send_photo(id, photo, text, parse_mode='Markdown', reply_markup=gen_link_ad(info[3]))
            photo.close()


def send_list_of_films(message, info):
    if info == [] or info == None:
        bot.send_message(message.chat.id, "У меня нет такого фильма. Прости 😔")
    else:
        text_message = ''
        for el in info:
            text_message += "*" + el[1] + "* (" + str(el[3]) + ')' + " - 🔐 Код 🔐 - *" + str(el[0]) + "*\n"
        text_message += "\nЧтобы посмотреть нужный фильм нажми *Код* и введи тот что после названия фильма."
        bot.send_message(message.chat.id, text_message, parse_mode='Markdown', reply_markup=gen_markup())


def send_film(message, info):
    if info == None or info == []:
        bot.send_message(message.chat.id, "У меня нет такого фильма. Прости 😔", reply_markup=gen_markup())
    else:
        send_ad(message.chat.id)
        photo = open(media_path+info[7], 'rb')
        text_message = '*' + info[1] + '*' + "\n" + "📈 *Рэйтинг*: " + str(info[6]) + "\n🗓 *Год*: " + str(info[3]) + "\n" + info[2]
        bot.send_photo(message.chat.id, photo, text_message, parse_mode='Markdown', reply_markup=gen_link(info[5]))
        photo.close()
        if info[4] != '':
            bot.send_message(message.chat.id, "Если хочешь посмортеть трэйллер, то вот ссылка: " + info[4])
        bot.send_message(message.chat.id, "Могу ещё чем-то помочь?", reply_markup=gen_markup())


if __name__ == '__main__':
    bot.infinity_polling()
