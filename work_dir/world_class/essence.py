import math


class essence:
    def init(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_cord(self):
        w = (self.x, self.y)
        return w

    def do_new_cord(self, x, y):
        cordss = (x, y)
        self.abs_cords = (self.x, self, y)
        animation(self, cordss)
        self.x = x
        self.y = y


def animation(self, cordss):
    distance = math.sqrt((cordss[0] - self.abs_cords[0]) + (cordss[1] - self.abs_cords[1]))

    tmp_x = self.abs_cords[0] - cordss[0]
    tmp_y = self.abs_cords[1] - cordss[1]
    try:
        angel = tmp_x / tmp_y
    except ZeroDivisionError:
        return cordss
    angel = math.degrees(math.atan(angel))

    if distance < 1:
        self.speed = 0
    elif 1 <= distance <= 30:
        if self.speed > 1:
            self.speed -= 0.5
    else:
        self.speed += 0.07

    if self.abs_cords[1] - cordss[1] < 0:
        x = self.abs_cords[0] + math.sin(angel * math.pi / 180) * self.speed
        y = self.abs_cords[1] + math.cos(angel * math.pi / 180) * self.speed
    else:
        x = self.abs_cords[0] - math.sin(angel * math.pi / 180) * self.speed
        y = self.abs_cords[1] - math.cos(angel * math.pi / 180) * self.speed

    self.abs_cords = [x, y]

    return self.abs_cords
