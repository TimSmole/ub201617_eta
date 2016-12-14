# (start_row, start_column, goal_row, goal_column, binary_matrix)
# (True = Wall, False = Path)
import pickle
import glob

mazes_train = []
for pk in glob.glob("mazes/training/*.pkl"):
    mazes_train.append(pickle.load(open(pk)))
