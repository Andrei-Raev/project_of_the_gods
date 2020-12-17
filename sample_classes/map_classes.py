TYPE_BLOCKS = {1: 'grass', 2: 'stone', }


class Obekt:
    def __init__(self, cord: tuple, preor=0):
        self.cord = cord
        self.importance = preor

    def get_x(self) -> int:
        return int(self.cord[0])

    def get_y(self) -> int:
        return int(self.cord[1])

    def get_preor(self) -> int:
        return int(self.importance)

    def get_pos(self) -> tuple:
        return tuple(self.cord)


class Landscape(Obekt):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)


class Grass(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 1


class Stone(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 2


'''
class poctr(Obekt):
    def __init__(self, y, x, preor=2):
        super().__init__(y, x, preor)
'''


class Entity(Obekt):
    def __init__(self, cord, hp, preor=3):
        super().__init__(cord, preor)
        self.hp = hp

    def get_hp(self):
        return self.hpв


class Item:
    def __init__(self):
        pass

#FFFFFF