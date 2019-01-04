import enemy1
import pyxel
import player
from scene import Scene


class Mission():

    def __init__(self):
        print("Mission")
        self.player = player.Player(pyxel.width / 2, 200, 10, 10, 1, 2)
        self.enemy_max_hp = self.enemy.hp
        self.return_value = Scene.NO_SCENE_CHANGE
        self.is_clear = False
        self.after_clear_time = 0

    def update(self):
        self.player.update()
        if not self.is_clear:
            self.enemy.update()
            self.collision_detection()
        else:
            self.after_clear_time += 1

        if self.after_clear_time == 180:
            self.return_value = Scene.MISSION_SELECT

    def draw(self):
        self.player.draw()
        if not self.is_clear:
            self.enemy.draw()
            pyxel.line(10, 10, 170 * self.enemy.hp / self.enemy_max_hp + 10, 10, 13)

        if self.is_clear:
            if self.after_clear_time % 30 < 15:
                pyxel.text(90, pyxel.height / 2, "Clear!", 14)
            else:
                pyxel.text(90, pyxel.height / 2, "Clear!", 15)

    def enemy_playerbullet_detection(self):
        x1 = self.enemy.view_start_x
        y1 = self.enemy.view_start_y
        x2 = self.enemy.view_start_x + self.enemy.width
        y2 = self.enemy.view_start_y + self.enemy.height
        for player_bullet in self.player.bullets:
            x = player_bullet.x
            y = player_bullet.y
            r = player_bullet.radius

            C1 = x > x1 and x < x2 and y > y1 - r and y < y2 + r
            C2 = x > x1 - r and x < x2 + r and y > y1 and y < y2
            C3 = (x1 - x) ** 2 + (y1 - y) ** 2 < r ** 2
            C4 = (x2 - x) ** 2 + (y1 - y) ** 2 < r ** 2
            C5 = (x2 - x) ** 2 + (y2 - y) ** 2 < r ** 2
            C6 = (x1 - x) ** 2 + (y2 - y) ** 2 < r ** 2

            if C1 or C2 or C3 or C4 or C5 or C6:
                self.enemy.hp -= 1
                print(self.enemy.hp)
                if self.enemy.hp <= 0:
                    self.mission_clear()
                player_bullet.is_active = False

    def player_enemybullet_detection(self):
        player_x = self.player.x
        player_y = self.player.y
        player_r = self.player.collision_radius
        # print(player_x, player_y, player_r)
        for shot_position in self.enemy.shot_positions:
            for enemy_bullet in shot_position.bullets:
                x = enemy_bullet.x
                y = enemy_bullet.y
                r = enemy_bullet.radius
                print(x, y, r)
                if (player_x - x) ** 2 + (player_y - y) ** 2 <= (player_r + r) ** 2:
                    # print("Hit")
                    enemy_bullet.is_active = False
                    return True
        return False

    def collision_detection(self):
        self.enemy_playerbullet_detection()
        if self.player_enemybullet_detection():
            self.return_value = Scene.MISSION_SELECT

    def mission_clear(self):
        self.is_clear = True
