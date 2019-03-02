from ps4 import PS4Controller
from pynput.keyboard import Key, Controller
from time import sleep


def pick(value, a, b):
    if value < 0:
        return a
    return b


def get_keyboard_key(controller_button, value):
    keys = [
        pick(value, 'a', 'd'),  # 0, Lx
        pick(value, 'f', 'e'),  # 1, Ly
        pick(value, 'q', 'e'),  # 2, Rx
        None,                   # 3, Ry
        'o',                    # 4, Sq
        None,                   # 5, X
        'l',                    # 6, O
        'c',                    # 7, Tr
        Key.shift_l,            # 8 L1
        'p',                    # 9 R1
        's',                    # 10 L2
        'w',                    # 11 R2
        Key.tab,                # 12 Select
        Key.esc,                # 13 Start
        Key.backspace,          # 14 L3
        None,                   # 15 R3
        None,                   # 16 PS
        None                    # 17 Touch
    ]
    if 0 <= controller_button <= 17:
        return keys[controller_button]
    print(controller_button)
    return None


def press(controller_state, p_dead_zone):
    l_keyboard = Controller()
    l_ps4 = PS4Controller()
    for n in range(len(l_ps4.state_names)):
        if abs(controller_state[n]) > p_dead_zone:
            k = get_keyboard_key(n, controller_state[n])
            if k is not None:
                l_keyboard.press(k)


def release(controller_state, p_dead_zone):
    l_keyboard = Controller()
    l_ps4 = PS4Controller()
    for n in range(len(l_ps4.state_names)):
        if abs(controller_state[n]) > p_dead_zone:
            k = get_keyboard_key(n, controller_state[n])
            if k is not None:
                l_keyboard.release(k)


if __name__ == "__main__":
    keyboard = Controller()
    ps4 = PS4Controller()
    ps4.init()
    dead_zone = 0.25
    # ps4.listen()
    while True:
        state = ps4.get_state()
        press(state, dead_zone)
        sleep(0.1)
