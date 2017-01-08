import os
import time
import argparse

from datetime import datetime
from dateutil.parser import parse
from agent import Agent
from population import Population, Ranking


execution_break = "2017-01-09T16:00:00"

class MazeRunner(object):
    POPULATION_SIZE = 0
    AGENT_SIZE = 0
    NUMBER_OF_GENERATIONS = 0
    ELITE_SIZE = 0

    # For stats
    best_fitness = []
    worst_fitness = []
    average_fitness = []

    def __init__(self, population_size, agent_size, 
                    number_of_generations, elite_size):

        self.POPULATION_SIZE = population_size
        self.AGENT_SIZE = agent_size
        self.NUMBER_OF_GENERATIONS = number_of_generations
        self.ELITE_SIZE = elite_size

        self.DELIMITER = "-" * 15 + "\n"

    def execute(self):
        start = time.time()
        population = Population(population_size=self.POPULATION_SIZE, 
                                agent_size=self.AGENT_SIZE, 
                                elite_size=self.ELITE_SIZE,
                                ranking=Ranking.FITNESS)
        
        population.generate_agents()
        do_break_on_time, break_date_time = self.prepare_execution_break(execution_break)
        padding = "=" * 26

        i = 0
        while i < self.NUMBER_OF_GENERATIONS \
                and (not do_break_on_time or (do_break_on_time and datetime.now() < break_date_time)):
            
            print "".join((padding, (" GENERATION " + str(i) + " "), padding))
            fit_start = time.time()

            fitness = [a.async_compute_fitness() for a in population.agents]
            print("async_compute_fitness time: " + str(time.time() - fit_start))

            population_avg = sum(fitness) / len(fitness)
            for f in fitness:
                print("Agent fitness: " + str(f))
            
            agents_sorted = sorted(fitness)
            population_best = agents_sorted[0]
            population_worst = agents_sorted[len(agents_sorted) - 1]
        
            print("Best population fitness: " + str(population_best))
            print("Worst population fitness: " + str(population_worst))
            print("Average population fitness: " + str(population_avg))
        
            self.best_fitness.append(population_best)
            self.worst_fitness.append(population_worst)
            self.average_fitness.append(population_avg)

            population.evolve(debug=False)
            i += 1

        print("".join((padding, (" FINISHED " + str(i) + " "), padding)))
        print("Execution time: " + str(time.time() - start) + "\n")

        [a.async_compute_fitness() for a in population.agents]
        best = population.return_fittest(population.agents)

        print("==== BEST AGENT ====")
        stats_path = './out/run_stats.txt'
        self.write_stats_to_file(stats_path)
        self.save_agent(best)
        best.solve_mazes()

    def write_stats_to_file(self, file_path):
        # Open file
        file = open(file_path, 'w+')

        # Write statistical data to file
        file.write("POP. SIZE: " + str(self.POPULATION_SIZE) + "\n")
        file.write("AGENT.SIZE: " + str(self.AGENT_SIZE) + "\n")
        file.write("GENERATIONS: " + str(self.NUMBER_OF_GENERATIONS) + "\n")
        file.write("ELITE SIZE: " + str(self.ELITE_SIZE) + "\n")

        file.write("BEST FITNESS\n")
        file.write(self.DELIMITER)
        for b in self.best_fitness:
            file.write(str(b) + "\n")

        file.write("WORST FITNESS\n")
        file.write(self.DELIMITER)
        for w in self.worst_fitness:
            file.write(str(w) + "\n")

        file.write("AVERAGE FITNESS\n")
        file.write(self.DELIMITER)
        for a in self.average_fitness:
            file.write(str(a) + "\n")
        file.close()

    def save_agent(self, agent):
        filename = './out/agent_' + str(self.POPULATION_SIZE) + '_' + \
                   str(self.AGENT_SIZE) + '_' + str(self.NUMBER_OF_GENERATIONS) + '_' + \
                   str(self.ELITE_SIZE) + '_' + str(agent.fitness) + '.txt'
        
        file = open(filename, 'w+')
        file.write("".join(agent.to_program()))
        file.flush()
        print("".join(agent.to_program()))


    def prepare_execution_break(self, date_time_string):
        try:
            dt = parse(date_time_string)
            return True, dt
        except ValueError:
            return False, None


def read_agent(filename):
    return Agent.generate_from_file_or_string("./out/" + filename)


def read_best_agent():
    fitness = []
    for f in os.listdir("./out/"):
        if os.path.isfile(os.path.join("./out/", f)) and 'agent_' in f:
            fitness.append(float(f.split("_")[-1].split(".txt")[0]))
    best_fitness = sorted(fitness)[0]
    return read_agent([f for f in os.listdir("./out/") if str(best_fitness) in f][0])


def solve_with_best():
    agent = read_best_agent()
    agent.solve_mazes()


if __name__ == "__main__":
    """ 
    SAMPLE PARAMETERS
    -----------------
    population_size = 150
    agent_size = 25
    number_of_generations = 500
    elite_size = 15

    """
    # Parsing arguments
    parser = argparse.ArgumentParser(description='Maze parameters')
    # Population size
    parser.add_argument('-p', type=int, dest='population_size', 
        default=150, help='Argument for population size.')
    # Agent size
    parser.add_argument('-a', type=int, dest='agent_size',
        default=25, help='Argument for the agent size parameter.')
    # Number of generations
    parser.add_argument('-g', type=int, dest='gen_number',
        default=500, help='Argument for number of generations')
    # Elite size
    parser.add_argument('-e', type=int, dest='elite_size',
        default=15, help='Argument for elite size')

    args = parser.parse_args()

    # Create MazeRunner object
    maze = MazeRunner(args.population_size, 
                      args.agent_size,
                      args.gen_number,
                      args.elite_size)

    maze.execute()
    solve_with_best()
