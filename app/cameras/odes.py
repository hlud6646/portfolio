import numpy as np
from time import sleep, time

# Global parameters
N = 50
dt = 10 ** -2.8


def init_state(A=None):
    A = A or np.random.randint(-4, 4, (2, 2))
    z = np.random.rand(2, N) - 0.5  # z lies in (-.5, .5)
    color = np.random.uniform(0, 0.9, (N, 3)) * 100
    return (A, z, color)


def update(z, A):
    z += A.dot(z) * dt
    for i in range(N):
        if np.max(np.abs(z[:, i])) > 0.5:
            z[:, i] = np.random.rand(2) - 0.5


def plot(z, canvas, color, colorfactor):
    height, width = canvas.shape[:2]
    w = z + 0.5
    w[0] *= height
    w[1] *= width
    w = w.astype(int)
    canvas[w[0], w[1]] += color * colorfactor


def gen(height, width, colorfactor=1, fps=None):
    while True:
        t0 = time()
        A, z, color = init_state()
        canvas = np.zeros((height, width, 3), np.float32)
        while time() - t0 < 5:
            for i in range(100):
                canvas *= 0.99
                update(z, A)
                plot(z, canvas, color, colorfactor)
            yield canvas
            sleep(1 / fps)
