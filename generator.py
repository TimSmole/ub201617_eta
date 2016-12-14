import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import pickle

def maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    start = (0, shape[1]-2)
    finish = (shape[0]-1, 1)

    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    Z[start[0], start[1]] = 0
    Z[finish[0], finish[1]] = 0
    # Make isles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return (start[0], start[1], finish[0], finish[1], Z)

for i in range(100):
    w = 20
    h = 20
    sx, sy, fx, fy, m = maze(w, h)
    pyplot.figure(figsize=(10, 5))
    pyplot.imshow(m, cmap=pyplot.cm.binary, interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    name = "mazes/test2/maze_%dx%d_%s" % (w, h, hex(hash(tuple(m.ravel()))))
    pyplot.savefig(name+".png", format='png')
    pickle.dump((sx, sy, fx, fy, m), open(name+".pkl", "w"))
#pyplot.show()
