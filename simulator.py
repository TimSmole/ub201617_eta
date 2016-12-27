# generate maze
import operator
from math import sqrt

from enum import Enum

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
    "set_flag_a()",
    "clear_flag_a()",
    "set_flag_b()",
    "clear_flag_b()",
    "mark_position()",
    "unmark_position()"
]
TESTS = [
    "getting_closer()",
    "can_move_forward",
    "can_move_backward",
    "marked_current",
    "marked_forward",
    "marked_backward",
    "flag_a",
    "flag_b",
    "random_choice()"
]


def get_parser():
    parse_dict = dict()

    for i, c in enumerate(CMDS):
        parse_dict[i] = "%s\n" % c

    i += 1
    for j, t in enumerate([ti for ti in itertools.product(TESTS, CMDS)]):
        parse_dict[i + j] = "if %s: %s\n" % (t[0], t[1])

    i = i + j + 1
    for j, t in enumerate([ti for ti in itertools.product(TESTS, CMDS)]):
        parse_dict[i + j] = "if not %s: %s\n" % (t[0], t[1])
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
    pd_inv = {replace_new_line(v): k for k, v in pd.items()}
    for i, line in enumerate(p):
        try:
            line = replace_new_line(line)
            v[i] = pd_inv[line]
        except:
            raise Exception("Illegal program")
    return v


def replace_new_line(s):
    s = s.replace("\n", "")
    s = s.replace("\r", "")
    return s


def vector_to_prog(v):
    try:
        return [pd[i] for i in v]
    except:
        raise Exception("Illegal vector")


pd = get_parser()


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def get_opposite(dir):
        """Returns opposite direction: UP->DOWN, DOWN->UP, ..."""
        return Direction._value2member_map_[tuple(map(lambda c: c * -1, dir.value))]


class Simulator:
    def __init__(self, input_maze, seed=0):
        # i: rows, j: columns
        self.start_i, self.start_j, self.end_i, self.end_j, self.maze = input_maze
        self.dim_i, self.dim_j = self.maze.shape

        # starting position (entrance of the labyrinth)
        self.move_counter = 0
        self.cur_dir = Direction.DOWN
        self.cur_i = self.start_i
        self.cur_j = self.start_j
        self.can_move_forward = True
        self.can_move_backward = False
        self.flag_a = self.flag_b = None
        self.marked_current = self.marked_backward = self.marked_forward = False
        self.prev_dist_to_goal = self.dist_to_goal()

        # Initialize random generator
        # a fixed random generator
        self.rand = random.Random(seed)

    def move(self, dir):
        """returns new coordinates of agent after moving in given direction """
        return tuple(map(operator.add, (self.cur_i, self.cur_j), dir.value))

    # Commands
    def move_forward(self):
        """Move forward"""
        if self.can_move_forward:
            self.cur_i, self.cur_j = self.move(self.cur_dir)
        self.update_move_counter()
        self.check_end()

    def move_backward(self):
        """Move backward"""
        if self.can_move_backward:
            self.cur_i, self.cur_j = self.move(Direction.get_opposite(self.cur_dir))
        self.update_move_counter()
        self.check_end()

    def turn_left(self):
        """change direction of agent"""
        self.cur_dir = Direction.LEFT
        self.update_move_counter()

    def turn_right(self):
        """change direction of agent"""
        self.cur_dir = Direction.RIGHT
        self.update_move_counter()

    def set_flag_a(self):
        self.flag_a = (self.cur_i, self.cur_j)
        self.update_move_counter()

    def clear_flag_a(self):
        self.flag_a = None
        self.update_move_counter()

    def set_flag_b(self):
        # TODO: WTF JE POINT?
        self.flag_b = (self.cur_i, self.cur_j)
        self.update_move_counter()

    def clear_flag_b(self):
        self.flag_b = None
        self.update_move_counter()

    def nop(self):
        pass
        # FIXME: update_move_counter ??

    def mark_position(self):
        """mark current position in maze"""
        self.maze[self.cur_i][self.cur_j] = -1
        self.update_move_counter()

    def unmark_position(self):
        """unmark current position in maze"""
        self.maze[self.cur_i][self.cur_j] = 0
        self.update_move_counter()

    def dist_to_goal(self):
        """return Euclidean distance from current position to goal"""
        cur_position = (self.cur_i, self.cur_j)
        goal_position = (self.dim_i, self.dim_j)
        return sqrt(sum([(x - y) ** 2 for x, y in zip(cur_position, goal_position)]))

    # TODO: add more commands

    def getting_closer(self):
        """check if agent was closer to goal before executing latest command"""
        return self.prev_dist_to_goal > self.dist_to_goal()

    def random_choice(self):
        """returns true of false"""
        return random.randint(0, 1)

    def update_move_counter(self):
        forward_coordinates = self.move(self.cur_dir)
        backward_coordinates = self.move(Direction.get_opposite(self.cur_dir))
        self.can_move_forward = self.check_can_move_to_coordinates(forward_coordinates)
        self.can_move_backward = self.check_can_move_to_coordinates(backward_coordinates)
        self.marked_current = self.maze[self.cur_i][self.cur_j] == -1
        self.marked_forward = self.maze[forward_coordinates[0]][forward_coordinates[1]] == -1
        self.marked_backward = self.maze[backward_coordinates[0]][backward_coordinates[1]] == -1
        self.prev_dist_to_goal = self.dist_to_goal()
        self.move_counter += 1

    def check_end(self):
        if self.cur_i == self.end_i and self.cur_j == self.end_j:
            raise FoundGoalException(0)

    def check_bounds(self, coordinates):
        """Checks if coordinates are valid coordinates for this maze"""
        return 0 <= coordinates[0] < self.dim_i and 0 <= coordinates[1] < self.dim_j

    def check_wall(self, coordinates):
        """Checks of coordinates represent wall or not"""
        return self.maze[coordinates[0]][coordinates[1]] != 1

    def check_can_move_to_coordinates(self, coordinates):
        """Check if agent can move to given coordinates"""
        return self.check_bounds(coordinates) and self.check_wall(coordinates)

    def fitness(self):
        return self.dist_to_goal() + 0.001 * self.move_counter


class FoundGoalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def simulate(input_maze, program, graphics=False, verbose=False, max_iter=100, max_len=100,
             delay=1.0, seed=0):
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

    prog = prog_to_executable(prog)  # add sim.

    try:
        one_step = compile("\n".join(prog) + "\n", "<string>", "exec")
    except:
        raise Exception("Compilation error")

    if graphics:
        import pylab as plt
        plt.ion()
        markers = {Direction.UP: '^', Direction.DOWN: 'v', Direction.LEFT: '<',
                   Direction.RIGHT: '>'}

    # run simulation
    for step in range(max_iter):
        try:
            exec (one_step)
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
            plt.plot(sim.marked_positions.T.nonzero()[0], sim.marked_positions.T.nonzero()[1], 'cs',
                     markersize=8.0, markerfacecolor="c")
            plt.plot(sim.cur_j, sim.cur_i, markers[sim.cur_dir], markersize=8.0,
                     markerfacecolor="g")
            if sim.flag_a:
                plt.plot(0, -1.2, 'go', markersize=8.0, markerfacecolor="g")
            if sim.flag_b:
                plt.plot(1, -1.2, 'bo', markersize=8.0, markerfacecolor="b")
            plt.draw()
            time.sleep(delay)
    if verbose:
        print("Iteration limit exceed: Failed to find path through maze. Fitness: ", sim.fitness())
    return sim.fitness()
