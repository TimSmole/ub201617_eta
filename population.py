from random import randint, uniform
from agent import Agent
from enum import Enum


class Mutation(Enum):
    RANDOM = 'random'
    SWAP = 'SWAP'


class Ranking(Enum):
    FITNESS = 'fitness'
    DIVERSITY = 'diversity'


class Population:
    def __init__(self, population_size=10, agent_size=20, tournament_size=5,
                 mutation=Mutation.RANDOM, mutation_rate=0.015, elite_size=1,
                 ranking=Ranking.FITNESS):
        self.ranking = ranking
        self.population_size = population_size
        self.agent_size = agent_size
        self.agents = None
        self.mutation_rate = mutation_rate
        self.mutation = mutation
        self.tournament_size = tournament_size
        self.elite_size = elite_size

    def generate_agents(self):
        self.agents = [Agent.generate_random(self.agent_size) for _ in range(self.population_size)]

    def evolve(self, debug=False):
        new_agents = self.get_sorted_agents(self.agents)[:self.elite_size]
        for _ in range(self.elite_size, self.population_size):
            parent1 = self.tournament_selection(new_agents)
            parent2 = self.tournament_selection(new_agents + [parent1])
            child = self.cross_agents(parent1, parent2)
            new_agents.append(self.mutate(child))
        self.agents = new_agents

    def cross_agents(self, parent_a, parent_b):
        parents = [parent_a, parent_b]
        return Agent([parents[randint(0, 1)].vector[randint(0, self.agent_size - 1)] for i in range(self.agent_size)])

    @staticmethod
    def return_fittest(candidates):
        return Population.get_sorted_agents(candidates)[0]

    @staticmethod
    def return_most_diverse(candidates, population):
        best_score = float("inf")
        best = 0
        for i, c in enumerate(candidates):
            # TODO TIM: CHECK SIMILARITY -> TEST
            score = (c.compute_similarity(population) / 100 + 1) * c.fitness
            if score < best_score:
                best_score = score
                best = i
        return candidates[best]

    def mutate(self, agent):
        if self.mutation == Mutation.RANDOM:
            cmds = set([i for i in range(len(agent.get_parser()))])
            for i in range(0, len(agent.vector)):
                if uniform(0, 1) < self.mutation_rate:
                    new_cmds = list(cmds - set(agent.vector))
                    agent.vector[i] = new_cmds[randint(0, len(new_cmds) - 1)]
            return agent
        elif self.mutation == Mutation.SWAP:
            for cursor in range(0, self.agent_size):
                if uniform(0, 1) < self.mutation_rate:
                    change_position = randint(0, self.agent_size - 1)
                    swap_a = agent.vector[cursor]
                    swap_b = agent.vector[change_position]
                    agent.vector[cursor] = swap_b
                    agent.vector[change_position] = swap_a
            return agent

    def tournament_selection(self, new_agents):
        tournament = []
        for i in range(0, self.tournament_size):
            random_id = randint(0, len(self.agents) - 1)
            tournament.append(self.agents[random_id])
        if self.ranking == Ranking.FITNESS:
            return self.return_fittest(tournament)
        else:
            return self.return_most_diverse(tournament, new_agents)

    @staticmethod
    def get_sorted_agents(candidates):
        return sorted(candidates, key=lambda x: x.fitness)
