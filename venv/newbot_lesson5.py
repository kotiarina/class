import  json
from  io import  BytesIO
import telebot
from telebot import types
import requests
import BotGames
from menuBot import Menu
import DZ
import bs4
import time

bot = telebot.TeleBot('5160152364:AAFQCGToseFHTF5wJn_t2ltokHu-Z090wf0')

game21=None
@bot.message_handler(commands="start")
def command(message,res=False):
    txt_message=f"Привет,{message.from_user.first_name}! Я тестовый бот" \
                f"для курас программирования Python"
    bot.send_message(message.chat.id,text=txt_message,
                     reply_markup=Menu.getMenu("Главное меню").markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21
    chat_id = message.chat.id
    ms_text = message.text

    result=goto_menu(chat_id,ms_text)
    if result:
        return
    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:
        if ms_text == "Помощь":
            send_help(chat_id)
        elif ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка")
        elif ms_text == "Прислать гороскоп":
            bot.send_message(chat_id, text=get_goroskop())
        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)
        elif ms_text == "Карту!":
            if game21 == None:  # если мы случайно попали в Это меню, а объекта
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))
            bot.send_message(chat_id, text=text_game)
            if game21.status != None:
                goto_menu(chat_id, "Выход")
                return
        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return
        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-4":
            DZ.dz4(bot, chat_id)

        elif ms_text == "Задание-5":
            DZ.dz5(bot, chat_id)

        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)
    else:
        bot.send_message(chat_id, text="Мне жаль,я не понимаю вашу команду:" + ms_text)
        goto_menu(chat_id, "Главное меню")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "ManOrNot_GoToSite":
        import webbrowser
        webbrowser.open("https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
        bot.answer_callback_query(call)


def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)
    if target_menu != None:
        bot.send_message(chat_id,text=target_menu.name,reply_markup=target_menu.markup)
        if target_menu.name=="Игра в 21":
            global game21
            game21=BotGames.Game21()
            text_game=game21.get_cards(2)
            bot.send_media_group(chat_id,media=getMediaCards(game21))
            bot.send_message(chat_id,text=text_game)
            return True
        if target_menu.name=="Камень,ножницы,бумага":
            global rps
            rps=BotGames.RockPaperScissors()
            text_game=rps.print_score()
            bot.send_message(chat_id,text=text_game)
            return True
        else:
            return False

def getMediaCards(game21):
    medias=[]
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias
def send_help(chat_id):
    global bot
    bot.send_message(chat_id,"Автор:Скоробогатова Екатерина под руководством Швец А.Ю.")
    markup=types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton(text="Напишите автору",url="https://t.me/Ikatirin")
    markup.add(btn1)
    img=open("1-МД-5_Скоробогатова_Екатерина.jpg","rb")
    bot.send_photo(chat_id,img,reply_markup=markup)

def get_goroskop():
    array_goroskop = []
    z = ''
    s = requests.get('https://horo.mail.ru/prediction/pisces/today/')
    soup = bs4.BeautifulSoup(s.text, "html.parser")
    result_find = soup.select('.article__text')
    for result in result_find:
        array_goroskop.append(result.getText().strip())
    return array_goroskop[0]
def get_dogURL():
    url=""
    req=requests.get('https://random.dog/woof.json')
    if req.status_code==200:
        r_json=req.json()
        url=r_json['url']
    return url
def get_ManOrNot(chat_id):
    global bot
    markup=types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton(text="Проверить",callback_data='ManOrNot_GoToSite')
    markup.add(btn1)
    req=requests.get("https://thispersondoesnotexist.com/image",allow_redirects=True)
    if req.status_code==200:
        img=BytesIO(req.content)
        bot.send_photo(chat_id,photo=img,reply_markup=markup,caption="Этот человек реален?")
bot.polling(none_stop=True,interval=0)
print()





