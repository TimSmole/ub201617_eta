#  REQUIREMENTS #
To run this project you need to have installed enum34 package.
If you are using pycharm go to File -> Settings -> search for Project Interpreter -> install package -> search fro enum34.
You can also install it by command: pip install --upgrade pip enum34

If you are running a linux instance, you can install virtualenv wrapper and issue the following commands:

`pip install -r requirements.txt`

# ABOUT THIS PROJECT #

## ASSIGNMENT DESCRIPTION ##

* Genertic algorithm
* 2D Maze
* Fixed set of commands
* Python programming language

### Agent ###

* Presented as integer vector/array
* Each number corresponds to a cerating command: move_forward, turn_left, set_flag, mark_position, go_to_flag,...

### Fittness score ###

* Fitness score is used to summarize how close a given solution is to achieve the set goal.
* Since our agents had to solve a maze, the fitness function was defined as a distance from mazes exit.
* Score was calculated as an average of multiple distances.

## What are genetic algorithms? ##

* A genetic algorithm is a metaheuristic method inspired by the process of natural selection.
* It relies on bio-inspired operators such as mutation, crossover and seelection.

### Elitism ###

* Preserves a small number of fittests candidates from the previous generation.
* Prevents wasting time re-discovering previously discarded partial solutions.

### Tournament selection ###

* At random selects individuals from a population
* The strongest (fittest) individual survive and is used for crossover.
* This project uses tournament implementation between two individuals.

### Crossover ###

* Crossover is a process of taking more than one parent solutions and producing a child solution from them.
* Different methods: Single-point crossover, Two-point crossover, Uniform crossover and Half uniform crossover.

### Mutation ###

* A mutation alters one or more gene values in a chromosome
* It occurs during evolution according to a user-defined probability
* If a mutation probability is too high, search will turn into a primitive random search.

## Assignment results ##

* Agents fitness evolved from generation to generation. Each geneeration jump produced better fitness results.
* For the termination process, a fixed number of generation alongiside an allogation budget (For testing, a fixed point in time was used).
* Usage of multithreading was used to achieve faster results (around a 80% faster average computing time).

### Comparison with random agents ###

* A different population size was used to showcase the results. Non evolving agents were used against evolution, to compare average fitness results. From the graphs below, it is clear, that generation after generation, the evolving agents' fitness score was closer to the genetic algorithms limit, than that of a randomized strategy.

### Graphed results ###

* Agent size = 30
* Elitism size = 5

* Population size = 50
![alt tag](https://github.com/TimSmole/ub201617_eta/blob/master/results/avg_compare.png)

* Population size = 100
![alt tag](https://github.com/TimSmole/ub201617_eta/blob/master/results/worst_compare.png)

* Population size = 50
![alt tag](https://github.com/TimSmole/ub201617_eta/blob/master/results/best_compare.png)

* Population size = 50
![alt tag](https://github.com/TimSmole/ub201617_eta/blob/master/results/worst_compare.png)

## Conclusion ##

The project took a closer look at how genetic algorithms evolution works. By implementing a simple maze solving problem it was showcased how different scenarios affect the process of evolution of a population.

Se nekej glede rezultatiov, glede cesa smo bli preseneceni...
