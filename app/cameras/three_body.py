import numpy as np
from scipy.ndimage import gaussian_filter
from itertools import product
from time import sleep, time

# Modelling stuff


def force(a, b):
    """ Return the gravitational force that b exerts on a. """
    G = 10e-5
    v = b["location"] - a["location"]
    d = sum(v * v) ** 0.5
    return (G * a["mass"] * b["mass"] / d ** 2) * v


def update(state):
    DT = 10e-2
    a, b, c = state
    q, w, e = [force(a, b), force(a, c), force(b, c)]
    net_force = np.array([q + w, e - q, -e - w])
    state["velocity"] += DT * net_force
    state["location"] += DT * state["velocity"]


def init_state():
    state = np.empty(
        3,
        dtype=[
            ("location", float, 2),
            ("velocity", float, 2),
            ("mass", float, 1),
            ("color", float, 3),
        ],
    )
    state["location"] = np.random.uniform(-0.7, 0.7, (3, 2))
    state["velocity"] = np.zeros((3, 2))
    state["mass"] = np.ones(3)
    state["color"] = np.random.uniform(0.2, 0.9, (3, 3)) ** 2 * 10
    return state


# Plotting stuff


def make_disk():
    """ Make a round mask for drawing the point masses. """
    r = 4
    disk = np.ones((2 * r, 2 * r, 3))
    for y, x in product(range(2 * r), repeat=2):
        d2 = (x - r) ** 2 + (y - r) ** 2
        disk[y][x] = int(d2 < r * r) * (1 - d2 / (r ** 2))
    return disk[1:, 1:]


def init_transforms(height, width):
    """ Return vectorized transformations from (-1, 1)x(-1, 1) to (0, width)x(0, height).
            These are a convenience for making drawing on the image frame cleaner.
            It's a compromise that every plotting method must call this method to create its own transformations, 
            but nesseccary in order that height and width can stay out of global namespace."""

    @np.vectorize
    def w(x):
        return np.int(((1 + x) / 2) * width)

    @np.vectorize
    def h(y):
        return np.int(((1 - y) / 2) * height)

    return w, h


def plot(state, canvas, color_factor):
    """ color_factor should by 1 if cv2 is used to write jpegs. """
    height, width = canvas.shape[:2]
    x_to_w, y_to_h = init_transforms(height, width)
    disk = make_disk()
    for mass in state:
        r = np.max(np.abs(mass["location"]))
        if r > 0.9:  # too close to the edge
            continue
        x, y = mass["location"]
        x, y = x_to_w(x), y_to_h(y)
        r = 3
        canvas[y : y + 2 * r + 1, x : x + 2 * r + 1] += (
            disk * mass["color"] * color_factor
        )


# Main generator


def gen(height, width, color_factor=1, fps=1000):
    while True:
        t0 = time()
        state = init_state()
        canvas = np.zeros((height, width, 3), np.float32)
        while time() - t0 < 10:
            for i in range(20):
                canvas *= 0.995
                update(state)
                plot(state, canvas, color_factor)
            yield canvas
        sleep(1 / fps)
