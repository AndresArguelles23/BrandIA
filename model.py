from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.regularizers import L1L2
from constants import LENGTH_KEYPOINTS, MAX_LENGTH_FRAMES

NUM_EPOCH = 200

def get_model(output_length: int):
    model = Sequential()
    model.add(LSTM(256, return_sequences=True, activation='tanh', input_shape=(MAX_LENGTH_FRAMES, LENGTH_KEYPOINTS)))
    model.add(LSTM(512, return_sequences=True, activation='tanh'))
    model.add(LSTM(256, return_sequences=False, activation='tanh'))
    model.add(Dense(256, activation='tanh', kernel_regularizer=L1L2(l1=0.001, l2=0.001)))
    model.add(Dense(128, activation='tanh', kernel_regularizer=L1L2(l1=0.001, l2=0.001)))
    model.add(Dense(output_length, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model
