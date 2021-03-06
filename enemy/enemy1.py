from enemy import enemy


class Enemy1(enemy.Enemy):
    def __init__(self, x, y, width, height, hp, color):
        super().__init__(x, y, width, height, hp, color)
        self.shot_positions.append(enemy.ShotPosition(self.x, self.y))
        self.shot_functions.append(self.shot_positions[0].pattern3(1, 11, 1.5, 60))

    def update(self):
        super().update()

    def draw(self):
        super().draw()
