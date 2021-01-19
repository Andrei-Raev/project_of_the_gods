import telebot

from date_reader import Player

from datetime import datetime, timedelta
from random import randint
from time import sleep

# print(str(Player('date/players/andrei.json')))

# from User_Engine import main
bot = telebot.TeleBot('1273116436:AAGOxkyIYhLyeI8Vh7IuT5TU09h8-a503CY')
# ----------[РАБОЧИЕ ПЕРЕМЕННЫЕ]----------
submit_exit = False
is_started = False
bot.send_message(780828132, "Тест")
# ----------[КЛАВИАТУРЫ]----------
# -={outline}=-
# Клавиатура с вариантами кубов
cubes = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, selective=False)
cubes.row('Д4', 'Д6', 'Д8')
cubes.row('Д10', 'Д20', 'Д100')

# Старая клваиатура с командами
commands = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, selective=False)
commands.row('/throw', '/stop')

# -={inline}=-
# Подтверждение выхода от моего имени
me_submit_exit = telebot.types.InlineKeyboardMarkup()
yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="m_confirm_exit")
no = telebot.types.InlineKeyboardButton(text="Нет", callback_data="m_cancel_exit")
me_submit_exit.add(yes, no)

# Подтверждение выхода от имени Арсения
submit_exit = telebot.types.InlineKeyboardMarkup()
yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="confirm_exit")
no = telebot.types.InlineKeyboardButton(text="Нет", callback_data="cancel_exit")
submit_exit.add(yes, no)

# Получение списка играющих
player_list = telebot.types.InlineKeyboardMarkup()
nemo = telebot.types.InlineKeyboardButton(text="Немо", callback_data="nemo")
piter = telebot.types.InlineKeyboardButton(text="Питер", callback_data="piter")
jeims = telebot.types.InlineKeyboardButton(text="Джеймс", callback_data="jeims")
silva = telebot.types.InlineKeyboardButton(text="Сильва", callback_data="silva")
teren = telebot.types.InlineKeyboardButton(text="Терен", callback_data="teren")
idown = telebot.types.InlineKeyboardButton(text="Ядаун", callback_data="yadaun")
submit = telebot.types.InlineKeyboardButton(text="Подтвердить", callback_data="submit_players")
player_list.row_width = 1
player_list.add(nemo, piter, jeims, silva, teren, idown, submit)


# ----------[СИСТЕМНЫЕ ФУНКЦИИ]---------
# Проверяет является ли отпрвитель мной(Андреем)
def check_me(message):
    return True if message.from_user.id == 780828132 else False


# Проверяет является ли отпрвитель Арсением
def check_admin(message):
    return True if message.from_user.id == 1278338237 else False


# Проверяет отправленно ли сообщение из общего чата
def check_common_сhat(message):
    return True if message.chat.id == -406124985 else False


# Проверяет отправленно ли сообщение из группы
def check_group(message):
    return True if message.type == 'group' else False


# ----------[ВНУТРЕИНРОВЫЕ ФУНКЦИИ]----------
# Бросок куба(бросок и мультибросок куба "Дхх")
def throw(message):
    if not message.text.lower().startswith('д'):
        return
    try:
        tmp = message.text[1:].split()
        count = -1
        if len(tmp) == 1:
            num = int(message.text[1:])
        elif len(tmp) == 2:
            num, count = int(tmp[0]), int(tmp[1])
    except:
        return
    if count == -1:
        if num < 1:
            bot.send_message(-406124985, 'Такого куба не существует!')
            return
        if num == 4 or num == 8 or num == 10 or num == 20 or num == 100:

            bot.send_message(-406124985, 'Результат броска куба Д' + str(num) + ': ' + str(randint(1, num)))
        else:
            bot.send_message(-406124985, 'Такого куба не существует!')
    elif count > 0:
        res = []
        res2 = []
        for _ in range(count):
            i = randint(1, num)
            res.append(i)
            res2.append(str(i))
        tmp = ', '.join(res2)
        bot.send_message(-406124985,
                         'Результат мальтиброска куба Д' + str(num) + ': ' + str(tmp) + '\nСреднее значение: ' + str(
                             sum(res) / count) + '\nСумма: ' + str(sum(res)))


mes = bot.send_message(780828132, 'Выберите:', reply_markup=player_list)

mi = mes.message_id
peoples = []


@bot.callback_query_handler(func=lambda c: True)
def select_player(callback):
    ci = 780828132
    global is_started
    if not is_started:
        if callback.data == 'submit_players':
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.\nНачало игры', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
            print(peoples)
            is_started = True
        elif callback.data == 'nemo':
            if 'Немо' in peoples:
                peoples.remove('Немо')
            else:
                peoples.append('Немо')
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
        elif callback.data == 'piter':
            if 'Питер' in peoples:
                peoples.remove('Питер')
            else:
                peoples.append('Питер')
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
        elif callback.data == 'jeims':
            if 'Джеймс' in peoples:
                peoples.remove('Джеймс')
            else:
                peoples.append('Джеймс')
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
        elif callback.data == 'silva':
            if 'Сильва' in peoples:
                peoples.remove('Сильва')
            else:
                peoples.append('Сильва')
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
        elif callback.data == 'teren':
            if 'Терен' in peoples:
                peoples.remove('Терен')
            else:
                peoples.append('Терен')
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
        elif callback.data == 'yadaun':
            if 'Ядаун' in peoples:
                peoples.remove('Ядаун')
            else:
                peoples.append('Ядаун')
            bot.edit_message_text('Выбраны игроки: ' + ', '.join(peoples) + '.', chat_id=ci, message_id=mi,
                                  reply_markup=player_list)
