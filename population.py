from agent import Agent
from random import randint, random

class Population:
    def __init__(self, population_size=10, agent_size=20):
        self.population_size = population_size
        self.agent_size = agent_size
        self.agents = None
        self.mutation_rate = 0.015
        self.tournament_size = 5
        self.enable_elitism = True

    def generate_agents(self):
        self.agents = [Agent.generate_random(self.agent_size) for _ in range(self.population_size)]

    def crossover(self):
        pass

    #Proposed code for evolution
    def return_best(self, candidates):
        #TODO: return candidate with max fitness value
        return candidates[0]

    def cross_agents(self, parent_a, parent_b):
        child = [0**self.agent_size]
        start_pos = randint(0, self.agent_size)
        end_pos = randint(0, self.agent_size)
        for i in range(0, self.agent_size):
            if start_pos < end_pos and i > start_pos and i < end_pos:
                child[i] = parent_a[i]
            elif start_pos > end_pos:
                if not (i < start_pos and i > end_pos):
                    child[i] = parent_a[i]
        for i in range(0, self.agent_size):
            if not parent_b[i] in child:
                for ii in range(0, len(child)):
                    if child[ii] == 0:
                        child[ii] = parent_b[i]
                        break
        return child

    def mutate(self, agent):
        for cursor in range(0, self.agent_size):
            if random() < self.mutation_rate:
                change_position = randint(0, self.agent_size)
                swap_a = agent[cursor]
                swap_b = agent[change_position]
                agent[cursor] = swap_b
                agent[change_position] = swap_a
        return agent

    def tournament_selection(self):
        tournament = []
        for i in range(0, self.tournament_size):
            random_id = randint(0, self.population_size)
            tournament.append(self.agents[random_id])
        fittest = self.return_best(tournament)
        return fittest

    def evolve(self):
        new_agents = []
        elitism_offset = 0
        if self.enable_elitism:
            new_agents.append(self.return_best(self.agents))
            elitism_offset = 1
        for i in range(elitism_offset, self.population_size):
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            child = self.cross_agents(parent1, parent2)
            new_agents.append(child)
        for i in range(elitism_offset, self.population_size):
            new_agents[i] = self.mutate(new_agents[i])
        self.agents = new_agents

