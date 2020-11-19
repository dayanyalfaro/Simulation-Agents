from enviroment import *
from elements import *
import random

DIRTINESS_UP_60_PERCENT = 0
CHILDREN_UNDER_CONTROL_CLEAN_HOUSE = 1
TIME_OVER = 2

class Simulation:
    def __init__(self, width, height, dirtiness, obstacles, children, interval, robot_init):
        self.environment = Environment(width, height, dirtiness, obstacles, children, robot_init)
        self.interval = interval

    def run(self):
        times = 1
        while True:
            print('Turno', times)
            print(s.environment)
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
                    print('RANDOM CHANGE')
                    self.environment.random_change()
            times += 1

    def terminate(self, state):
        print('State', state)


s = Simulation(width = 10, height = 10, dirtiness = 20, obstacles = 20, children = 10, interval = 5, robot_init = NearFirstRobot)
s.run()