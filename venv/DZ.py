# ======================================= модуль ДЗ
import math
# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Факториал":
        dz1(bot, chat_id)

    elif ms_text == "Синус":
        dz2(bot, chat_id)

    elif ms_text == "Косинус":
        dz3(bot, chat_id)

    elif ms_text == "Тангенс":
        dz4(bot, chat_id)

    elif ms_text == "Возраст":
        dz5(bot, chat_id)

    elif ms_text == "Имя":
        dz6(bot, chat_id)

# -----------------------------------------------------------------------
def dz1(bot, chat_id):
    my_inputInt(bot, chat_id, "Введите число", dz1_ResponseHandler)
def dz1_ResponseHandler(bot, chat_id, number_int):
    bot.send_message(chat_id, text=f"Факториал числа {number_int}! \nБудет равен {fac(number_int)}!!!")
# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    my_inputInt(bot, chat_id, "Введите число", dz2_ResponseHandler)
def dz2_ResponseHandler(bot, chat_id, number_int):
    bot.send_message(chat_id, text=f" Cинус числа {number_int}! \nБудет равен {math.sin(number_int)}!!!")
# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    my_inputInt(bot, chat_id, "Введите число", dz3_ResponseHandler)
def dz3_ResponseHandler(bot, chat_id, number_int):
    bot.send_message(chat_id, text=f" Косинус числа {number_int}! \nБудет равен {math.cos(number_int)}!!!")
# -----------------------------------------------------------------------
def dz4(bot, chat_id):
    my_inputInt(bot, chat_id, "Введите число", dz4_ResponseHandler)
def dz4_ResponseHandler(bot, chat_id, number_int):
    bot.send_message(chat_id, text=f" Тангенс числа {number_int}! \nБудет равен {math.tan(number_int)}!!!")
# -----------------------------------------------------------------------
def dz5(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)

def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id, text=f"О! тебе уже {age_int}! \nА через год будет уже {age_int+1}!!!")
# -----------------------------------------------------------------------
def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id, f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)
# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):

    # bot.send_message(chat_id, text=botGames.GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,

def fac(n):
    if n == 0:
        return 1
    return fac(n-1) * n
def primer(n):
    a=random.randint(1,1000)
    b=random.randint(1,1000)
    return a+b
