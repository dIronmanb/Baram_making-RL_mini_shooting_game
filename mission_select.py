import pyxel
from scene import Scene
import missions
import Episodes as ep
import time

class MissionSelect():

    def __init__(self, cursor_position):
        self.cursor = cursor_position
        self.missions = ["mission" + i for i in missions.missions.keys()]
        self.mission_recode = [i for i in open("score.txt").readlines()]
        self.recode_list = ["0", "0", "0", "0"]
        self.menu_item = ["MissionSelect", "Quit"]
        self.is_active = True

    def update(self):
        # 커서가 요소 외부를 표시하지 않도록 제한
        if pyxel.btnp(pyxel.KEY_UP, 30, 20):
            self.cursor = max(1, self.cursor - 1)
        elif pyxel.btnp(pyxel.KEY_DOWN, 30, 20):
            self.cursor = min(len(self.missions), self.cursor + 1)

        self.recode_list = self.mission_recode[self.cursor].split(",")

        '''여기서! 어떤 미션을 수행할 건지가 결정된다.'''
        if pyxel.btnp(pyxel.KEY_Z, 10, 10):
            # print("You pressed key_z!") # Mission Select에서 눌려짐!
            for mission_number in range(1, len(self.missions) + 1):
                if self.cursor == mission_number:
                    return Scene.MISSION, mission_number, int(self.recode_list[3])

        if pyxel.btn(pyxel.KEY_X):
            # print("You pressed key_x!")
            return Scene.MENU, 0
        
        # 자동함수 >> 토글 스위치
        if pyxel.btn(pyxel.KEY_1):
            if not ep.FLAG:
                print("자동 함수 작동!")
                ep.FLAG = not ep.FLAG
                time.sleep(0.6)
                
            else:
                print("자동함수 해제!")
                ep.FLAG = not ep.FLAG
                time.sleep(0.6)
                
        if ep.FLAG:
            for mission_number in range(1, len(self.missions) + 1):
               if self.cursor == mission_number:
                    return Scene.MISSION, mission_number, int(self.recode_list[3])
            
            

        return Scene.NO_SCENE_CHANGE, 0

    def draw(self):
        pyxel.text(10, 120, self.menu_item[0], 8)
        pyxel.text(10, 140, self.menu_item[1], 5)

        for i in range(0, len(self.missions)):
            if i+1 == self.cursor:
                pyxel.text(67, 120, self.missions[i], 8)
            elif i+1 > self.cursor:
                pyxel.text(67 + abs(self.cursor - i-1) ** 1.1 * 5,
                           120 - (self.cursor - i) * 10 + 20, self.missions[i], 5)
            else:
                pyxel.text(67 + abs(self.cursor - i-1) ** 1.1 * 5,
                           120 - (self.cursor - i) * 10 + 10, self.missions[i], 5)

        recode_text = "HISTORY:{0}/{1} BESTTIME:{2}".format(self.recode_list[1], self.recode_list[2], self.recode_list[3])
        pyxel.text(67, 130, recode_text, 5)
