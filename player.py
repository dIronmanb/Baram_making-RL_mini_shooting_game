import pyxel
import bullet_pool
import math


class Player():
    x = -10
    y = -10

    # 현재 mission.py에서 Player객체 생성함 >> (pyxel.width / 2, 200, 10, 10, 1, 2)
    def __init__(self, x, y, width, height, collision_radius, speed):
        Player.x = x
        Player.y = y
        self.width = width
        self.height = height
        self.view_start_x = self.x - self.width / 2  # 사각형의 x시작점
        self.view_start_y = self.y - self.height / 2  # 사각형의 y시작점
        self.collision_radius = collision_radius  # 아마 충돌 판정 아닐까??
        self.speed = speed 
        self.slow_speed = 0.5  # 低速移動したときのスピード
        self.count = 0
        self.bullet_pool = bullet_pool.PlayerBulletPool(28)
        self.bullets = []

        # Action List
        self.action_space = ['up', 'down', 'left', 'right', 'stop'] # slow는 넣지 말자. 생각할게 많아진다.
        self.n_actions = len(self.action_space)

    @classmethod
    def getPosition(cls):
        return cls.x, cls.y

    def update(self, action = 0): #action은 0 ~ 4중에 하나
        self.count += 1
        for b in self.bullets[:]:
            b.update()
            if not b.is_active:
                self.bullets.remove(b)
        
        # 기존의 move함수
        # self.move()
        
        # 내가 구현한 함수: DQN이 알아서 이리저리 가도록
        self.move_by_action(action)

        # # move 고쳐 버리기 >> 이게 행동인데, time_interval를 짧게 할수록 다양하게 움직이겠지만 시간 및 복잡성 증가
        # if self.count % 15 == 0:
        #     self.step(action)

        if self.count % 10 == 0: # 자동 공격
        #if pyxel.btnp(pyxel.KEY_Z, 10, 10): # Z키를 눌러서 공격을 했다면...?
            self.shot(6, -97.5, 3, 5, 1, 1) #(way, start_angle, delta_angle, speed, radius, color)
        


    # 화면을 그리는 함수
    def draw(self):
        pyxel.rect(self.view_start_x, self.view_start_y, self.width+1, self.height+1, 9)
        pyxel.pix(self.x, self.y, 12)
        for b in self.bullets:
            b.draw()


    
    def move(self):
        is_slanting = False
        slanting_speed = 0.71
        is_slow = False

        if pyxel.btn(pyxel.KEY_LEFT_SHIFT):
            is_slow = True

        # 위쪽 또는 아래쪽과 왼쪽이나 오른쪽을 누를 때 이동량을 0.71 배하기
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)) and \
            (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN)):
            is_slanting = True

        if pyxel.btn(pyxel.KEY_RIGHT):
            Player.x += self.speed * (slanting_speed if is_slanting else 1) * (self.slow_speed if is_slow else 1)
        elif pyxel.btn(pyxel.KEY_LEFT):
            Player.x -= self.speed * (slanting_speed if is_slanting else 1) * (self.slow_speed if is_slow else 1)

        if pyxel.btn(pyxel.KEY_UP):
            Player.y -= self.speed * (slanting_speed if is_slanting else 1) * (self.slow_speed if is_slow else 1)
        elif pyxel.btn(pyxel.KEY_DOWN):
            Player.y += self.speed * (slanting_speed if is_slanting else 1) * (self.slow_speed if is_slow else 1)

        self.view_start_x = Player.x - self.width / 2
        self.view_start_y = Player.y - self.height / 2

        # 화면 밖으로 가지 않도록 이동 제한
        if self.view_start_x < 0:
            Player.x = self.width / 2
        elif self.view_start_x + self.width >= pyxel.width:
            Player.x = pyxel.width - self.width / 2 - 1

        if self.view_start_y < 0:
            Player.y = self.height / 2
        elif self.view_start_y + self.height >= pyxel.height:
            Player.y = pyxel.height - self.height / 2 - 1

        self.view_start_x = Player.x - self.width / 2
        self.view_start_y = Player.y - self.height / 2

    # 이 함수로 agent의 움직임을 가능케 한다.
    def move_by_action(self, action):
        
        # action == 0일때 >> 정지
        if action == 0: pass

        elif action == 1: # 위로 이동
            Player.y -= self.speed

        elif action == 2: # 아래로 이동
            Player.y += self.speed

        elif action == 3: # 왼쪽으로 이동
            Player.x -= self.speed

        else: # 오른쪽으로 이동
            Player.x += self.speed

        self.view_start_x = Player.x - self.width / 2
        self.view_start_y = Player.y - self.height / 2

        #화면은 밖으로 나가지 않게 하자.
        if self.view_start_x < 0:
            Player.x = self.width / 2
        elif self.view_start_x + self.width >= pyxel.width:
            Player.x = pyxel.width - self.width / 2 - 1

        if self.view_start_y < 0:
            Player.y = self.height / 2
        elif self.view_start_y + self.height >= pyxel.height:
            Player.y = pyxel.height - self.height / 2 - 1

        self.view_start_x = Player.x - self.width / 2
        self.view_start_y = Player.y - self.height / 2
    


    def shot(self, way, start_angle, delta_angle, speed, radius, color): 
        # 현재: shot(총알 수, -97.5: 시작되는 각도에서, 3 만큼씩 각도의 차이를 두며, 5의 속도로 공격, 1, 1)
        angle = start_angle
        _bullets = []
        for i in range(way):
            b = self.bullet_pool.get_bullet(radius, Player.x, Player.y, math.cos(math.radians(angle)),
                                            math.sin(math.radians(angle)), speed, color)
            angle += delta_angle
            if b:
                _bullets.append(b)
            else:
                for _b in _bullets:
                    _b.is_active = False
                break
        else:
            self.bullets.extend(_bullets)
