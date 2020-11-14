import random

class Environment:
    def __init__(self, width, height, dirtiness, obstacles, children, robot_initializer):
        self.width = width
        self.height = height
        self.total = width * height
        self.matrix = {(i, j): None for i in range(height) for j in range(width)}
        self.set_playpen(children)
        self.initialize(dirtiness, Dirty)
        self.initialize(obstacles, Obstacle)
        self.initialize(children, Child)
        self.initialize_robot(robot_initializer)

    def set_playpen(self, children):
        pass

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
                self.matrix[(i, j)] = initializer((i, j), self)
                placed = True

    def get_empty_spaces(self):
        return [pos for pos in self.matrix.keys() if not self.matrix[pos]]

    def get_dirty_spaces(self):
        return [pos for pos in self.matrix.keys() if type(self.matrix[pos]) is Dirty]

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
        return very_dirty or forever_clean


class Element:
    def __init__(self, pos, environment):
        self.pos = pos
        self.environment = environment

class Playpen(Element):
    def __init__(self, pos, environment):
        Element.__init__(self, pos, environment)
        self.child = False

class Child(Element):
    pass

class Obstacle(Element):
    pass

class Dirty(Element):
    pass

class Robot(Element):
    pass
        
    