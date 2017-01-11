#  REQUIREMENTS #
To run this project you need to have installed enum34 package.
If you are using pycharm go to File -> Settings -> search for Project Interpreter -> install package -> search fro enum34.
You can also install it by command: pip install --upgrade pip enum34

If you are running a linux instance, you can install virtualenv wrapper and issue the following commands:

* pip install -r requirements.txt

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

  
