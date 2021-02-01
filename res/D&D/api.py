from json import load, dump

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
submit.row_width = 2
submit.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="yes"),
           telebot.types.InlineKeyboardButton(text="Нет", callback_data="no"))


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

players_name = {'дима': 0, 'дмитрий': 0, 'гюнтер': 0, 'катя': 1, 'крона': 1, 'андрей': 2, 'ларка': 2, 'ла-рум': 2,
                'алина': 3, 'листок': 3, 'мак': 4, 'лера': 4, 'янхи': 5, 'егор': 5}
name_ids = {0: 'гюнтер', 1: 'крона', 2: 'ларка', 3: 'листок', 4: 'мак', 5: 'янхи'}

TARGET = 1278338237
last_inventory_message_id = 0
last_inventory_player_id = 0
last_inventory_data = ['', '', 0]

count_request = 1


def normalize(*args):
    res = []
    for i in enumerate(args):
        if i[0] == 0:
            res.append(name_ids[i[1]])
        else:
            res.append(i[1])
    return tuple(res)


def log(function_to_decorate):
    def log_decorate(*args):
        with open('log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(
                f'\n----------[{datetime.now()}]----------\nВыполнена функция: {function_to_decorate.__name__}\nАргументы: {normalize(*args)}')
        function_to_decorate(*args)

    return log_decorate


def send_log():
    with open('log.txt', 'r', encoding='utf-8') as log_file:
        log_text = log_file.read()

    open('log.txt', 'w', encoding='utf-8').close()

    while len(log_text) > 4000:
        bot.send_message(780828132, log_text[:4000])
        log_text = log_text[4000:]
    bot.send_message(780828132, log_text[:4000])


def cmd(command):
    eval(command)


def ans_edit(string: str) -> str:
    string = string.replace('\t', '    ')
    return string


# ----------
def show_inventory_button(name_id):
    global last_inventory_message_id
    name = name_ids[name_id]
    with open('date/game/inventory.json', 'r', encoding='utf-8') as json_file:
        invent = load(json_file)
        invent = invent[name]
    tmp_mes = bot.send_message(TARGET, f'Инвентарь *{name.capitalize()}*:', parse_mode="Markdown",
                               reply_markup=creat_inline_item_list_keyboard(invent))
    last_inventory_message_id = tmp_mes.id
    return tmp_mes


@log
def hp_show():
    res = 'Хиты команды:\n'
    with open('date/game/hp.json', 'r', encoding='utf-8') as json_file:
        hp = load(json_file)

    for pl_id in range(6):
        print(pl_id)
        tmp_pl = Player(f'date/players/{pl_id}.json')
        if hp[name_ids[pl_id]] < 0:
            res += f'\t*{tmp_pl.name}*:\t*мертв*\n'
        else:
            res += f'\t*{tmp_pl.name}*:\t{hp[name_ids[pl_id]]}/{tmp_pl.hp} ({round((hp[name_ids[pl_id]] / tmp_pl.hp) * 100)}%)'
            if hp[name_ids[pl_id]] / tmp_pl.hp < .20 and hp[name_ids[pl_id]] != -1:
                res += ' *Критической состояние!*\n'
            else:
                res += '\n'

    bot.send_message(TARGET, ans_edit(res.strip()), parse_mode="Markdown")


@log
def carte(pl_id):
    bot.send_message(TARGET, Player(f'date/players/{pl_id}.json')[0])
    bot.send_message(TARGET, Player(f'date/players/{pl_id}.json')[1])
    bot.send_message(TARGET, Player(f'date/players/{pl_id}.json')[2])


@log
def item_list(pl_id):
    name = name_ids[pl_id]
    with open('date/game/inventory.json', 'r', encoding='utf-8') as json_file:
        invent = load(json_file)
        invent = invent[name]
    bot.send_message(TARGET, f'Инвентарь *{name.capitalize()}*:\n' + '\n'.join(
        map(lambda tmp_it: f'{tmp_it[0] + 1}. ' + tmp_it[1].capitalize(), enumerate(sorted(invent)))),
                     parse_mode="Markdown")


@log
def get_item(pl_id, item: str):
    name = name_ids[pl_id]
    with open('date/game/inventory.json', 'r', encoding='utf-8') as json_file:
        invent = load(json_file)
    invent[name.lower()].append(item)
    with open('date/game/inventory.json', 'w', encoding='utf-8') as json_file:
        dump(invent, json_file, ensure_ascii='utf8')

    bot.send_message(TARGET, f'Игроку *{name.capitalize()}* выдан предмет *{item.capitalize()}*', parse_mode="Markdown")


def del_item(pl_id):
    global last_inventory_data
    global last_inventory_player_id
    last_inventory_player_id = pl_id
    show_inventory_button(pl_id)


@log
def del_item_f():
    global last_inventory_data
    global last_inventory_player_id
    name = name_ids[last_inventory_player_id]
    with open('date/game/inventory.json', 'r', encoding='utf-8') as json_file:
        invent = load(json_file)
    item = invent[name][last_inventory_data[2]]
    del invent[name][last_inventory_data[2]]
    with open('date/game/inventory.json', 'w', encoding='utf-8') as json_file:
        dump(invent, json_file, ensure_ascii='utf8')

    bot.edit_message_text(f'У игрока *{name.capitalize()}* удален предмет *{item.capitalize()}*', chat_id=TARGET,
                          message_id=last_inventory_message_id, reply_markup=None, parse_mode="Markdown")


def lvl_finder(exp: int) -> int:
    if exp < 300:
        return 1
    elif exp < 900:
        return 2
    elif exp < 2700:
        return 3
    elif exp < 6500:
        return 4
    elif exp < 14000:
        return 5
    elif exp < 23000:
        return 6
    elif exp < 34000:
        return 7
    elif exp < 48000:
        return 8
    elif exp < 64000:
        return 9
    elif exp < 85000:
        return 10
    elif exp < 100000:
        return 11
    elif exp < 120000:
        return 12
    elif exp < 140000:
        return 13
    elif exp < 165000:
        return 14
    elif exp < 195000:
        return 15
    elif exp < 225000:
        return 16
    elif exp < 265000:
        return 17
    elif exp < 305000:
        return 18
    elif exp < 355000:
        return 19
    else:
        return 20


@log
def exp_show():
    with open('date/game/exp.json', 'r', encoding='utf-8') as json_file:
        exp = load(json_file)
    res = 'Общий опыт:\n'
    for i in exp.keys():
        res += f'*{i.capitalize()}*:\t{lvl_finder(exp[i])} ур. ({exp[i]})\n'

    bot.send_message(TARGET, ans_edit(res), parse_mode="Markdown")


@log
def get_exp(pl_id, count):

    with open('date/game/exp.json', 'r', encoding='utf-8') as json_file:
        exp = load(json_file)

    if pl_id == "все":
        for i in exp.keys():
            exp[i] += count
    else:
        exp[name_ids[pl_id]] += count

    with open('date/game/exp.json', 'w', encoding='utf-8') as json_file:
        dump(exp, json_file, ensure_ascii='utf8')
    if pl_id == "все":
        bot.send_message(TARGET, f'*Всем* выдано *{count}* единиц опыта',
                         parse_mode="Markdown")
    else:
        bot.send_message(TARGET, f'Игроку *{name_ids[pl_id].capitalize()}* выдано *{count}* единиц опыта',
                         parse_mode="Markdown")


@log
def hil(pl_id, hp_count):
    if hp_count < 0:
        return kik(pl_id, hp_count)

    with open('date/game/hp.json', 'r', encoding='utf-8') as json_file:
        hp = load(json_file)

    tmp_pl = Player(f'date/players/{pl_id}.json')
    hp[name_ids[pl_id]] += hp_count
    if hp[name_ids[pl_id]] > int(tmp_pl.hp):
        hp[name_ids[pl_id]] = int(tmp_pl.hp)

    with open('date/game/hp.json', 'w', encoding='utf-8') as json_file:
        dump(hp, json_file, ensure_ascii='utf8')

    answer = f'Игрок *{tmp_pl.name}* был вылечен на *{hp_count}* хп\nТеперь хиты составляют: {hp[name_ids[pl_id]]}/{tmp_pl.hp} ({round((hp[name_ids[pl_id]] / tmp_pl.hp) * 100)}%)'

    if hp[name_ids[pl_id]] == int(tmp_pl.hp):
        answer += '\n*Хиты игрока полностью восстановлены!*'

    bot.send_message(TARGET, ans_edit(answer), parse_mode="Markdown")


@log
def kik(pl_id, hp_count):
    with open('date/game/hp.json', 'r', encoding='utf-8') as json_file:
        hp = load(json_file)

    hp_count = abs(hp_count)
    tmp_pl = Player(f'date/players/{pl_id}.json')
    hp[name_ids[pl_id]] -= hp_count
    death_answer = ''

    if hp[name_ids[pl_id]] < 0:
        death_answer = f'\n\nИгрок *{tmp_pl.name}* получил критический урон:\n'
        throw_death = [randint(1, 20) for _ in range(3)]

        if sum(throw_death) >= 30:
            death_answer += f'\t*Спасбросок успешен!* ({", ".join(list(map(lambda t: str(t), throw_death)))} (Сумма: *{sum(throw_death)}*))'
            hp[name_ids[pl_id]] = 0
        else:
            death_answer += f'\t*Спасбросок провален!* ({", ".join(list(map(lambda t: str(t), throw_death)))} (Сумма: *{sum(throw_death)}*))\n*Игрок умер :(*'
            hp[name_ids[pl_id]] = -1

    with open('date/game/hp.json', 'w', encoding='utf-8') as json_file:
        dump(hp, json_file, ensure_ascii='utf8')

    answer = f'Игроку *{tmp_pl.name}* был нанесен урон на *{hp_count}* хп\nТеперь хиты составляют: {hp[name_ids[pl_id]]}/{tmp_pl.hp} ({round((hp[name_ids[pl_id]] / tmp_pl.hp) * 100)}%)' + death_answer

    if hp[name_ids[pl_id]] / tmp_pl.hp < .20 and hp[name_ids[pl_id]] != -1:
        answer += '\n*Критической состояние!*'

    bot.send_message(TARGET, ans_edit(answer), parse_mode="Markdown")


@bot.message_handler()
def command_execute(message):
    try:
        text = message.text.split()
        if text[1] == 'все' and (text[0].lower() == 'повышение' or text[0].lower() == 'п'):
            command_type, player_id = text[0].lower(), text[1].lower()
        else:
            command_type, player_id = text[0].lower(), players_name[text[1].lower()]

        if command_type == 'карта' or command_type == 'к':
            return carte(player_id)  # Готово
        elif command_type == 'вещи' or command_type == 'в':
            return item_list(player_id)  # Готово
        elif command_type == 'дать' or command_type == 'д':
            return get_item(player_id, text[2])  # Готово
        elif command_type == 'убрать' or command_type == 'у':
            return del_item(player_id)  # Готово
        elif command_type == 'лечить' or command_type == 'л':
            return hil(player_id, int(text[2]))  # Готово
        elif command_type == 'бить' or command_type == 'б':
            return kik(player_id, int(text[2]))  # Готово
        elif command_type == 'повышение' or command_type == 'п':
            return get_exp(player_id, int(text[2]))  # Готово

        bot.send_message(TARGET, f'Команда *{message.text}* некорректна', parse_mode="Markdown")
        return
    except IndexError:
        command_type = message.text.lower()

        if command_type.lower() == 'хп' or command_type.lower() == 'hp' or command_type.lower() == 'х':
            return hp_show()  # Готово
        elif command_type == 'опыт' or command_type == 'о':
            return exp_show()  # Готово
        elif command_type == 'log':
            return send_log()

        bot.send_message(TARGET, f'Команда *{message.text}* некорректна', parse_mode="Markdown")
        return
    except KeyError:
        if command_type == 'cmd':
            return cmd(message.text[4:])

        bot.send_message(TARGET, f'Игрока *{text[1]}* не существует', parse_mode="Markdown")
        return
    except ValueError:
        bot.send_message(TARGET, f'*{text[2]}* не число', parse_mode="Markdown")
        return


@bot.callback_query_handler(func=lambda call: call.message.id == last_inventory_message_id)
def select_player(callback):
    global last_inventory_data
    global last_inventory_player_id

    if callback.data == 'yes':
        del_item_f()
    elif callback.data == 'no':
        bot.edit_message_text('Операция отменена', chat_id=TARGET,
                              message_id=last_inventory_message_id, reply_markup=None)
    else:
        name = name_ids[last_inventory_player_id]
        with open('date/game/inventory.json', 'r', encoding='utf-8') as json_file:
            invent = load(json_file)
        item = invent[name][int(callback.data)]

        last_inventory_data[2] = int(callback.data)
        last_inventory_data[1] = name
        last_inventory_data[0] = item

        bot.edit_message_text('Вы уверены?', chat_id=TARGET,
                              message_id=last_inventory_message_id, reply_markup=submit)


while True:
    try:
        bot.polling(none_stop=False)
    except Exception as e:
        print(f'----------[{datetime.now()}]----------\nОшибка ({e.__class__.__name__})\n{e}')
        sleep(1)
