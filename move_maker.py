import pickle

import numpy as np
import tensorflow as tf
from PIL import ImageGrab, Image
from keras.engine.saving import load_model
from pynput.keyboard import Controller
from scipy import misc
from tensorflow import keras

from rocket_league_action import get_keyboard_key

data_path = 'data/buf1.pickle'
model_path = 'models/model'
weights_path = 'models/weights'

with open(data_path, 'rb') as handle:
    states = pickle.load(handle)

images_list = []
ps4_list = []

for state in states:
    arr = state[0]
    ps4_state = state[1]
    shape = arr.shape

    for i in range(4):
        ps4_state[i] = (ps4_state[i] + 1) / 2

    images_list.append(arr)
    ps4_list.append(ps4_state)

images = np.asarray(images_list)
ps4 = np.asarray(ps4_list)

images = images / 255


def get_model(height, width):
    l_model = keras.Sequential([
        keras.layers.Flatten(input_shape=(height, width, 3)),
        keras.layers.Dense(72, activation=tf.nn.relu),
        keras.layers.Dense(18, activation=tf.nn.softmax)
    ])
    # optimizer = 'rmsprop'
    l_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['acc'])
    return l_model


def train_and_save_model(rate=40):
    img = ImageGrab.grab()
    img_matrix = misc.fromimage(img)
    (height, width, pixels) = img_matrix.shape
    if height % rate != 0 or width % rate != 0:
        print("Incorrect rate. Screen height or weight not a multiple.")

    h = height//rate
    w = width//rate
    l_model = get_model(h, w)

    l_model.fit(images, ps4, validation_data=(images, ps4), epochs=8, batch_size=16)

    l_model.save(model_path)
    l_model.save_weights(weights_path)


def load():
    l_model = load_model(model_path)
    l_model.load_weights(weights_path)
    return l_model


def play(rate=40):
    img = ImageGrab.grab()
    img_matrix = misc.fromimage(img)
    (height, width, pixels) = img_matrix.shape
    if height % rate != 0 or width % rate != 0:
        print("Incorrect rate. Screen height or weight not a multiple.")

    h = height // rate
    w = width // rate
    l_model = load()

    while True:
        img = ImageGrab.grab()
        img.thumbnail((w, h), Image.ANTIALIAS)
        img_matrix = misc.fromimage(img)
        img_matrix = (np.expand_dims(img_matrix, 0))
        prediction = l_model.predict(img_matrix)[0]
        for j in range(4):
            prediction[j] = prediction[j] * 2 - 1
        prediction[10] = prediction[10] * 2 - 1
        prediction[11] = prediction[11] * 2 - 1
        prediction[-1] = 0
        prediction[-2] = 0
        prediction[-5] = 0
        prediction[-6] = 0
        # press(prediction, 0.5)
        k = np.argmax(prediction)
        keyboard = Controller()
        keyboard.press(get_keyboard_key(k, prediction[k]))
        # sleep(0.1)
        keyboard.release(get_keyboard_key(k, prediction[k]))


