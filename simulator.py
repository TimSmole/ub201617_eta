# generate maze
import numpy as np
import time
import random
import itertools
import os
import sys

# legal commands and tests
# students can (and should) add additional moves and tests
CMDS = [
    "nop()",
    "move_forward()",
    "move_backward()",
    "turn_left()",
    "turn_right()",
    "set_flag()",
    "clear_flag()",
    "mark_position()",
    "unmark_position()"
]
TESTS = [
    "getting_closer()",
    "can_move_forward",
    "can_move_backward",
    "marked",
    "flag_a"
]

def get_parser():
    parse_dict = dict()

    for i, c in enumerate(CMDS):
        parse_dict[i] = "%s\n" % c

    i += 1
    for j, t in enumerate([ti for ti in itertools.product(TESTS, CMDS)]):
        parse_dict[i+j] = "if %s: %s\n" % (t[0], t[1])

    i = i + j + 1
    for j, t in enumerate([ti for ti in itertools.product(TESTS, CMDS)]):
        parse_dict[i+j] = "if not %s: %s\n" % (t[0], t[1])
    return parse_dict

def prog_to_executable(p):
    out = []
    for l in p:
        for r in CMDS + TESTS:
            l = l.replace(' ' + r, " sim." + r)
            if l.startswith(r):
                l = 'sim.' + r + l[len(r):]
        out.append(l)
    return out

def prog_to_vector(p):
    v = np.zeros((len(p),), dtype=int)
    pd_inv = {v: k for k, v in pd.items()}
    for i, line in enumerate(p):
        try:
            v[i] = pd_inv[line]
        except:
            raise Exception("Illegal program")
    return v

def vector_to_prog(v):
    try:
        return [pd[i] for i in v]
    except:
        raise Exception("Illegal vector")

pd = get_parser()


class Simulator:

    def __init__(self, input_maze, seed=0):
        # i: rows, j: columns
        self.start_i, self.start_j, self.end_i, self.end_j, self.maze = input_maze
        self.dim_i, self.dim_j = self.maze.shape

        # starting position (entrance of the labyrinth)
        self.move_counter = 0
        self.cur_dir = 'down'
        self.cur_i = self.start_i
        self.cur_j = self.start_j
        self.can_move_forward = True
        self.can_move_backward = self.flag_a = False
        self.prev_dist_to_goal = self.dist_to_goal()

        # Initialize random generator
        # a fixed random generator
        self.rand = random.Random(seed)

    # Commands
    def move_forward(self):
        # TO-DO: move forward
        self.update_move_counter()
        self.check_end()

    def move_backward(self):
        # TO-DO: move backward
        self.update_move_counter()
        self.check_end()

    def turn_left(self):
        # TO-DO: turn left
        self.update_move_counter()

    def turn_right(self):
        # TO-DO: turn right
        self.update_move_counter()

    def set_flag(self):
        # TO-DO: set flag A
        self.update_move_counter()

    def clear_flag(self):
        # TO-DO: clear flag A
        self.update_move_counter()

    def nop(self):
        pass

    def mark_position(self):
        # TO-DO: mark position
        self.update_move_counter()

    def unmark_position(self):
        # TO-DO: clear position
        self.update_move_counter()

    def dist_to_goal(self):
        # TO-DO: return Euclidean distance from current position to goal
        return -1

    # TODO: add more commands

    def update_move_counter(self):
        self.move_counter += 1

    def check_end(self):
        if self.cur_i == self.end_i and self.cur_j == self.end_j:
            raise FoundGoalException(0)

    def fitness(self):
        return self.dist_to_goal() + 0.001*self.move_counter

class FoundGoalException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def simulate(input_maze, program, graphics=False, verbose=False, max_iter=100, max_len=100, delay=1.0, seed=0):
    '''
        program can be a path to file, string or vector
        return fitness value
    '''
    sim = Simulator(input_maze, seed)

    if isinstance(program, str):
        if os.path.exists(program):
            prog = open(program).readlines()
        else:
            prog = program
            prog = map(lambda x: x + '\n', filter(None, prog.split('\n')))
    else:
        prog = vector_to_prog(program)

    v = prog_to_vector(prog)
    if len(v) > max_len:
        raise Exception("Illegal program length")

    prog = prog_to_executable(prog) #add sim.

    try:
        one_step = compile("\n".join(prog)+"\n", "<string>", "exec")
    except:
        raise Exception("Compilation error")

    if graphics:
        import pylab as plt
        plt.ion()
        markers = {'up': '^', 'down': 'v', 'left': '<', 'right': '>'}

    # run simulation
    for step in range(max_iter):
        try:
            exec(one_step)
            if verbose:
                sys.stdout.write("Distance: %f\r" % (sim.dist_to_goal()))
                sys.stdout.flush()
        except FoundGoalException:
            if verbose:
                print("Home. Fitness value:", sim.fitness())
            return sim.fitness()
        if graphics:
            plt.clf()
            plt.imshow(sim.maze, cmap=plt.cm.binary, interpolation='nearest')
            plt.plot(sim.marked_positions.T.nonzero()[0], sim.marked_positions.T.nonzero()[1], 'cs', markersize=8.0, markerfacecolor="c")
            plt.plot(sim.cur_j, sim.cur_i, markers[sim.cur_dir], markersize=8.0, markerfacecolor="g")
            if sim.flag_a:
                plt.plot(0, -1.2, 'go', markersize=8.0, markerfacecolor="g")
            if sim.flag_b:
                plt.plot(1, -1.2, 'bo', markersize=8.0, markerfacecolor="b")
            plt.draw()
            time.sleep(delay)
    if verbose:
        print("Iteration limit exceed: Failed to find path through maze. Fitness: ", sim.fitness())
    return sim.fitness()

