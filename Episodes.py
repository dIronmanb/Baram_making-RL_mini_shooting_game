from collections import deque
import os
import tensorflow as tf
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.optimizers import Adam

FLAG = False

NUM_OF_BULLETS = 10

IS_LOADED = True
TRAINED_MODEL = True # true이면 load파일만 사용, false면 학습하는 걸로!
load_wight_file = "/Users/lolli/Desktop/mini_shooting/Weights/Mini_Shooting_light_10_25_25_25_5(0)"
save_wight_file = "/Users/lolli/Desktop/mini_shooting/Weights/Mini_Shooting_light_10_25_25_25_5(0)"

bullet_distance = 120
# Mission 2 >> 120 10_25_25_25_5(0)
# Mission 8 >>  70 15_28_28_28_5(1)

EMENY_HP_DECREASE = 4.0

EPISODES = 0
SCORE = 0
cnt = 0

DISCOUNT_FACTOR = 0.999
LEARNING_RATE = 0.0005

EPSILON = 1.0
EPSILON_DECAY = 0.9995
EPSILON_MIN = 0.01


TRAIN_START = 1000
MEMORY = deque(maxlen = 2000)

BOUNDARY = 0.0
MAX_BOUNDARY = 100


#################################################################

# 파일 이름에 에포크 번호를 포함시킵니다(`str.format` 포맷)
checkpoint_path = "/Users/lolli/Desktop/mini_shooting/Weights"
checkpoint_dir = os.path.dirname(checkpoint_path)

# 다섯 번째 에포크마다 가중치를 저장하기 위한 콜백을 만듭니다
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=True

)

#################################################################