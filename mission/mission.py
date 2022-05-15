
# from tensorflow import keras
# import tensorflow as tf

import pyxel
import player
from scene import Scene
import bullet_pool


import os
import Episodes as ep
import sys
import numpy as np
from dqn import DQNAgent #얘를 직접 넣어야 하는데...

import math

checkpoint_path = "/Users/lolli/Desktop/mini_shooting/Weights/Mini_Shooting_light_2" #끝단에 있는 게 이름
# checkpoint_dir = os.path.dirname(checkpoint_path) # Create a callback that saves the models's weights


class Mission():

    def __init__(self):

        self.agent = DQNAgent(state_size = (ep.NUM_OF_BULLETS + 1)* 4 , action_size = 5) #DQN를 init으로 하나 생성!
        self.interval = 0
        '''
        load할 수 있도록 구현하기
        가중치 일정 주기마다 save하기
        '''



        self.player = player.Player(pyxel.width / 2, 200, 10, 10, 1, 2) # (self, x, y, width, height, collision_radius, speed):
        
        self.enemy_max_hp = self.enemy.hp
        self.enemy_pre_hp = self.enemy_max_hp
        self.enemy_after_hp = self.enemy_max_hp

        self.return_value = {"status": Scene.NO_SCENE_CHANGE}
        
        self.is_clear = False
        self.agent.done = False

        self.after_clear_time = 0 #굳이 "clear!!"했다고 안 알려줘도 된다! 이전꺼로 복구하려면 mini_shooting(0)보기 >> 현재 이 필드를 사용하는 곳이 있으니 일단 요렇게!
        self.count = 0
        self.bullet_pool = bullet_pool.EnemyBulletPool

        self.limited_bullets = ep.NUM_OF_BULLETS # range에 따라 탄막의 개수 조절
        self.wanted_bullets = np.array([])

        self.relative_position_x, self.relative_position_y = self.player.x - self.enemy.x, self.player.y - self.enemy.y
        # return으로 만들기가 복잡할 수도 있다. 걍 self로 받아오기
        self.state, self.emeny_reward = [0] * ((self.limited_bullets + 1)* 4 ), 10
        #위에: 상태, 시간 보상, 적 보스 체력 깎일 때 보상, 클리어 보상, 죽음 보상
        
        # self.relation_bullet_agent = []

    def update(self): # DQN.py에서 액션을 업데이트한다. 여기서 action은 0 ~ 5

        self.relative_position_x, self.relative_position_y = self.player.x - self.enemy.x, self.player.y - self.enemy.y
        pre_x, pre_y = self.relative_position_x, self.relative_position_y
        
        ep.BOUNDARY = abs(self.player.y - self.enemy.y)

        '''After action, get reward and next state'''
        if not self.is_clear: #클리어하지 않았을 때
            self.count += 1
            self.enemy.update()
            self.collision_detection() #여기서 보스의 체력이 깎였는지를 확인함.

            self.relative_position_x, self.relative_position_y = self.player.x - self.enemy.x, self.player.y - self.enemy.y
            next_x, next_y = self.relative_position_x, self.relative_position_y
            
            if self.enemy_pre_hp > self.enemy_after_hp:
                self.enemy_pre_hp = self.enemy_after_hp               
                self.state = [self.player.x, self.player.y, self.relative_position_x, self.relative_position_y]+ self.wanted_bullets.tolist() if len(self.wanted_bullets) == 4 * self.limited_bullets\
                 else [self.player.x, self.player.y, self.relative_position_x, self.relative_position_y] + [0] * (4*self.limited_bullets)
                self.agent.reward = +40
                
                if abs(pre_x) + abs(pre_y) > abs(next_x) + abs(next_y):
                    self.agent.reward += 90
                else:
                    self.agent.reward -= 90
                    
                if abs(self.player.y - self.enemy.y) < 60:
                    self.agent.reward -= 120
                
                
            else:
            # '''현재 state를 에이전트의 위치만 뽑아왔는데, (이것 말고도 boss의 위치 및 속도), 탄막들의 상대위치 및 상대속도도 필요함.'''
            # if self.count % 10 == 0:
            # print("계속 진행 중\n",[self.player.x, self.player.y] + self.wanted_bullets.tolist())
                self.state = [self.player.x, self.player.y, self.relative_position_x, self.relative_position_y]+ self.wanted_bullets.tolist() if len(self.wanted_bullets) == 4 * self.limited_bullets\
                     else [self.player.x, self.player.y, self.relative_position_x, self.relative_position_y] + [0]*(4*self.limited_bullets)
                self.agent.reward = -(1/1000000 * self.count**2)
                
                if abs(pre_x) + abs(pre_y) > abs(next_x) + abs(next_y):
                    self.agent.reward += 90
                    
                else:
                    self.agent.reward -= 90
                    
                if abs(self.player.y - self.enemy.y) < 60:
                    self.agent.reward -= 120
 


        else: #현재 클리어 했다는 의미
            
            self.relative_position_x, self.relative_position_y = self.player.x - self.enemy.x, self.player.y - self.enemy.y
            next_x, next_y = self.relative_position_x, self.relative_position_y
            
            self.bullet_pool.all_reset_bullet()
            self.return_value["status"] = "clear"
            self.return_value["time"] = self.count
            print("clear!")
            
            # print("성공!!\n",[self.player.x, self.player.y] + self.wanted_bullets.tolist())
            self.state = [self.player.x, self.player.y, self.relative_position_x, self.relative_position_y] + self.wanted_bullets.tolist() if len(self.wanted_bullets) == 4 * self.limited_bullets\
                 else [self.player.x, self.player.y, self.relative_position_x, self.relative_position_y] + [0]*(4*self.limited_bullets)
            self.agent.reward = +20000000
            
            
        '''Take Action'''
        self.state = np.array([self.state])
        self.agent.state = self.state
         
        self.agent.action = self.agent.get_action(self.state) #현재 action을 취하기
        self.player.update(self.agent.action)
    
        
        '''state다시 정렬하는 곳'''
        self.state = np.reshape(np.array(self.state, dtype = float), [1, (self.limited_bullets + 1)* 4])
        self.state = self.state.tolist()
        self.agent.next_state = self.state

        '''여기서부터 Agent Training'''
        # 학습된 모델로 진행
        if ep.TRAINED_MODEL:
            pass
        
        
        # 모델을 학습하는 거로!
        else:
            if ep.EPISODES < 6:

                if not self.agent.done:
                    self.agent.append_sample() #현재 있는 agent의 모든 것들을 replay에 저장
                    

                    if len(ep.MEMORY) >= ep.TRAIN_START:
                        self.agent.train_model()
                    

                    ep.SCORE += self.agent.reward
                    ep.cnt += 1
                    
                    if ep.cnt == 500:
                        ep.cnt = 0
                        self.agent.model.save_weights(ep.save_wight_file)
                        print("Model Saved!!(Cnt ==  {0})".format(ep.cnt))
                        
                    # self.agent.state = self.agent.next_state
                    '''
                    episodes는 Mission 실행할 때마다 초기화 된다 
                    따라서. Mission객체에 두지 말고
                    임의의 .py에 전역변수 하나를 설정하여 이를 늘리는 방식으로 하는 것이 더 낫다.
                    '''
                else: # self.agent.done is True:
                    ep.EPISODES += 1
                    self.agent.append_sample()
                    
                    print("{} Episode".format(ep.EPISODES))
                    print("Score:{}".format(ep.SCORE))
                    
                    ep.SCORE = 0
                    self.agent.update_target_model()

                    # self.agent.model.save_weights(ep.save_wight_file)
                    # print("Saved!!")
                    # if os.path.isdir("/Users/lolli/Desktop/mini_shooting/Weights"):
                    #    os.chdir("/Users/lolli/Desktop/mini_shooting/Weights")
                    #    self.agent.model.save_weights("Mini_Shooting_"+str(ep.EPISODES)+".h5")
                    #    print("Saved in 'Weight' directory") 
                    #    os.chdir("/Users/lolli/Desktop/mini_shooting")
                    
                    # self.agent.model.save_weights("Mini_Shooting_"+str(ep.EPISODES)+".h5")
                    # print("Saved!!")
                
            else: ep.EPISODES = 0
        

        if pyxel.btn(pyxel.KEY_Q) and not self.is_clear: # KEY_Q를 누르면 시간 정보 추가
            print("자동함수 해제!")
            ep.FLAG = not ep.FLAG
            
            
            self.bullet_pool.all_reset_bullet()
            self.return_value["status"] = "exit"
            # 시간에 대한 정보 추가
            self.return_value["time"] = self.count
        
    
        '''
            self.count의 time interval를 적절히 정해야한다.
            가아끔...
            input_dim = 2인 게 만들어진다.
        '''

        # active한 총알 수: MAX_BULLETS(250) - active_bullets를 리턴함

        
        _, active_list = self.bullet_pool.get_active_bullet_num()
        # cnt_in_boundary = 0 # 범위 내 탄막 개수
        bullets = []
        bullets_temp = []
        # self.wanted_bullets = None #???
        # print(nums, active_list)

        
        for i in active_list:
        # 탄막들의 위치 및 속도 구하는 코드
        #  print('{0}번째 총알 좌표:({1:.2f}, {2:.2f}), 속도:({3:.3f}, {4:.3f})'.format(i, self.bullet_pool.bullet_pool[i].x, \
        #      self.bullet_pool.bullet_pool[i].y, self.bullet_pool.bullet_pool[i].movement_x, self.bullet_pool.bullet_pool[i].movement_y))

        # 에이전트 반경 내에 있는 탄막들이 몇 개 있는지를 구하는 코드           
            norm_1x, norm_1y = (self.player.x - self.bullet_pool.bullet_pool[i].x), (self.player.y - self.bullet_pool.bullet_pool[i].y)
            

            # norm1 = abs(norm_1x) + abs(norm_1y)
            norm_2 = math.sqrt((norm_1x) ** 2 + (norm_1y) ** 2)


            if norm_2 < ep.bullet_distance:  # boundary는 바꾸어보기 for optimal reusult
                
                bullets.append([norm_2, norm_1x, norm_1y, self.bullet_pool.bullet_pool[i].movement_x, \
                    self.bullet_pool.bullet_pool[i].movement_y]) # norm, 상대거리x, 상대거리y, 탄막속도x, 탄막속도y
                
                # print('(범위 내)에이전트와 {}번째 총알 간 상대 위치: ({:.2f},{:.2f})'.format(i, norm_1x, norm_1y))
            

        bullets = sorted(bullets, key = lambda x : x[0]) # 현재 최소 거리부터를 정렬
        bullets = [i[1:] for i in bullets] # norm(거리를 재기 위한 도구)는 제거
        
        ################ ----------------------------- #####################
        #pre_bullet_set = [bullets[0 + i*4 : 1 + i*4] for i in range(10)]
        #next_bullet_set = pre_
        
            
        zero_list = [[0] * 4 for _ in range(self.limited_bullets - len(bullets))] #총알 개수가 n(현재 10)보다 작으면 나머지는 0으로 채우기
        bullets = bullets[:self.limited_bullets] if len(bullets) > self.limited_bullets else bullets + zero_list
        bullets = bullets[:self.limited_bullets] # 0 ~ 10개까지 가져오기
            
        '''
            if len(bullets) > self.limited_bullets:
            bullets = bullets[:self.limited_bullets]
            else:
            zero_list = [[0] * 4 for _ in range(self.limited_bullets - len(bullets))]
            bullets + zero_list
        '''
        for i in bullets:
            bullets_temp.extend(i) # 1,2,3,4 = px, py, vx, vy >> 2차원을 1차원으로 flatten 
            self.wanted_bullets = np.array(bullets_temp).round(3)

        # print(self.wanted_bullets[:10])
        # '''
        # 현재 bullets의 모습은 다음과 같다
        # bullets = [[1,2,3,4], [1,2,3,4], ...]
        # Qusetion1: 이를 풀어낼까, 아님 그대로 쓸까?
        # Qusetion2: 위치 데이터, 속도 데이터의 크기가 다르다. 위치 데이터와 속도 데이터를 정규화하는게 좋지 않을까??
        # '''


        # print('에이전트 좌표: ({:.2f},{:.2f}) / 범위 내 탄막 개수: {} / time = {}'.format(self.player.x, self.player.y, cnt_in_boundary, self.count // 100)) 
            
        # 화면에 있는 탄막들의 좌표만 취하고 싶은데...
        # if self.count % 100 == 0:
        #     cnt = 0
        #     for i in active_list:
        #         print('{0}번째 총알 좌표:({1:.2f}, {2:.2f}), 속도:({3:.3f}, {4:.3f})'.format(i, self.bullet_pool.bullet_pool.x, i.y, i.movement_x, i.movement_y))
        #         cnt += 1



    def draw(self):
        self.player.draw()
        if not self.is_clear:
            self.enemy.draw()
            for bit in self.enemy.bits:
                bit.shot_position.draw()

            pyxel.line(50, 5, 130 * self.enemy.hp / self.enemy_max_hp + 50, 5, 13)

        pyxel.text(5, 5, "TIME:" + str(self.count), 13)
        if self.is_clear:
            pass
            '''
            self.after_claer_time이 쓰일까??
            if self.after_clear_time % 30 < 15:
                pyxel.text(85, pyxel.height / 2, "Clear!", 14)
            else:
                pyxel.text(85, pyxel.height / 2, "Clear!", 15)
            '''

    def enemy_playerbullet_detection(self):
        x1 = self.enemy.view_start_x
        y1 = self.enemy.view_start_y
        x2 = self.enemy.view_start_x + self.enemy.width
        y2 = self.enemy.view_start_y + self.enemy.height
        for player_bullet in self.player.bullets:
            x = player_bullet.x
            y = player_bullet.y
            r = player_bullet.collision_radius

            C1 = x > x1 and x < x2 and y > y1 - r and y < y2 + r
            C2 = x > x1 - r and x < x2 + r and y > y1 and y < y2
            C3 = (x1 - x) ** 2 + (y1 - y) ** 2 < r ** 2
            C4 = (x2 - x) ** 2 + (y1 - y) ** 2 < r ** 2
            C5 = (x2 - x) ** 2 + (y2 - y) ** 2 < r ** 2
            C6 = (x1 - x) ** 2 + (y2 - y) ** 2 < r ** 2

            if C1 or C2 or C3 or C4 or C5 or C6:
                self.enemy.hp -= ep.EMENY_HP_DECREASE #계속 적의 HP를 깎는 행위
                #이때에도 보상을 허락하도록 하자.
                self.enemy_after_hp = self.enemy.hp
                # print("HIT! HIT! HIT! HIT! HIT!")
                self.state, self.agent.reward = [self.player.x, self.player.y, self.player.x - self.enemy.x, self.player.y - self.enemy.y] + self.wanted_bullets.tolist(), 10
                self.agent.next_state = self.state
                if self.enemy.hp <= 0:
                    self.mission_clear()
                player_bullet.is_active = False

    def bit_playerbullet_detection(self):
        for bit in self.enemy.bits:
            x1 = bit.view_start_x
            y1 = bit.view_start_y
            x2 = bit.view_start_x + bit.width
            y2 = bit.view_start_y + bit.height
            for player_bullet in self.player.bullets:
                x = player_bullet.x
                y = player_bullet.y
                r = player_bullet.collision_radius

                C1 = x > x1 and x < x2 and y > y1 - r and y < y2 + r
                C2 = x > x1 - r and x < x2 + r and y > y1 and y < y2
                C3 = (x1 - x) ** 2 + (y1 - y) ** 2 < r ** 2
                C4 = (x2 - x) ** 2 + (y1 - y) ** 2 < r ** 2
                C5 = (x2 - x) ** 2 + (y2 - y) ** 2 < r ** 2
                C6 = (x1 - x) ** 2 + (y2 - y) ** 2 < r ** 2

                if (C1 or C2 or C3 or C4 or C5 or C6) and bit.is_active:
                    bit.hp -= 1
                    if bit.hp <= 0:
                        bit.is_active = False
                    player_bullet.is_active = False

    def player_enemybullet_detection(self):
        player_x = self.player.x
        player_y = self.player.y
        player_r = self.player.collision_radius
        for shot_position in self.enemy.shot_positions:
            for enemy_bullet in shot_position.bullets:
                x = enemy_bullet.x
                y = enemy_bullet.y
                r = enemy_bullet.collision_radius
                if (player_x - x) ** 2 + (player_y - y) ** 2 <= (player_r + r) ** 2:
                    enemy_bullet.is_active = False
                    return True
        return False

    def player_bitbullet_detection(self):
        player_x = self.player.x
        player_y = self.player.y
        player_r = self.player.collision_radius
        for bit in self.enemy.bits:
            for bit_bullet in bit.shot_position.bullets:
                x = bit_bullet.x
                y = bit_bullet.y
                r = bit_bullet.collision_radius
                if (player_x - x) ** 2 + (player_y - y) ** 2 <= (player_r + r) ** 2:
                    bit_bullet.is_active = False
                    return True
        return False

    def collision_detection(self):
        self.enemy_playerbullet_detection()
        self.bit_playerbullet_detection()
        #현재 탄막이 내게 닿았는가를 판단
        if self.player_enemybullet_detection() or self.player_bitbullet_detection():
            self.bullet_pool.all_reset_bullet()
            self.return_value["status"] = "exit"
            self.return_value["time"] = self.count #이걸로 게임 오버가 되었을 떄도 시간 가져올 수 있다.

            self.agent.done = True
            # print("사망 플래그 뜸\n",[self.player.x, self.player.y] + self.wanted_bullets.tolist())
            my_and_boss_info = [self.player.x, self.player.y, self.player.x - self.enemy.x, self.player.y - self.enemy.y]
            
            self.state = my_and_boss_info + self.wanted_bullets.tolist() if len(self.wanted_bullets) == 4 * self.limited_bullets\
                 else [self.player.x, self.player.y] + [0]*(4*self.limited_bullets)
            self.agent.reward = -10000000
            print("Died..")


    def mission_clear(self):
        self.is_clear = True
        self.agent.done = True




