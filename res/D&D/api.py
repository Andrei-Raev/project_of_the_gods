from json import load

import telebot

from date_reader import Player

from threading import Thread

from datetime import datetime, timedelta
from random import randint
from time import sleep

# print(str(Player('date/players/2.json')))

# from User_Engine import main
bot = telebot.TeleBot('1273116436:AAG5ZLR1nk0Jl3VOdwm4UT3UK0WQKcdCVQo')
# ----------[РАБОЧИЕ ПЕРЕМЕННЫЕ]----------
submit_exit = False
is_started = False
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
# Клавиатура подтверждения
submit = telebot.types.InlineKeyboardMarkup()
submit.row_width = 1
submit.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="1"),
           telebot.types.InlineKeyboardButton(text="Нет", callback_data="2"))


# Создает клавиатуру из списка
def creat_inline_item_list_keyboard(spisok: list) -> telebot.types.InlineKeyboardMarkup:
    tmp = telebot.types.InlineKeyboardMarkup()
    for tmp_item in enumerate(spisok):
        tmp.add(telebot.types.InlineKeyboardButton(text=tmp_item[1].capitalize(), callback_data=str(tmp_item[0])))

    return tmp


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
'''def throw(message):
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


# mes = bot.send_message(780828132, 'Выберите:', reply_markup=player_list)
#
# mi = mes.message_id
# peoples = []
'''
'''
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
'''

players_name = {'дима': 0, 'дмитрий': 0, 'гюнтер': 0, 'катя': 1, 'корона': 1, 'андрей': 2, 'ларка': 2, 'ла-рум': 2,
                'алина': 3, 'листок': 3, 'мак': 4, 'лера': 4, 'янхи': 5, 'егор': 5}
name_ids = {0: 'гюнтер', 1: 'корона', 2: 'ларка', 3: 'листок', 4: 'мак', 5: 'янхи'}


def show_i(name_id):
    name = name_ids[name_id]
    with open('date/game/inventory.json', 'r', encoding='utf-8') as json_file:
        invent = load(json_file)
        invent = invent[name]
    tmp_markups = creat_inline_item_list_keyboard(invent)
    print(type(tmp_markups))
    bot.send_message(780828132, f'Инвентарь *{name.capitalize()}*:', parse_mode="Markdown",
                     reply_markup=tmp_markups)


def hp_show():
    res = 'Хиты команды:\n'
    with open('date/game/hp.json', 'r', encoding='utf-8') as json_file:
        hp = load(json_file)

    for pl_id in range(6):
        if pl_id == 4:
            continue
        print(pl_id)
        tmp_pl = Player(f'date/players/{pl_id}.json')
        res += f'\t*{tmp_pl.name}*:\t{hp[name_ids[pl_id]]}/{tmp_pl.hp}\n'

    bot.send_message(780828132, res.strip(), parse_mode="Markdown")


@bot.message_handler()
def command_execute(message):
    try:
        text = message.text.split()
        command_type, player_id = text[0].lower(), players_name[text[1].lower()]
    except IndexError:
        command_type = message.text.lower()

        if command_type.lower() == 'хп' or command_type.lower() == 'hp':
            return hp_show()

        bot.send_message(780828132, f'Команда *{message.text}* некорректна', parse_mode="Markdown")
        return
    except KeyError:
        bot.send_message(780828132, f'Игрока *{text[1]}* не существует', parse_mode="Markdown")
        return

    if command_type.lower() == 'и':
        show_i(player_id)


while True:
    try:
        bot.polling(none_stop=False)

    except Exception as e:
        print('ERROR', e, e.__class__.__name__)
        sleep(1)
