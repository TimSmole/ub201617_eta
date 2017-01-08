from numpy import random

import os
import numpy as np
import itertools

import mazes
from multiprocessing import Process, Queue, current_process
from simulator import simulate


def worker(work_queue, done_queue):
    try:
        for job in iter(work_queue.get, 'STOP'):
            result = simulate(job["maze"], job["self"], job["verbose"], job["graphics"],
                              job["max_iter"])
            done_queue.put(("%s - ID: %s, " % (current_process().name, job["id"]), True, result))
    except Exception, e:
        done_queue.put(("%s - ID: %s failed with: %s" %
                        (current_process().name, job["id"], e.message), False, 0))
    return True


class Agent:
    # legal commands and tests
    # students can (and should) add additional moves and tests
    CMDS = [
        "nop()",
        "move_forward()",
        "move_backward()",
        "turn_left()",
        "turn_right()",
        "turn_up()",
        "turn_down()",
        "turn_random()",
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
        "random_choice()",
        "check_no_progress()",
        "check_visited_position()"
    ]
    parser = None

    def __init__(self, vector):
        self.vector = vector
        self.executable = None
        self.fitness = None

    def to_vector(self):
        return self.vector

    def to_program(self):
        return Agent.vector_to_program(self.vector)

    def to_executable(self):
        if self.executable is None:
            self.executable = Agent.program_to_executable(Agent.vector_to_program(self.vector))
        return self.executable

    def compute_similarity(self, agents):
        """Similarity is represented as number of commands that are this agent and another."""
        return sum([cmd in a.vector for cmd in self.vector for a in agents]) / len(agents)

    def compute_fitness(self, graphics=False):
        """Simulate and visualize some mazes.
         The function simulate can operate on files, programs or vectors.
         If you have problems with visualization (i.e. are a Mac user),
         try running the script from the terminal instead of PyCharm."""
        af = 0
        for m in mazes.mazes_train:
            af += simulate(m, self, verbose=True, graphics=graphics, max_iter=200)
        self.fitness = af / len(mazes.mazes_train)
        return self.fitness

    def async_compute_fitness(self, graphics=False, workers=4):
        work_queue = Queue()
        done_queue = Queue()
        processes = []

        [work_queue.put(
            dict(id=i, maze=m, self=self, verbose=False, graphics=graphics, max_iter=100))
         for i, m in enumerate(mazes.mazes_train)]

        for w in xrange(workers):
            p = Process(target=worker, args=(work_queue, done_queue))
            p.start()
            processes.append(p)
            work_queue.put('STOP')

        for p in processes:
            p.join()

        done_queue.put('STOP')

        af = 0
        for result in iter(done_queue.get, 'STOP'):
            af += result[2]

        self.fitness = af / len(mazes.mazes_train)
        return self.fitness

    def solve_mazes(self):
        self.compute_fitness(graphics=False)

    @staticmethod
    def generate_random(agent_size):
        cmds = [i for i in range(len(Agent.get_parser()))]
        random.shuffle(cmds)
        return Agent(cmds[0:agent_size])

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
            print("VECTOR: ")
            print(v)
            print("i: ")
            print(i)
            raise Exception("Illegal vector")
