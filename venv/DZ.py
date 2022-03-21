def dz1(bot, chat_id):
    bot.send_message(chat_id, text='Доделать')


def dz2(bot, chat_id):
    bot.send_message(chat_id, text='Доделать')


def dz3(bot, chat_id):
    bot.send_message(chat_id, text='Доделать')


def dz4(bot, chat_id):
    bot.send_message(chat_id, text='Доделать')


def dz5(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)


def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id, text=f"О! тебе уже {age_int}!\nА через год будет уже {age_int + 1}!!!")


def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id,
                                                           f"Добро Пожаловать {message.text}! У тебя очень красивое имя,в нем {len(message.text)}букв!")
    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)


def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)


def my_inputInt(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart,
                                   botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)


def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                                 text="Можно вводить только число в десятичной системе исчсиления\n Попробуйте еще раз")
        my_inputInt(botQuestion,chat_id,txtQuestion,ResponseHandler)