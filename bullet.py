import pyxel


class bullet():

    def __init__(self, radius, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self. vx = vx
        self.vy = vy
        self.color = color
        self.count = 0
        self.delete_ok = False

    def update(self):
        self.count += 1
        self.y += 1
        if self.x < 0 or self.x > pyxel.width or self.y < 0 or self.y > pyxel.height:
            self.delete_ok = True

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)
