import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
import urllib3
import time

# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")

    elif ms_text == "Прислать цитату":
        bot.send_message(chat_id,text=get_quote())
    elif ms_text == "Прислать гороскоп":
        bot.send_message(chat_id,text=get_goroskop())

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Прислать фильм":
        send_film(bot, chat_id)

    elif ms_text == "Угадай кто?":
        get_ManOrNot(bot, chat_id)

    elif ms_text == "Прислать курсы":
        bot.send_message(chat_id, text=get_cur())
    elif ms_text=="Прислать карту звёздного неба":
        bot.send_photo(chat_id,photo=get_nasa(),caption="Вот тебе звёздочки")

    elif ms_text=='МКС online':
        bot.send_message(chat_id,text=get_mks())



# -----------------------------------------------------------------------
def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# ----------------------------------------------------------------------

def get_goroskop():
    array_goroskop = []
    z = ''
    s = requests.get('https://horo.mail.ru')
    soup = bs4.BeautifulSoup(s.text, "html.parser")
    result_find = soup.select('.article__text')
    for result in result_find:
        array_goroskop.append(result.getText().strip())
    return array_goroskop[0]


# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""



# -----------------------------------------------------------------------
def get_quote():
    array_quote = []
    z = ''
    s = requests.get('https://citaty.info/random')
    soup = bs4.BeautifulSoup(s.text, "html.parser")
    result_find = soup.select('.field-items')
    for result in result_find:
        array_quote.append(result.getText().strip())
    return array_quote[0]
# -----------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def get_cur_pairs():
    lst_cur_pairs = []
    req_currency_list = requests.get(f'https://currate.ru/api/?get=currency_list&key={"a12d86cedf125955b1b95decccf73fa8"}')
    if req_currency_list.status_code == 200:
        currency_list_json = req_currency_list.json()
        for pairs in currency_list_json["data"]:
            if pairs[3:] == "RUB":
                lst_cur_pairs.append(pairs)
    return lst_cur_pairs


# -----------------------------------------------------------------------
def get_cur():
    txt_curses = ""
    txt_pairs = ",".join(get_cur_pairs())
    req_currency_rates = requests.get(f'https://currate.ru/api/?get=rates&pairs={txt_pairs}&key={"a12d86cedf125955b1b95decccf73fa8"}')
    if req_currency_rates.status_code == 200:
        currency_rates = req_currency_rates.json()
        for pairs, rates in currency_rates["data"].items():
            txt_curses += f"{pairs} : {rates}\n"
    else:
        txt_curses = req_currency_rates.text
    return txt_curses

# ------------------- ----------------------------------------------------
def get_nasa():
     req=requests.get('https://api.nasa.gov/planetary/apod?api_key=BVWTYELH5NTraKdLrjXJN3zB7F0oozq0MkdeM9OU')
     url=''
     r_json = req.json()
     url = r_json['url']
     return url
def get_mks():
    req = requests.get("http://api.open-notify.org/iss-now.json")
    obj = req.json()
    tim=time.ctime(int(obj['timestamp']))
    return obj['iss_position']['latitude']+'   '+ obj['iss_position']['longitude']+'   '+tim
def get_ManOrNot(bot, chat_id):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm
