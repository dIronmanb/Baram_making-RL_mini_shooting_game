# DQN Algorithm

# from mission.mission import Mission # for setting environment
import random
import numpy as np
from collections import deque

# from keras.models import Sequential
# from keras.layers import Dense
# from keras.optimizers import Adam

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# from keras.layers import Dense
# from keras.optimizer_v2.adam import Adam
# from keras.models import Sequential


import os
import Episodes as ep #여기에도 전역변수를 넣어 학습이 진행된 신경망을 넣기 위해서
'''
아래쪽에 이제 해야할 것들 살펴보기
'''


EPISODES = 25

class DQNAgent:
    def __init__(self, state_size, action_size):
        '''self.render = False'''
        self.load_model = ep.IS_LOADED

        # 상태와 행동의 크기 정의
        self.state_size = state_size
        self.action_size = action_size
        
        

        # 아예 DQNAgnet에 현 상태, 다음 상태, 보상, 행동 정의
        self.state = None
        self.next_state = None
        self.reward = None
        self.action = None
        self.done = False

        # DQN 하이퍼파라미터
        self.discount_factor = 0.999
        self.learning_rate = 0.0005
        
        print("------------------------ 현재 엡실론의 값: {0} ---------------------------".format(ep.EPSILON))
        print("DEQUE값:",len(ep.MEMORY))
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.batch_size = 64 # Original Batch Size = 64
        
        self.train_start = 500  #train 시작 지점
        self.memory = deque(maxlen = 1000) # 리플레이 메모리, 최대 크기 2000
       

        # 모델과 타깃 모델 생성
        self.model = self.build_model()
        self.target_model = self.model

        # 타깃 모델 초기화
        self.update_target_model()


        if self.load_model:
            self.model.load_weights(ep.load_wight_file)
            self.model.summary()
            print("Successfully Loaded!")
            
            # if os.path.isdir("/Users/lolli/Desktop/mini_shooting/Weights"):
            #   print("Weights 디렉토리에서 신경망 불어오기")
            #    os.chdir("/Users/lolli/Desktop/mini_shooting/Weights")
            #   self.model.load_weights("Mini_Shooting_"+str(ep.EPISODES-1)+".h5")
            #  os.chdir("/Users/lolli/Desktop/mini_shooting")

        #현재 업데이트한 모델을 타겟 모델로 지정
        self.target_model = self.model
         

    # 상태가 입력, 큐함수가 출력인 인공신경망 생성
    def build_model(self):
        model = Sequential()
        model.add(Dense(25, input_dim=self.state_size, activation='relu',
                        kernel_initializer='he_uniform'))
        model.add(Dense(25, activation='relu',
                        kernel_initializer='he_uniform'))
        model.add(Dense(25, activation='relu',
                        kernel_initializer='he_uniform'))
        model.add(Dense(self.action_size, activation='linear',
                        kernel_initializer='he_uniform'))
        model.summary()
        # model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate)) adam어디감ㅁㅋㅋ
        model.compile(loss='mse', optimizer=Adam(learning_rate = ep.LEARNING_RATE))
        return model

    # 타깃 모델을 모델의 가중치로 업데이트
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    # 입실론 탐욕 정책으로 행동 선택
    def get_action(self, state):
        # 여기서 state_size 및 state는 아래 docstring에서 참고
        # 여기서는 정책을 업데이트하는 것이다. 최적의 정책이 나와서 그것을 따를 때, '행동'이라고 부른다.
        self.state = state.reshape(1, (ep.NUM_OF_BULLETS + 1 )* 4)
        
        # 학습된 모델로 진행하기
        if ep.TRAINED_MODEL:
            
            
            if np.random.rand() <= 0.0 : #self.epsilon:
                
                result = random.randrange(self.action_size) # 5개의 행동 중 하나
                
                if ep.BOUNDARY < ep.MAX_BOUNDARY and result == 1:
                    return 2
                return result
                
            else:
                #print(state.shape)
                q_value = self.model.predict(state)
                result =  np.argmax(q_value[0])
                
                if ep.BOUNDARY < ep.MAX_BOUNDARY and result == 1:
                    return 2
                return result
            

        # 모델 학습하는 중
        else:
            if np.random.rand() <= ep.EPSILON : #self.epsilon:
                result = random.randrange(self.action_size) # 5개의 행동 중 하나
                
                if ep.BOUNDARY < ep.MAX_BOUNDARY and result == 1:
                    return 2
                return result
            
            else:
                # print(state.shape)
                q_value = self.model.predict(state)
                result = np.argmax(q_value[0])
                
                if ep.BOUNDARY < ep.MAX_BOUNDARY and result == 1:
                    return 2
                return result


    # 샘플 <s, a, r, s'>을 리플레이 메모리에 저장
    def append_sample(self):
        # self.memory.append((self.state, self.action, self.reward, self.next_state, self.done))
        ep.MEMORY.append((self.state, self.action, self.reward, self.next_state, self.done))

    # 리플레이 메모리에서 무작위로 추출한 배치로 모델 학습
    def train_model(self):
        if ep.EPSILON > ep.EPSILON_MIN: #self.epsilon > self.epsilon_min:
            ep.EPSILON *= ep.EPSILON_DECAY #self.epsilon *= self.epsilon_decay

        # 메모리에서 배치 크기만큼 무작위로 샘플 추출
        mini_batch = random.sample(ep.MEMORY, self.batch_size) #(self.memory, self.batch_size)
        

        states = np.zeros((self.batch_size, self.state_size))
        next_states = np.zeros((self.batch_size, self.state_size))
        actions, rewards, dones = [], [], []       

        for i in range(self.batch_size):
        
            states[i] = mini_batch[i][0][0]
            actions.append(mini_batch[i][1])
            rewards.append(mini_batch[i][2])
            next_states[i] = mini_batch[i][3][0]
            dones.append(mini_batch[i][4])

        # 현재 상태에 대한 모델의 큐함수
        # 다음 상태에 대한 타깃 모델의 큐함수
        target = self.model.predict(states)
        target_val = self.target_model.predict(next_states)

        # 벨만 최적 방정식을 이용한 업데이트 타깃
        for i in range(self.batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                target[i][actions[i]] = rewards[i] + self.discount_factor * (
                    np.amax(target_val[i]))

        self.model.fit(states, target, batch_size=self.batch_size,
                        epochs=1  ,verbose=0)
            
        



# # =========================
# if __name__ == '__main__':
#     env = Mission() #환경을 Misson()으로 받을 예정
    
#     # action 정의하기
#     '''
#      현재 내가 만드는 DQN에서는 리스트마다 각각을 행동하도록 해야 한다.
#      0 - 정지
#      1 - 상
#      2 - 하
#      3 - 좌
#      4 - 우
#      이 코드는 에이전트가 움직이게 하는 함수에서 구현해야 한다.
#      뭔가 부드러운 움직임을 기대하기는 어렵다.
#      상하좌우에 따른 움직임을 고려하자.
    
#     '''
#     action = [0,1,2,3,4]

#     # state 받아오기
#     state = env.state
    
    

#     state_size = 42 # 2 + 4*self.limited_bullets
#     action_size = 5 # actions

#     agent = DQNAgent(state_size, action_size) # 에이전트 클래스 가져오기, 인자에는 상태 사이즈, 행동 사이즈 넣기

#     '''
#      상태는 다음과 같다. 
#      1. 에이전트 위치
#      2. 에이전트 주변 탄막(10 ~ 15)의 상대위치
#      3. 에이전트 주변 탄막(10 ~ 15)의 상대속도
#      4. 보스와의 거리?도 필요하면 넣고

#      행동
#      1. ['up', 'down', 'left','right','stop']
#      2. 공격은 항상 할테니까 리스트에서 제외
#      3. 슬로우?는 구현하기 어려워서 제외

#      현재까지 된 것들
#      - 에이전트 현 위치
#      - 에이전트와 탄막 간에 상대위치, 상대속도
#      - 종료되는 시간
#      - action을 dpn.py에서 호출하여 state, reward, done을 반환하는 것

#      나머지 더 해봐야 하는 것들
#      - 상태 개수 및 어떻게 상태를 넘겨주는지: Agent_x, Agent_y, bullets_info(px,py,vx,vy) >> 총 2 + 4*self.limited_bullets 개( 2 + 4*10 = 42 )
#      - 행동 개수 및 어떻게 행동을 넘겨주는지: 
    
#     '''

#     # 에이전트가 현재 상황에서 액션을 취하고
#     action = agent.get_action(state)

#     env.update(action) #action을 취하고 다음 상태, 보상, clear했는지를 가져옴
#     next_state, reward, done = env.state, env.reward, env.is_clear #update를 하고 다음것들을 가져오는 것이므로, clear의 했는지를 판단할 수 있다!

# # ========================= #

#     # DQN 에이전트 생성
#     agent = DQNAgent(state_size, action_size)

#     scores, episodes = [], []

#     for e in range(EPISODES):

#         '''지금 글은 쓴 이 부분에는 계속 게임을 자동적으로 시행하는 코드가 있어야 함.'''
#         done = False
#         score = 0

#         # env 초기화
#         '''
#          내 게임에서는 env를 어떻게 초기화할까...
#          초기화하다 == 게임을 처음부터 다시 시작하다.
#          게임을 다시 시작하도록 한다면....? 굳이 다른 것들까지 초기화할 필요 X
#         '''
#         state = env.reset()
#         state = np.reshape(state, [1, state_size])  #이게 왜 필요하지??

        # while not done:
        #     '''
        #     if agent.render:
        #          env.render()
        #     '''

        #     # 현재 상태로 행동을 선택
        #     action = agent.get_action(state)
        #     # 선택한 행동으로 환경에서 한 타임스텝 진행
        #     env.update(action)
        #     next_state, reward, done = env.state, env.reward, env.is_clear

        #     next_state = np.reshape(next_state, [1, state_size]) #이게 왜 필요하지??
            
            
            
        #     # 에피소드가 중간에 끝나면 -100 보상
        #     '''
        #      이건 어떻게 할까...
        #      에피소드가 중간에 끝나게 되면 다시 시작을 해야한다...!
        #      그렇게 된다면 이전 행동해서 얻은 rewards + 죽은 것에 대한 reward
        #      종료해야 되는 거 아닌가?
        #      여기서는
        #      done이 되는 경우가
        #       >> 게임이 아예 clear되었을 때
        #       >> 정말로 도중에 끝났을 때
        #     '''
        #     reward = reward if not done or score == 499 else -100

        #     # 리플레이 메모리에 샘플 <s, a, r, s'> 저장
        #     agent.append_sample(state, action, reward, next_state, done)

        #     # samples가 1000개 이상이 되면 학습 ㄱㄱ
        #     if len(agent.memory) >= agent.train_start:
        #         agent.train_model()

            
        #     score += reward #reward는 계속 더해진다.
        #     state = next_state

        #     if done:
        #         # 각 에피소드마다 타깃 모델을 모델의 가중치로 업데이트
        #         agent.update_target_model()

        #         '''내가 정한 score가 있으므로 바로 적용하기에는 문제가 있다.'''
        #         score = score if score == 500 else score + 100 #???

        #         # 에피소드마다 학습 결과 출력
        #         scores.append(score)
        #         episodes.append(e)
        #         pylab.plot(episodes, scores, 'b')
        #         pylab.savefig("./save_graph/cartpole_dqn.png")
        #         print("episode:", e, "  score:", score, "  memory length:",
        #               len(agent.memory), "  epsilon:", agent.epsilon)

        #         # 이전 10개 에피소드의 점수 평균이 490보다 크면 학습 중단
        #         '''이것 역시 문제가 있다. 점수를 다시 바꾸고, 수시로 저장하도록 하자.'''
        #         if np.mean(scores[-min(10, len(scores)):]) > 490:
        #             agent.model.save_weights("./save_model/cartpole_dqn.h5")
        #             sys.exit()
        



# '''
# dqn과 이 게임을 연결해서 어떻게 학습을 시킬 것인가...

# 1. 현 게임에 dqn을 넣는다.



# 2. dqn에 현 게임을 넣는다.

# 현재 env에 Mission을 받았음
#  - 이 Mission object를 받는 부분이 있나?

 
# '''



'''
DONE
- 현재 DQN을 Mission에 넣음으로써 무작위 행동까지는 구현함.
- 무작위 행동에 따른 다음 행동과 보상이 나온다. 이때 그냥 계속 보상을 -1로만 주면 학습이 진행되지 않을 수도 있다.
    따라서, 보스의 체력을 값을 때, 양의 보상을 받도록 한다.


MUST
- 현재 DQN내부에 아예 state, next_state, action, reward, done을 넣었다.
    이를 deque에 넣고 어느 정도 채워지면 학습 ㄱㄱ 
    매번 학습된 신경망을 저장해야 한다.
    이를 불러와야 한다.

- 

- 자동 학습을 해야 한다. 




'''