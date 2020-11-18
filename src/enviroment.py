from elements import *
import random

class Environment:
    def __init__(self, width, height, dirtiness, obstacles, children, robot_initializer):
        self.width = width
        self.height = height
        self.total = width * height
        self.matrix = {(i, j): None for i in range(height) for j in range(width)}
        self.robot = None 
        self.set_playpen(children)
        self.initialize(dirtiness, Dirty)
        self.initialize(obstacles, Obstacle)
        self.initialize(children, Child)
        self.initialize_robot(robot_initializer)

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key,value):
        self.matrix[key] = value

    def set_playpen(self, children):
        i = random.randint(0, self.height)
        j = random.randint(0, self.width)
        playpen = Playpen((i, j), self)
        self.matrix[(i, j)] = playpen
        amount = children - 1
        while amount:
            direction = random.randint(0,4)
            next = playpen.find_next_step(direction)
            if self.is_in(next) and not self.matrix[next]:
                playpen = Playpen(next, self)
                amount -= 1
            

    def initialize(self, percent, initializer):
        amount = self.total * percent / 100
        while amount:
            i = random.randint(0, self.height)
            j = random.randint(0, self.width)
            if not self.matrix[(i, j)]:
                self.matrix[(i, j)] = initializer((i,j),self)
                amount -= 1

    def initialize_robot(self, initializer):
        placed = False
        while not placed:
            i = random.randint(0, self.height)
            j = random.randint(0, self.width)
            if not self.matrix[(i, j)]:
                self.robot = initializer((i, j), self)
                placed = True

    def is_in(self, position):
        return position[0] >= 0 and position[0] < self.height and position[1] >= 0 and position[1] < self.width 

    def get_empty_spaces(self):
        return [pos for pos in self.matrix.keys() if not self.matrix[pos]]

    def get_dirty_spaces(self):
        return [pos for pos in self.matrix.keys() if type(self.matrix[pos]) is Dirty]

    def get_childs(self):
        return [pos for pos in self.matrix.keys() if type(self.matrix[pos]) is Child]

    def get_playpen(self):
        return [pos for pos in self.matrix.keys() if type(self.matrix[pos]) is Playpen]

    def is_playpen_full(self):
        playpen = [pos for pos in self.matrix.keys() if type(self.matrix[pos]) is Playpen]
        for pos in playpen:
            if not self.matrix[pos].child:
                return False
        return True

    def is_final_state(self):
        dirty_spaces = len(self.get_dirty_spaces())
        very_dirty = (dirty_spaces / self.total) > 0.6
        forever_clean = dirty_spaces == 0 and self.is_playpen_full()
        if very_dirty:
            return True, 0
        elif forever_clean:
            return True, 1
        return False, -1

    def get_square(self, i,j):
        squares = [(i,j)]
        pos = (i - 1, j - 1)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i - 1, j)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i - 1, j + 1)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i, j + 1)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i + 1, j + 1)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i + 1, j)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i + 1, j - 1)
        if self.is_in(pos):
            squares.append(pos)
        pos = (i, j - 1)
        if self.is_in(pos):
            squares.append(pos)
        return squares

    def apply_dirtiness(self):
        for pos in self.positions_to_dirty:
            if not self.matrix[pos]:
                self.matrix[pos] = Dirty(pos,self)

    def generate_dirtiness(self):
        self.positions_to_dirty = []
        for i in range(self.height):
            for j in range(self.width):
                square = self.get_square(i,j)
                childs = [pos for pos in square if type(self.matrix[pos]) is Child]
                if childs:
                    empty = [pos for pos in square if not type(self.matrix[pos])]
                    if len(childs) == 1:
                        cant = min(len(empty), random.randint(0,1))
                        self.positions_to_dirty += random.sample(empty,cant)
                    elif len(childs) == 2:
                        cant = min(len(empty), random.randint(0,3))
                        self.positions_to_dirty += random.sample(empty, cant)
                    else:
                        cant = min(len(empty), random.randint(0,6))
                        self.positions_to_dirty += random.sample(empty, cant)

    def random_change(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) != self.robot.pos:
                    element = self.matrix[(i, j)]
                    if element and type(element) is not Playpen:
                        while random.random() < 0.5:
                            direction = random.randint(0, 3)
                            next = element.find_next_step(direction)
                            if self.is_in(next) and not self.matrix[next]:
                                element.step(next)


    def natural_change(self):
        self.generate_dirtiness()
        childs = self.get_childs()
        for child in childs():
            child.move()
        self.apply_dirtiness()
    