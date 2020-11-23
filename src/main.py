from enviroment import *
from elements import *
import random

DIRTINESS_UP_60_PERCENT = 0
CHILDREN_UNDER_CONTROL_CLEAN_HOUSE = 1
TIME_OVER = 2

output_fd = open('output.txt', 'w')

class Simulation:
    def __init__(self, width, height, dirtiness, obstacles, children, interval, id):
        self.interval = interval
        self.width = width
        self.height = height
        self.dirtiness = dirtiness
        self.obstacles = obstacles
        self.children = children
        self.id = id
        self.fired = 0
        self.clean = 0
        self.time_out = 0
        self.dirty_mean = []

    def describe(self):
        output_fd.write(f'Environment {self.id}\n width:{self.width} --- height:{self.height} --- dirtiness:{self.dirtiness} --- obstacles:{self.obstacles} --- children:{self.children} --- interval:{self.interval}\n')
        
    def restart(self):
        self.fired = 0
        self.clean = 0
        self.time_out = 0
        self.dirty_mean = []        

    def run(self, robot_init):
        self.environment = Environment(self.width, self.height, self.dirtiness, self.obstacles, self.children)
        self.environment.initialize_robot(robot_init)
        times = 1
        while True:
            print('Turno', times)
            print(self.environment)
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
        if state == DIRTINESS_UP_60_PERCENT:
            self.fired += 1
        elif state == CHILDREN_UNDER_CONTROL_CLEAN_HOUSE:
            self.clean += 1
        elif state == TIME_OVER:
            self.time_out += 1
        self.dirty_mean.append(sum(self.environment.dirty_count)/len(self.environment.dirty_count))

    def report_results(self):
        output_fd.write(f'Success: {self.clean}\n')
        output_fd.write(f'Fired: {self.fired}\n')
        output_fd.write(f'Timeout: {self.time_out}\n')
        output_fd.write(f'Dirty Mean: {sum(self.dirty_mean)/len(self.dirty_mean)}\n')
        output_fd.write('\n')

environments = [Simulation(width=10, height=10, dirtiness=30, obstacles=20, children=6, interval=10, id = 1),
                Simulation(width=7, height=8, dirtiness=20, obstacles=10, children=3, interval=5, id = 2),
                Simulation(width=7, height=8, dirtiness=20, obstacles=10, children=4, interval=20, id = 3),
                Simulation(width=15, height=15, dirtiness=20, obstacles=20, children=10, interval=50, id = 4),
                Simulation(width=5, height=5, dirtiness=10, obstacles=5, children=2, interval=5, id = 5),
                Simulation(width=10, height=5, dirtiness=30, obstacles=20, children=4, interval=10, id = 6),
                Simulation(width=10, height=10, dirtiness=40, obstacles=10, children=6, interval=20, id = 7),
                Simulation(width=10, height=10, dirtiness=10, obstacles=40, children=7, interval=30, id = 8),
                Simulation(width=9, height=9, dirtiness=30, obstacles=20, children=4, interval=20, id = 9),
                Simulation(width=10, height=10, dirtiness=20, obstacles=20, children=5, interval=20, id=10)
                ]


output_fd.write(f'------------------------------------------------------------------------\n')
output_fd.write(f'Robot: ChildsFirstRobot\n')
output_fd.write(f'------------------------------------------------------------------------\n')
for e in environments:
    e.describe()
    for i in range(30):
        e.run(ChildsFirstRobot)
    e.report_results()
    e.restart()

output_fd.write(f'------------------------------------------------------------------------\n')
output_fd.write(f'Robot: NearFirstRobot\n')
output_fd.write(f'------------------------------------------------------------------------\n')
for e in environments:
    e.describe()
    for i in range(30):
        e.run(NearFirstRobot)
    e.report_results()
    e.restart()
    