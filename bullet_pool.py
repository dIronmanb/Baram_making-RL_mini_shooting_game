import bullet

MAX_BULLET_NUM = 250 # 한 화면에서 나올 수 있는 Bullet은 250개


class EnemyBulletPool():
    """
    bass 탄막 개체 pool
    게임을 시작할 때 MAX_BULLET_NUM 개의 총알을 생성함, 이를 돌아가면서 사용
    """
    bullet_pool = [bullet.EnemyBullet(2, -1, -11, 0, 0, 0, 0) for i in range(MAX_BULLET_NUM)] #(탄막 반경, px,py, vx?, vy?, speed?, 색깔)
    max_bullet_num = MAX_BULLET_NUM
    

    def __init__(self):
        pass 

    @classmethod
    def get_bullet(cls, radius, x, y, movement_x, movement_y, speed, color):
        
        for i in range(MAX_BULLET_NUM):
            if not cls.bullet_pool[i].is_active:
                cls.bullet_pool[i].is_active = True
                cls.bullet_pool[i].count = 0
                cls.bullet_pool[i].radius = radius
                cls.bullet_pool[i].x = x
                cls.bullet_pool[i].y = y
                cls.bullet_pool[i].movement_x = movement_x
                cls.bullet_pool[i].movement_y = movement_y
                cls.bullet_pool[i].speed = speed
                cls.bullet_pool[i].color = color
                cls.bullet_pool[i].move_functions.clear()

                # 각 n번째 총알의 정보
                # 하지만 총알은 화면을 나가면 다시 갱신된다 >> 순서가 있는 총알은 중요치 않다.
                # 다만, 에이전트와 가까운 총알이 필요하다.
                # Qusetion: 총알 속도 및 방향이 수시로 변하는가? ...가속도 정보도 필요하려나? 속도가 매번 바뀔텐데 이를 근사하면 될 것 같은데...
                # if i == 0: print('--'*10)
                # print('{0}번째 총알 좌표:({1:.2f}, {2:.2f}), 속도:({3:.3f}, {4:.3f})'.format(i, cls.bullet_pool[i].x, cls.bullet_pool[i].y, cls.bullet_pool[i].movement_x, cls.bullet_pool[i].movement_y))
                
                return cls.bullet_pool[i]

        return None

    @classmethod
    def get_active_bullet_num(cls): # count, list를 리턴하는 것으로 수정
        active_list = []
        count = 0
        for i in range(cls.max_bullet_num):
            if cls.bullet_pool[i].is_active: #bullet이 활성화(화면에 노출)되어 있다면
                count += 1
                active_list.append(i)

        return count, active_list

    @classmethod
    def all_reset_bullet(cls):
        for b in cls.bullet_pool:
            b.is_active = False
            b.move_functions.clear()


class PlayerBulletPool():

    def __init__(self, max_bullet_num):
        self.max_bullet_num = max_bullet_num
        self.bullet_pool = []

        for i in range(max_bullet_num):
            self.bullet_pool.append(bullet.PlayerBullet(2, -1, -11, 0, 0, 0, 0))

    def get_bullet(self, radius, x, y, movement_x, movement_y, speed, color):
        for i in range(self.max_bullet_num):
            if not self.bullet_pool[i].is_active:
                self.bullet_pool[i].is_active = True
                self.bullet_pool[i].radius = radius
                self.bullet_pool[i].count = 0
                self.bullet_pool[i].x = x
                self.bullet_pool[i].y = y
                self.bullet_pool[i].movement_x = movement_x
                self.bullet_pool[i].movement_y = movement_y
                self.bullet_pool[i].speed = speed
                self.bullet_pool[i].color = color

                return self.bullet_pool[i]

        return None
