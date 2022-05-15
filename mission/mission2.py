from enemy import enemy2
import pyxel
from . import mission


class Mission2(mission.Mission):

    def __init__(self):
        self.enemy = enemy2.Enemy2(pyxel.width / 2, 20, 16, 16, 240, 8)
        super().__init__()

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def collision_detection(self):
        super().collision_detection()
