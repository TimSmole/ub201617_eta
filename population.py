from random import randint

from simulator import get_parser, vector_to_prog


class Population:
    def __init__(self, population_size=10, agent_size=20):
        self.population_size = population_size
        self.agent_size = agent_size
        self.agents = None

    def generate_agents(self):
        cmds = get_parser()
        return [[randint(0, len(cmds) - 1) for _ in range(self.agent_size)]
                for _ in range(self.population_size)]

    def crossover(self):
        pass

