import numpy as np
from cv2 import imencode
from time import sleep
norm, sin, cos, pi = np.linalg.norm, np.sin, np.cos, np.pi

green = np.array((0, 250, 0))
yellow= np.array((0, 250, 250))



# Modelling stuff

def normal(q, e):
	""" Return unit inward pointing normal vetor to the ellipse with eccentricity e, at the point q. """
	n = np.array( (((1 - e * e) * q[0] / q[1])[0], 1) )
	if q[1] > 0:
		n = -n 
	return n / norm(n)

def reflected_unit_vector(d, q, e):
	""" d is vector representing a ray which meets the ellipse (with eccentricity e) at q.
		Returns a vector representing the reflected ray leaving q. """
	n = normal(q, e)
	d = 2*d.dot(n)*n - d
	return d / norm(d)

def next_intersection(p, r, e):
	""" Given a ray leaving p in the direction of r, return the point where this ray next meets the ellipse. """
	c = 1-e*e
	k = -2 * (c * p[0] * r[0] + p[1] * r[1] ) / (c * r[0]**2 + r[1]**2)
	return p + k*r

def init_state(e=None):
	e = e or np.random.rand(1)			# eccentricity in (0,1)
	b = (1-e**2)**.5					# equation of ellipse: b^2x^2 + y^2 = b^2			
	theta = pi*np.random.rand(1)		# angle of incoming ray in (0, pi)
	p = b*(0,1)							# ray enters at the top of the ellipse
	r = -np.array((sin(theta)[0], cos(theta)[0]))
	return (e, p, r)




# Init stuff

def init_transforms(height, width):
	""" Return vectorized transformations from (-1, 1)x(-1, 1) to (0, width)x(0, height).
		These are a convenience for making drawing on the image frame cleaner.
		It's a compromise that every plotting method must call this method to create its own transformations, 
		but nesseccary in order that height and width can stay out of global namespace."""
	@np.vectorize
	def w(x):
		return np.int(((1+x)/2) * width)
	@np.vectorize
	def h(y):
		return np.int(((1-y)/2) * height)
	return w, h

def init_ellipse(e, height, width):
	""" Generate a mask for the outline of the ellipse. """
	x_to_w, y_to_h = init_transforms(height, width)
	b = (1-e**2)**.5
	ellipse = np.zeros((height, width, 3), np.float32)
	x = np.linspace(-.999, .999, 500)
	y1 = b*(1 - x**2)**.5
	y2 = -y1[:]

	x = x_to_w(x)
	y1, y2 = y_to_h(y1), y_to_h(y2)

	ellipse[y1, x] += 250
	ellipse[y2, x] += 250
	return ellipse

def init_canvas(height, width):
	""" Initialise a blank canvas. """
	canvas = np.zeros((height, width, 3), np.float32)
	return canvas



# Plotting

def plot_dot(p, canvas):
	height, width = canvas.shape[:2]
	x_to_w, y_to_h = init_transforms(height, width)
	x, y = p
	x = x_to_w(x)
	y = y_to_h(y)
	canvas[y-2:y+2, x-2:x+2] += green

def plot_ray(p, q, canvas):
	height, width = canvas.shape[:2]
	x_to_w, y_to_h = init_transforms(height, width)
	x = np.linspace(x_to_w(p[0]), x_to_w(q[0]), 500).astype(int)
	y = np.linspace(y_to_h(p[1]), y_to_h(q[1]), 500).astype(int)
	canvas[y, x] += yellow



# Main generator

def gen(height, width, fps=10):
	e, p, r = init_state()
	q = next_intersection(p, r, e)
	ellipse= init_ellipse(e, height, width)
	canvas = init_canvas(height, width) + ellipse
	while True:
		plot_dot(p, canvas)
		q = next_intersection(p, r, e)
		plot_dot(q, canvas)
		plot_ray(p, q, canvas)
		r = reflected_unit_vector(r, q, e)
		p = q
		yield canvas
		sleep(1 / fps)
		if np.abs(q[0]) < 0.01:
			e, p, r = init_state()
			q = next_intersection(p, r, e)
			ellipse= init_ellipse(e, height, width)
			canvas = init_canvas(height, width) + ellipse
