from simulator import *
import mazes

af = 0

# Load program file
path = "examples/sample_program2.py"

# Program is a list of commands. Each command ends with \n. Look at simulator.py for more info.
program = open(path).readlines()
print("Program: ")
for line in program:
    print("\t%s" % line)

# Convert program to vector. Use vectors when performing searching, genetic algorithms, etc.
# vector is a list of command numbers 0-227
# The command will fail for illegal programs.
vector = prog_to_vector(program)
print()
print("Vector: ", vector)

# You can convert vectors back to programs to manually examine solutions.
# The command will fail for illegal vectors.
program2 = vector_to_prog(vector)

# Simulate and visualize some mazes.
# The function simulate can operate on files, programs or vectors.
# If you have problems with visualization (i.e. are a Mac user),
# try running the script from the terminal instead of PyCharm.
for m in mazes.mazes_train:
    af += simulate(m, vector, verbose=True, graphics=False, delay=0.1, max_iter=500)
print("Average fitness: ", af/len(mazes.mazes_train))
