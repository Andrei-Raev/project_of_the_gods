from json import load, dump
from pyperclip import copy

with open('date/game/class.json', 'r', encoding='utf-8') as file:
    CLASSES = load(file)
with open('date/game/race.json', 'r', encoding='utf-8') as file:
    RACE = load(file)


def recycle(string: str, point=False) -> str:
    string = string.strip().capitalize()
    if point:
        if string.endswith('.'):
            return string
        else:
            return string + '.'
    else:
        if string.endswith('.'):
            return string[:-1]
        else:
            return string


def skell_recycle(string: str) -> str:
    if '%' in string:
        string, lvl = string.split('%')
        string = recycle(string)
        return f'{string}, {lvl} ур.'
    else:
        return recycle(string)


class Player:
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            self.data = load(file)

        self.name = self.data['name']
        self.owner = self.data['owner']
        self.gender = self.data['gender']

        self.hp = int(self.data['hp'])
        self.kd = int(self.data['kd'])

        self.classes = CLASSES[self.data['class']][0]  # Добавить описание навыков
        self.race = RACE[self.data['race']][0][0]  # Добавить описание навыков

        self.static = self.data['specifications']['static']
        self.height = int(self.data['specifications']['height'])
        self.weight = int(self.data['specifications']['weight'])
        self.age = int(self.data['specifications']['age'])

        self.appearance = self.data['specifications']['appearance']
        self.temper = self.data['specifications']['temper']
        self.background = self.data['specifications']['background']

        self.skill = self.data['skill']
        self.items = self.data['items']

    def __str__(self):
        res = f'Карта персонажа (Владелец: {self.owner})\n\n'

        res += f'Имя:\t{self.name}\nПол:\t{"Мужской" if self.gender == "M" else "Женский"}\nРаса:\t{self.race}\nКласс:\t{self.classes}\n\n'
        res += f'Характеристики:\n\tСила:\t{self.static["strength"]}\n\tЛовкость:\t{self.static["dexterity"]}\n\tТелосложение:\t{self.static["constitution"]}\n\tИнтеллект:\t{self.static["intelligence"]}\n\tМудрость:\t{self.static["wisdom"]}\n\tХаризма:\t{self.static["charisma"]}\n\n\tHP:\t{self.hp}\n\tКД:\t{self.kd}\n\n'
        res += f'Биометрические данные:\n\tВозраст:\t{self.age} лет\n\tРост:\t{self.height} см.\n\tВес:\t{self.weight} кг.\n\n'
        res += f'Внешность:\n\tТело:\t{recycle(self.appearance["skin"])}\n\tВолосы:\t{recycle(self.appearance["hair"])}\n\tГлаза:\t{recycle(self.appearance["eyes"])}\n\n'
        res += f'Характер ({self.temper[0]}):\t{self.temper[1]}\n\n'
        res += f'\n----------[Начало предыстории]----------\n{recycle(self.background, point=True)}\n----------[Конец предыстории]----------\n\n'

        if self.items:
            res += f'Предметы:\n\t' + '\n\t'.join(list(map(lambda x: recycle(x), self.items)))
        else:
            res += f'Предметы:\tОтсутствуют'

        res += '\n\n'

        if self.skill:
            res += f'Навыки:\n\t' + '\n\t'.join(list(map(lambda x: skell_recycle(x), self.skill)))
        else:
            res += f'Навыки:\tОтсутствуют'

        return res


copy(str(Player('date/players/dima.json')))
