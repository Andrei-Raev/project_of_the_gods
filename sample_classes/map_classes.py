class obekt:
    def __init__(self, y, x, preor=3):
        self.y = y
        self.x = x
        self.preor = preor

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_preor(self):
        return self.preor

    def get_pos(self):
        return (self.y, self.x)


class relef(obekt):
    def __init__(self, y, x, preor=3):
        self.y = y
        self.x = x
        self.preor = preor


class poctr(obekt):
    def __init__(self, y, x, preor=2):
        self.y = y
        self.x = x
        self.preor = preor


class entiti(obekt):
    def __init__(self, y, x, hp, preor=1):
        self.y = y
        self.x = x
        self.preor = preor
        self.hp = hp

    def get_hp(self):
        return self.hp


class predmet():
    def __init__(self):
        pass
