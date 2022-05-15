import pyxel
import math


COLLISION_RADIUS_RATE = 0.3  # 외형 당 판정이 얼마나 작은 지...? 한 번 숫자 바꾸어보기: (0,1)사이에서



class Bullet(): # 에이전트가 쏘는 총알

    def __init__(self, radius, x, y, movement_x, movement_y, speed, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.collision_radius = self.radius * COLLISION_RADIUS_RATE  # 当たり判定
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
            # 이동
            self.x += self.movement_x * self.speed
            self.y += self.movement_y * self.speed

            # 이동에 대한 함수가 설정되어 있지 않으면 실행
            for move_function in self.move_functions:
                if move_function is not None:
                    try:
                        next(move_function)
                    except StopIteration:
                        self.move_functions.remove(move_function)

        # 탄막이 화면 밖으로 나오면 해당 탄막 비활성화
        if self.x < 0 or self.x > pyxel.width or self.y < 0 or self.y > pyxel.height:
            self.count = 0
            self.move_functions.clear()
            self.is_active = False

    def draw(self):
        """
        화면 describe
        """
        if self.is_active:
            pyxel.circ(self.x, self.y, self.radius, self.color)


class EnemyBullet(Bullet): # boss가 쏘는 총알

    def __init__(self, radius, x, y, movement_x, movement_y, speed, color): #(탄막 반경, px,py, vx?, vy?, speed?, 색깔)
        super().__init__(radius, x, y, movement_x, movement_y, speed, color)

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
                self.movement_x = math.cos(math.radians(angle))
                self.movement_y = math.sin(math.radians(angle))
                self.speed = speed
                break

            yield None

    def pattern2(self, a, min_speed, max_speed, start_count, end_count):
        while True:
            if self.count >= start_count:
                self.speed += a
                if not (min_speed < self.speed < max_speed):
                    break
            if self.count > end_count:
                break

            yield None

    def pattern3(self, angle, start_count):
        while True:
            if self.count == start_count:
                self.movement_x = math.cos(math.radians(angle))
                self.movement_y = math.sin(math.radians(angle))
                break

            yield

    def pattern4(self, bullet_angle_function, interval_count, start_count=0, end_count=math.inf):
        count = 0
        while count < end_count:
            if count >= start_count:
                if (start_count + count) % interval_count == 0:
                    angle = math.degrees(math.atan2(self.movement_y, self.movement_x))
                    self.movement_x = math.cos(math.radians(angle + bullet_angle_function(count)))
                    self.movement_y = math.sin(math.radians(angle + bullet_angle_function(count)))

            count += 1
            yield


class PlayerBullet(Bullet):

    def __init__(self, radius, x, y, movement_x, movement_y, speed, color):
        super().__init__(radius, x, y, movement_x, movement_y, speed, color)

    def update(self):
        super().update()

    def draw(self):
        super().draw()
