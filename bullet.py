import pyxel
import math


class Bullet():

    def __init__(self, radius, x, y, movement_x, movement_y, speed, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.collision_radius = self.radius * 0.3
        self.speed = speed
        self.color = color
        self.count = 0
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.is_active = False
        self.move_functions = []

    def update(self):
        if self.is_active:
            self.count += 1
            self.x += self.movement_x * self.speed
            self.y += self.movement_y * self.speed
            # print(self.x, self.y)

            for move_function in self.move_functions:
                # print("O")
                if move_function is not None:
                    # print("A")
                    try:
                        next(move_function)
                    except StopIteration:
                        self.move_functions.remove(move_function)

        if self.x < 0 or self.x > pyxel.width or self.y < 0 or self.y > pyxel.height:
            self.count = 0
            self.move_functions.clear()
            self.is_active = False

    def draw(self):
        if self.is_active:
            pyxel.circ(self.x, self.y, self.radius, self.color)


class EnemyBullet(Bullet):

    def __init__(self, radius, x, y, movement_x, movement_y, speed, color):
        super().__init__(radius, x, y, movement_x, movement_y, speed, color)
        self.count = 0

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def set_move_function(self, move_function):
        self.move_functions.append(move_function)

    def pattern1(self, move1_count, stop_count, angle, speed):
        while True:
            if self.count == move1_count:
                self.movement_x = self.movement_y = 0
            elif self.count == move1_count + stop_count:
                print("POP")
                self.movement_x = math.cos(math.radians(angle))
                self.movement_y = math.sin(math.radians(angle))
                self.speed = speed
                break

            yield None

    def pattern2(self, a, min_speed, max_speed, start_count, end_count):
        while True:
            if self.count > start_count:
                self.speed += a
                if not (min_speed < self.speed < max_speed):
                    break
            elif self.count > end_count:
                break

            yield None

    def pattern3(self, angle, start_count):
        while True:
            # print(self.count, start_count)
            if self.count == start_count:
                # print("mom")
                self.movement_x = math.cos(math.radians(angle))
                self.movement_y = math.sin(math.radians(angle))
                break

            yield

class PlayerBullet(Bullet):

    def __init__(self, radius, x, y, movement_x, movement_y, speed, color):
        super().__init__(radius, x, y, movement_x, movement_y, speed, color)

    def update(self):
        super().update()

    def draw(self):
        super().draw()
