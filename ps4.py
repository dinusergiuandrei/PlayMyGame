import os
import pprint
import pygame
from time import sleep


class PS4Controller(object):
    dead_zone = 0.25

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    state_names = ["Lx", "Ly", "Rx", "Ry", "Sq", "X", "O", "Tr", "L1", "R1", "L2", "R2", "Select", "Start", "L3", "R3",
                   "PS", "Touch"]
    button_names = ["Sq", "X", "O", "Tr", "L1", "R1", "L2", "R2", "Select", "Start", "L3", "R3", "PS", "Touch"]
    axis_names = ["Lx", "Ly", "Rx", "Ry", "R2", "L2"]

    def init(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def get_state(self):
        if not self.axis_data:
            self.axis_data = {}
            for i in range(len(self.axis_names)):
                self.axis_data[i] = 0.0

        if not self.button_data:
            self.button_data = {}
            for i in range(len(self.button_names)):
                self.button_data[i] = False

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                val = event.value
                if event.axis == 4 or event.axis == 5:
                    self.axis_data[event.axis] = round((val + 1) / 2, 2)
                    self.button_data[11 - event.axis] = self.axis_data[event.axis]
                else:
                    self.axis_data[event.axis] = round(val, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = 1.0
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = 0.0
            # pprint.pprint(self.axis_data)
            # pprint.pprint(self.button_data)

        # result = {}
        # result.update(self.axis_data)
        # for b in range(len(self.button_names)):
        #     result[b + 4] = self.button_data[b]
        #
        result = []
        for a in range(4):
            result.append(self.axis_data[a])
        for bn in range(len(self.button_names)):
            result.append(self.button_data[bn])
        return result


# demo
if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    dead_zone = 0.25
    # ps4.listen()
    while True:
        state = ps4.get_state()

        s = ""
        for b in range(len(ps4.state_names)):
            if abs(state[b]) > dead_zone:
                if b >= 4:
                    s += ps4.state_names[b] + ", "
                else:
                    s += ps4.state_names[b] + ":" + str(state[b]) + "; "
        if len(s) > 0:
            print(s)
