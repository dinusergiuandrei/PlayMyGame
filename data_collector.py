import time
from PIL import ImageGrab
from PIL import Image
from scipy import misc
import pickle
from ps4 import PS4Controller


def pickle_save(obj, p_path):
    with open(p_path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(p_path):
    with open(p_path, 'rb') as handle:
        pickle.load(handle)


def collect_data(total_frames=1000, buffer_size=100, rate=40):
    start_time = time.time()
    index = 0

    ps4 = PS4Controller()
    ps4.init()

    states = []

    for frame in range(total_frames):
        index += 1
        print(index)
        img = ImageGrab.grab()
        arr = misc.fromimage(img)
        (height, width, pixels) = arr.shape
        if height % rate != 0 or width % rate != 0:
            print("Incorrect rate. Screen height or weight not a multiple.")
        img.thumbnail((width // rate, height // rate), Image.ANTIALIAS)
        arr = misc.fromimage(img)
        ps4_state = ps4.get_state()
        states.append((arr, ps4_state))
        if index % buffer_size == 0:
            print(index)
            save_path = '../data/buf' + str(index // buffer_size) + ".pickle"
            pickle_save(states, save_path)
            states = []

    print("FPS: " + str(total_frames / (time.time() - start_time)))
