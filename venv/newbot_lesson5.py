# Телеграм-бот v.004

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import botGames  # бот-игры, файл botGames.py
import menuBot
from menuBot import Menu  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого урока
import fun  # развлечения
import random
bot = telebot.TeleBot('5160152364:AAFQCGToseFHTF5wJn_t2ltokHu-Z090wf0')  # Созм экземпляр бота
value=''
old_value=''
keyboard=telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton(' ',callback_data='no'),
			 telebot.types.InlineKeyboardButton('C',callback_data='C'),
			 telebot.types.InlineKeyboardButton('<=',callback_data='<='),
			 telebot.types.InlineKeyboardButton('/',callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('7',callback_data='7'),
			 telebot.types.InlineKeyboardButton('8',callback_data='8'),
			 telebot.types.InlineKeyboardButton('9',callback_data='9'),
			 telebot.types.InlineKeyboardButton('*',callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('4',callback_data='4'),
			 telebot.types.InlineKeyboardButton('5',callback_data='5'),
			 telebot.types.InlineKeyboardButton('6',callback_data='6'),
			 telebot.types.InlineKeyboardButton('-',callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton('1',callback_data='1'),
			 telebot.types.InlineKeyboardButton('2',callback_data='2'),
			 telebot.types.InlineKeyboardButton('3',callback_data='3'),
			 telebot.types.InlineKeyboardButton('+',callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton('00',callback_data='00'),
			 telebot.types.InlineKeyboardButton('0',callback_data='0'),
			 telebot.types.InlineKeyboardButton(',',callback_data='.'),
			 telebot.types.InlineKeyboardButton('=',callback_data='='))

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)

@bot.message_handler(commands=['calculater'])
def getMessage(message):
	if value == '':
		bot.send_message(message.from_user.id,'0',reply_markup=keyboard)
	else:
		bot.send_message(message.from_user.id,value,reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
        global value,old_value
        data=query.data
        if data=='no':
            pass
        elif data=='C':
            value=''
        elif data=='<=':
            if value!='':
                value=value[:len(value)-1]
        elif data=='=':
            try:
                value=str(eval(value))
            except:
                value='Error!'
        else:
            value+=data
        if (value!=old_value and value!='') or ('0'!=old_value and value==''):
            if value=='':
                bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id,text='0',reply_markup=keyboard)
                old_value='0'
            else:
                bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id,text=value,reply_markup=keyboard)
                old_value=value
        if value=='Error!':value=''
# -----------------------------------------------------------------------
# Получение стикеров от юзера
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
# Получение аудио от юзера
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)


# -----------------------------------------------------------------------
# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)


# -----------------------------------------------------------------------
# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
# Получение координат от юзера
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)

    from Weather import WeatherFromPyOWN
    pyOWN = WeatherFromPyOWN()
    bot.send_message(chat_id, pyOWN.getWeatherAtCoords(location.latitude, location.longitude))
    bot.send_message(chat_id, pyOWN.getWeatherForecastAtCoords(location.latitude, location.longitude))


# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if subMenu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=game21.mediaCards)  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            gameRPS = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры и регистрируем его
            bot.send_photo(chat_id, photo=gameRPS.url_picRules, caption=gameRPS.text_rules, parse_mode='HTML')
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        module = cur_menu.module

        if module != "":  # проверим, есть ли обработчик для этого пункта меню в другом модуле, если да - вызовем его (принцип инкапсуляции)
            exec(module + ".get_text_messages(bot, cur_user, message)")

        if ms_text == "Помощь":
            send_help(bot, chat_id)
        if ms_text=='Калькулятор':
            bot.send_message(chat_id,text='Для использования калькулятора,нажмите\n/calculater')


    else:  # ======================================= случайный текст
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать один или несколько параметров в обработчик кнопки,
    # используйте методы Menu.getExtPar() и Menu.setExtPar()
    # call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    # После обработки каждого запроса вызовете метод answer_callback_query(), чтобы Telegram понял, что запрос обработан
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "GameRPSm":
        botGames.callback_worker(bot, cur_user, cmd, par, call)  # обработчик кнопок игры находится в модули игры

# -----------------------------------------------------------------------
def send_help(bot, chat_id):
    bot.send_message(chat_id, "Автор:   Скоробогатова Екатерина")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/Ikatirin")
    markup.add(btn1)
    img = open("1-МД-5_Скоробогатова_Екатерина.jpg", 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

# ---------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)  # Запускаем бота