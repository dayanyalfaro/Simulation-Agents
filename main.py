from enviroment import *
import random

DIRTINESS_UP_60_PERCENT = 0
CHILDREN_UNDER_CONTROL_CLEAN_HOUSE = 1
TIME_OVER = 2

class Simulation:
    def __init__(self):
        self.environment = None
        self.interval = None

    def run(self):
        times = 0
        while True:
            is_final_state, state = self.environment.is_final_state()
            if is_final_state:
                self.terminate(state)
                break
            elif times == 100 * self.interval:
                self.terminate(2)
                break
            else:
                self.environment.robot.move()
                self.environment.natural_change()
                if not times % self.interval:
                    self.environment.random_change()

    def terminate(self, state):
        pass


