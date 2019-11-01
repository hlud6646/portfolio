import numpy as np
from scipy.signal import convolve2d
from time import sleep
from itertools import product


# Model

def update(state):
    kernel = np.array([1, 1, 1, 1, 0, 1, 1, 1, 1]).reshape((3, 3))
    neighbours = convolve2d(state, kernel, mode='same')

    death_rule = np.logical_and(
        state, np.logical_or(neighbours < 2, neighbours > 3))
    birth_rule = np.logical_and(~state, neighbours == 3)
    lives_rule = np.logical_and(
        state, np.logical_or(neighbours == 2, neighbours == 3))

    return np.where(death_rule, 0,
                    np.where(lives_rule, 1,
                             np.where(birth_rule, 1, state)))

# Init

def init_cells():
    height, width = 36, 72
    cells = np.empty((height, width), dtype=[('state',  bool,    1),
                                             ('color',  float,   3)])
    cells['state'] = np.random.choice([0, 1], (height, width), p=[.7, .3])
    cells['color'] = np.random.uniform(.3, .9, (height, width, 3))
    return cells


# Plot

def plot(cells, canvas, color_factor):
    """ The scale of color values depends on how images are drawn.
        This is the purpose of the color_factor argument. """
    height, width = canvas.shape[:2]
    gheight, gwidth = cells.shape
    d = height//gheight
    r = d // 3  # radius of a cell
    for x, y in product(range(gwidth), range(gheight)):
        if not cells['state'][y][x]:
            continue
        X = (x*d) + d//2
        Y = (y*d) + d//2
        canvas[Y-r:Y+r, X-r:X+r] = cells['color'][y][x]*255

# Generator

def gen(height, width, color_factor=255, fps=24):
    cells = init_cells()
    canvas = np.zeros((height, width, 3), np.float32)
    cache = []

    while True:
        canvas *= 0.1
        new_state = update(cells['state'])

        if not np.any(new_state - cells['state']):
            cells = init_cells()
            cache = []
        elif not all(np.any(cells['state'] ^ x) for x in cache):
            cells['state'] = False
        else:
            cache.append(np.copy(cells['state']))
            cells['state'] = new_state

        plot(cells, canvas, color_factor)
        yield canvas
        sleep(1 / fps)



