import random

N = 0
E = 1
S = 2
W = 3
STAY = 4

class Element:
    def __init__(self, pos, environment):
        self.pos = pos
        self.environment = environment

    def find_next_step(self, direction):
        if direction == N:
            return (self.pos[0] - 1, self.pos[1])
        elif direction == E:
            return (self.pos[0], self.pos[1] + 1)
        elif direction == S:
            return (self.pos[0] + 1, self.pos[1])
        elif direction == W:
            return (self.pos[0], self.pos[1] - 1)

    def step(self, next):
        self.environment[self.pos] = None
        self.pos = next
        self.environment[next] = self
        return True

class Dirty(Element):
    pass

class Playpen(Element):
    def __init__(self, pos, environment):
        Element.__init__(self, pos, environment)
        self.child = False

class Child(Element):
    def move(self):
        direction = random.randint(0, 4)
        if direction != STAY:
            next = self.find_next_step(direction)
            if self.environment.is_in(next) and next != self.environment.robot.pos:
                element = self.environment[next]
                if type(element) is Obstacle and element.move(direction):
                    self.step(next)
                elif element is None:
                    self.step(next)

class Obstacle(Element):
    def move(self, direction):
        next = self.find_next_step(direction)
        if self.environment.is_in(next):
            element = self.environment[next]

            if type(element) is Obstacle:
                return element.move(direction) and self.step(next)
            elif element is None:
                return self.step(next)
            return False

        return False


class Robot(Element):
    def __init__(self, pos, environment):
        Element.__init__(self, pos, environment)
        self.child = False

    def bfs(self):
        d = {(i, j): None for i in range(self.environment.height) for j in range(self.environment.width)}
        pi = {(i, j): None for i in range(self.environment.height) for j in range(self.environment.width)}
        d[self.pos] = 0
        q = [self.pos]
        while q:
            u = q[0]
            for direction in range(0, 4):
                v = self.find_next_step(direction)
                if self.environment.is_in(v) and not d[v] and type(self.environment[v]) is not Obstacle:
                    element = self.environment[v]
                    d[v] = d[u] + 1
                    pi[v] = u
                    on_child_no_pass = self.environment.robot.child and (type(element) is Child or (type(element) is Playpen and element.child))
                    if not on_child_no_pass:
                        q.append(v)
                        
        return d,pi

    def get_path(self, pi, v):
        path = []
        while pi[v]:
            path.insert(0, pi[v])
            v = pi[v]
        return path
            
    def find_near_element(self, d, elements):
        min = self.environment.height * self.environment.width
        element = None
        for e in elements:
            if d[e.pos] < min:
                min = d[e.pos]
                element = e
        return element


    def move(self):
        pass

class ChildsFirstRobot(Robot):     
    def move(self):
        d, pi = self.bfs()
        dirty_spaces = len(self.environment.get_dirty_spaces())
        dirty_percent = dirty_spaces / self.environment.total
        if dirty_percent > 0.5:
            if self.child:
                if not self.environment[self.pos]:
                    self.child = False
                    self.environment[self.pos] = Child(self.pos, self.environment)
                else:
                    playpens = self.environment.get_playpen()
                    empty_playpens = [ p for p in playpens if not p.child]
                    near_playpen = self.find_near_element(d, empty_playpens)
                    path = self.get_path(pi, near_playpen.pos)
                    next = path[1] if len(path) > 1 else path[0] 
                    self.pos = next
                    if type(self.environment[next]) is Playpen and not self.environment[next].child:
                        self.child = False
                        self.environment[next].child = True
            else:
                dirties = self.environment.get_dirty_spaces()
                near_dirty = self.find_near_element(d, dirties)
                path = self.get_path(pi, near_dirty.pos)
                next = path[0]
                self.pos = next
        else:
            if self.child:
                playpens = self.environment.get_playpen()
                empty_playpens = [ p for p in playpens if not p.child]
                near_playpen = self.find_near_element(d, empty_playpens)
                path = self.get_path(pi, near_playpen.pos)
                next = path[1] if len(path) > 1 else path[0] 
                self.pos = next
                if type(self.environment[next]) is Playpen and not self.environment[next].child:
                    self.child = False
                    self.environment[next].child = True
            else:
                childs = self.environment.get_childs()
                if childs:
                    near_child = self.find_near_element(d, childs)
                    path = self.get_path(pi, near_child.pos)
                    next = path[0]
                    self.pos = next
                    if type(self.environment[next]) is Child:
                        self.child = True
                        self.environment[next] = None
                elif type(self.environment[self.pos]) is Dirty:
                    self.environment[self.pos] = None
                else:
                    dirties = self.environment.get_dirty_spaces()
                    near_dirty = self.find_near_element(d, dirties)
                    path = self.get_path(pi, near_dirty.pos)
                    next = path[0]
                    self.pos = next

class NearFirstRobot(Robot):
    def move(self):
        d, pi = self.bfs()
        if self.child:
            playpens = self.environment.get_playpen()
            empty_playpens = [ p for p in playpens if not p.child]
            near_playpen = self.find_near_element(d, empty_playpens)
            path = self.get_path(pi, near_playpen.pos)
            next = path[1] if len(path) > 1 else path[0] 
            self.pos = next
            if type(self.environment[next]) is Playpen and not self.environment[next].child:
                self.child = False
                self.environment[next].child = True
        elif type(self.environment[self.pos]) is Dirty:
            self.environment[self.pos] = None
        else:
            elements = self.environment.get_dirty_spaces() + self.environment.get_childs()
            near_element = self.find_near_element(d, elements)
            path = self.get_path(pi, near_element.pos)
            next = path[0]
            self.pos = next
            if type(self.environment[next]) is Child:
                self.child = True
                self.environment[next] = None            

    
        
