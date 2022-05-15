import pyxel
import scene_manager
import time
import os

'''
현재 에이전트를 위한 환경을 구성하기 위해서 다음 정보들이 필요하다.
1. 한 에피소드가 진행된 시간
    mission_manager.py >> mission.py >> "return_value['time'] = self.count"


2. 현 상태 >> return_value['status'] 에서 상태를 확인할 수 있음.
+ 참고용 + 1초동안의 60개 이미지: 가져와서 어느 time_interval이 지나야 각각 이미지가 구분이 가능한지.

찬혁 선배의 말을 따르면(탄막은 가장 가까운 1개부터 시작)
3. 각 탄막의 위치[px,py] >> bulleet_pool.py >> get_active_bullet_num코드 수정 >> mission에서 현 화면에서 보이는 탄막들 위치 보임
4. 각 탄막의 속도[vx,vy] >> 3에 의해서 속도 역시 가져올 수 있음. 이때 속도가 변하기 하지만 미분가능하게 변하는 것은 아님.
    어느 미션에서는 불연속적으로 속도가 변함. time_step의 너비를 좁게 해야 학습할 수 있지 않을까 싶음.
5. 에이전트 위치[px,py] >> player.py >> class Player >> Player.x, Player.y


Q: DQN에 넘기는 건: 3.4.5정보들 Qusetion: fps = 60인데 이를 모두 가져와야 하나?
A: 일단 self.count % 10 == 0등을 이용하여 굳이 1초에 60개 모두 가져올 필요는 없을 듯


pyxel.btn(pyxel.KEY_LEFT_SHIFT) >> 왼쪽 방향키를 누르면 True리턴

- 자동 공격: player.py >> class Player >> def update() >> shot()
- 
'''


class App:
    def __init__(self):
        pyxel.init(width=189, height=252, caption="shooting", fps=30, border_width=0)
        self.one_second_count = 0
        self.fps_base_time = time.time()
        self.fps = 0
        self.scene_manager = scene_manager.SceneManager()

         # 기록용 파일이 없으면 시작할 때 작성 - 점수와 Best타임 저장
        if not os.path.exists("score.txt"):
            with open("score.txt", "wt") as f:
                for mission_number in range(0, 21):
                    f.writelines(str(mission_number) + "," + "0" + "," + "0" + "," + "0" + "\n")

        pyxel.run(self.update, self.draw)

    def update(self):
        self.one_second_count += 1
        self.scene_manager.update()

        now = time.time()
        if now - self.fps_base_time >= 1:
            self.fps = self.one_second_count / (now - self.fps_base_time)
            self.fps_base_time = now
            self.one_second_count = 0

    def draw(self):
        pyxel.cls(7)
        self.scene_manager.draw()
        pyxel.text(173, 246, str(self.fps)[:4], 3)


App()
