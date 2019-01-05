import enemy6
import pyxel
from . import mission

class Mission6(mission.Mission):

    def __init__(self):
        print("Mission6")
        self.enemy = enemy6.Enemy6(pyxel.width / 2, 40, 16, 16, 50, 8)
        super().__init__()

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def collision_detection(self):
        super().collision_detection()
