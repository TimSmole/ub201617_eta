from agent import Agent


class Population:
    def __init__(self, population_size=10, agent_size=20):
        self.population_size = population_size
        self.agent_size = agent_size
        self.agents = None

    def generate_agents(self):
        self.agents = [Agent.generate_random(self.agent_size) for _ in range(self.population_size)]

    def crossover(self):
        pass

