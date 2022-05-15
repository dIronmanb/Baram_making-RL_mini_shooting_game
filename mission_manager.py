from scene import Scene

class Mission():
    """
    미션 중의 클래스를 유지하고 관리, 기록 갱신 할 수 있음.
    score텍스트를 ','로 구분해보면:
    >> [미션, 클리어 횟수, 도전 횟수, Best Time]
    """

    def __init__(self, mission, best_time):
        
        self.record_time = 0
        
        self.mission = mission()
        self.best_time = best_time
        self.mission_number = int(''.join([ch for ch in self.mission.__class__.__name__[-2:] if ch.isdecimal()]))
        # 도전 횟수를 추가
        with open("score.txt", "rt") as f:
            record_list = f.readlines()
            new_record_list = record_list
        record = record_list[self.mission_number][:-1].split(",")
        new_record_list[self.mission_number] = "{0},{1},{2},{3}\n".format(record[0], record[1], str(int(record[2]) + 1),
                                                                          record[3])
        with open("score.txt", "wt") as f:
            f.writelines(new_record_list)

    def update(self):
        '''
        여기 업데이트에 dqn을 넣어야 한다....!!!
        state = self.mission.state
        # action = [0,1,2,3,4]
        agent = DQNAgent(state_size = 42, action_size = 5)
        action = agent.get_action(state)
        
        아....
        참 이상하게도
        
        self.mission의 attribute는 가져올 수 있는데
        method를 사용할 수 없다...하;;;

        '''

        self.mission.update()
        
        # if self.mission.count % 30 == 0:
        #    print("현재 상태: {0} \n현재 보상: {1} \n취한 행동: {2} \n다음 상태: {3} \n끝났는가?: {4}\n".format(\
        #       self.mission.agent.state, self.mission.agent.reward, self.mission.agent.action, self.mission.agent.next_state, self.mission.agent.done))

        if self.mission.return_value["status"] == "clear":
            print("현재 상태: {0} \n현재 보상: {1} \n취한 행동: {2} \n다음 상태: {3} \n끝났는가?: {4}\n".format(\
                self.mission.agent.state, self.mission.agent.reward, self.mission.agent.action, self.mission.agent.next_state, self.mission.agent.done))

            # 클리어 횟수를 추가
            with open("score.txt", "rt") as f:
                record_list = f.readlines()
                new_record_list = record_list
            record = record_list[self.mission_number][:-1].split(",")
            
            # 최고 기록 또는 첫 클리어 Best_Time 업데이트

            # # 현재 클리어한 시간을 가져옴
            # print("진행된 시간값: {}".format(self.mission.return_value))

            # # self.record_time에 기록된 시간 가져오고 print로 확인하기
            # self.record_time = self.mission.return_value['time']
            # print('가져온 시간값: {}'.format(self.record_time))
            
            if self.best_time > self.mission.return_value["time"] or self.best_time == 0:
                new_record_list[self.mission_number] = "{0},{1},{2},{3}\n".format(record[0], str(int(record[1]) + 1),
                                                                                  record[2],
                                                                                  self.mission.return_value["time"])
            else:
                new_record_list[self.mission_number] = "{0},{1},{2},{3}\n".format(record[0], str(int(record[1]) + 1),
                                                                                  record[2],
                                                                                  record[3])
            with open("score.txt", "wt") as f:
                f.writelines(new_record_list)

            return Scene.MISSION_SELECT, self.mission_number

        if self.mission.return_value["status"] == "exit": # 'exit'는 게임오버와 바로 직결
            # # 게임 오버시: return_value = {'status':'exit', 'time':count}
            # print("진행된 시간값: {}".format(self.mission.return_value))
            
            # # self.record_time에 기록된 시간 가져오고 print로 확인하기
            # self.record_time = self.mission.return_value['time']
            # print('가져온 시간값: {}'.format(self.record_time))

            return Scene.MISSION_SELECT, self.mission_number


        return Scene.NO_SCENE_CHANGE, 0



    def draw(self):
        self.mission.draw()
