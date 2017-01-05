from random import randint

import os
import numpy as np
import itertools
import mazes
from simulator import simulate


class Agent:
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
        "unmark_position()",
        "go_to_flag_a()",
        "go_to_flag_b()"
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
    parser = None

    def __init__(self, vector):
        self.vector = vector
        self.fitness = None

    def to_vector(self):
        return self.vector

    def to_program(self):
        return Agent.vector_to_program(self.vector)

    def to_executable(self):
        return Agent.program_to_executable(Agent.vector_to_program(self.vector))

    def compute_fitness(self):
        """Simulate and visualize some mazes.
         The function simulate can operate on files, programs or vectors.
         If you have problems with visualization (i.e. are a Mac user),
         try running the script from the terminal instead of PyCharm."""
        af = 0
        for m in mazes.mazes_train:
            af += simulate(m, self, verbose=False, graphics=False, delay=0.1, max_iter=500)
        self.fitness = af / len(mazes.mazes_train)
        return self.fitness

    @staticmethod
    def generate_random(agent_size):
        vector = [randint(0, len(Agent.get_parser()) - 1) for _ in range(agent_size)]
        return Agent(vector)

    @staticmethod
    def generate_from_file_or_string(program):
        if isinstance(program, str):
            if os.path.exists(program):
                program = open(program).readlines()
            else:
                program = map(lambda x: x + '\n', filter(None, program.split('\n')))
        elif not isinstance(program, list):
            raise Exception("Argument must be filename or list of strings!")
        return Agent(Agent.program_to_vector(program))

    @staticmethod
    def get_parser():
        if Agent.parser is not None:
            return Agent.parser
        parse_dict = dict()

        for i, c in enumerate(Agent.CMDS):
            parse_dict[i] = "%s\n" % c

        i += 1
        for j, t in enumerate([ti for ti in itertools.product(Agent.TESTS, Agent.CMDS)]):
            parse_dict[i + j] = "if %s: %s\n" % (t[0], t[1])

        i = i + j + 1
        for j, t in enumerate([ti for ti in itertools.product(Agent.TESTS, Agent.CMDS)]):
            parse_dict[i + j] = "if not %s: %s\n" % (t[0], t[1])
        Agent.parser = parse_dict
        return Agent.parser

    @staticmethod
    def program_to_executable(p):
        out = []
        for l in p:
            for r in Agent.CMDS + Agent.TESTS:
                l = l.replace(' ' + r, " sim." + r)
                if l.startswith(r):
                    l = 'sim.' + r + l[len(r):]
            out.append(l)
        return out

    @staticmethod
    def program_to_vector(p):
        """
        Convert program to vector. Use vectors when performing searching, genetic algorithms, etc.
        vector is a list of command numbers 0-227.
        The command will fail for illegal programs."""
        v = np.zeros((len(p),), dtype=int)
        pd_inv = {Agent.replace_new_line(v): k for k, v in Agent.get_parser().items()}
        for i, line in enumerate(p):
            try:
                line = Agent.replace_new_line(line)
                v[i] = pd_inv[line]
            except:
                raise Exception("Illegal program")
        return v

    @staticmethod
    def replace_new_line(s):
        s = s.replace("\n", "")
        s = s.replace("\r", "")
        return s

    @staticmethod
    def vector_to_program(v):
        """
        You can convert vectors back to programs to manually examine solutions.
        The command will fail for illegal vectors."""
        try:
            return [Agent.get_parser()[i] for i in v]
        except:
            raise Exception("Illegal vector")
