# tspsolver.py
# Mike Fortner

import sys
import os
import math
import re
import timeit
import shutil
import random
import itertools
import heapq
import signal

from multiprocessing import Process, Queue as MPQueue

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
class Node(object):
	def __init__(self, label):
		self.label = label
		self.conn = [None, None]
		self.prev = None

	def __contains__(self, item):
		return item in self.conn

	def __len__(self):
		ret = 0
		for item in self.conn:
			if item is not None:
				ret += 1
		return ret

	def __str__(self):
		return "%s"%self.label

	def __repr__(self):
		return "(\"%s\", <%s<, >%s>)"%(self, self.conn[1], self.conn[0])

	def next(self):
		if self.prev is None:
			if self.conn[0] is None: 
				if self.conn[1] is None:
					return None
				else:
					self.conn[1].prev = self
					return self.conn[1]
			else:
				self.conn[0].prev = self
			return self.conn[0]
		elif self.prev == self.conn[0]:
			if self.conn[1] is None: 
				return None
			else:
				self.conn[1].prev = self
				self.prev = None
				return self.conn[1]
		elif self.prev == self.conn[1]:
			if self.conn[0] is None: 
				return None
			else:
				self.conn[0].prev = self
				self.prev = None
				return self.conn[0]
		else:
			raise "oops"
	def connect(self, node):
		for i in xrange(2):
			for j in xrange(2):
				if self.conn[i] is None and node.conn[j] is None:
					self.conn[i] = node
					node.conn[j] = self
					return

	def get_list(self):
		self.prev = None
		start = self
		cur = self.next()
		ret = [start.label]
		while (cur is not None and cur.label != self.label):
			ret.append(cur.label)
			cur = cur.next()
		return ret

	def test_for_loop(self, node):
		for i in xrange(2):
			for j in xrange(2):
				if self.conn[i] is None and node.conn[j] is None:
					self.conn[i] = node
					node.conn[j] = self
					ret = self.has_loop()
					for i in xrange(2):
						for j in xrange(2):
							if self.conn[i] is node and node.conn[j] is self:
								self.conn[i] = None
								node.conn[j] = None
								return ret

	def has_loop(self):
		self.prev = None
		slow = fast_a = fast_b = self
		while (slow and fast_a and fast_b):
			fast_a = fast_b.next()
			if fast_a is None: break
			if (slow.label == fast_a.label):
				return True
			fast_b = fast_a.next()
			if fast_b is None: break
			if (slow.label == fast_b.label):
				return True
			slow = slow.next()
		return False

	def test(self):
		nodes = [Node(i) for i in xrange(10)]
		for i in xrange(len(nodes)):
			nodes[i-1].connect(nodes[i])
			print nodes[-1].has_loop()
		print nodes


class TSP_solver(object):
	def __init__(self, points):
		self.input = points
		self.points = dict([(point[0], (point[1:3])) for point in points])
		self.labels = [a for a,b,c in points]
		self.best_path = self.labels[:]
		random.shuffle(self.best_path)

		self.best_length = self.path_length(self.best_path)
		self.thread = None


	def solve(self):
		self.construct_greedy()
		print "construct_greedy done"
		while True:
			self.k_opt(3) #random 3 opts

	def iterate(self):
		stored_length = self.best_length
		count = 0
		while self.best_length >= stored_length and count < 1000:
			self.k_opt(3) #random 3 opts
			count+=1

	def thread(self):
		self.thread = Process(target=self.iterate)
		self.thread.start()

	def get_update(self):
		if self.thread is None:
			return
		self.thread.join()
		self.thread.start()



	def get_result(self):
		return (self.best_length, self.best_path)

	def sqr_dist(self, a, b):
		"""find the square of the distance between two points.  leaving it as the square of the distance has no effect on ordering"""
		xa, ya = a
		xb, yb = b
		dx = xb - xa
		dy = yb - ya
		return dx*dx + dy*dy

	def dist(self, a, b):
		"""find the integer distance between two points."""
		return int(round(math.sqrt(self.sqr_dist(a, b))))

	def path_length(self, path):
		a = self.points[path[0]]
		b = self.points[path[len(path)-1]]
		length = self.dist(a, b)
		for i in xrange(len(path)-1):
			a = self.points[path[i]]
			b = self.points[path[i+1]]
			length += self.dist(a, b)
		return length

	def construct_greedy(self):
		"""add shortest edge that does not create a small loop or a fork in the path until all points are in path"""
		possible_edges = []
		connections = dict()
		for a in self.labels:
			connections[a] = Node(a)
		for a, b in itertools.combinations(self.labels, 2):
			possible_edges.append((self.sqr_dist(self.points[a], self.points[b]), a, b))
			
		possible_edges = sorted(possible_edges)
		num_edges = 0
		for distance, a, b in possible_edges:
			if len(connections[a]) == 2 or len(connections[b]) == 2:
				continue
			elif connections[a].test_for_loop(connections[b]) and num_edges != len(self.labels)-1:
				continue
			else:
				connections[a].connect(connections[b])
				num_edges+=1

			if num_edges == len(self.labels):
				break

		new_path = connections[0].get_list()
		new_length = self.path_length(new_path)
		if new_length < self.best_length:
			self.best_path = new_path
			self.best_length = new_length
			print self.best_length


	def k_opt(self, k):
		"""tries a single random k-opt move and takes the best reordering of the chunks
	   		runtime is proportional to (k-1)! * 2^k * n"""

		if k < 2: return

		path = self.best_path[:]
		breaks = set()
		while (len(breaks) < k):
			temp = random.randint(0, len(path)-1)
			if (temp - 1) in breaks or (temp + 1) in breaks: continue
			breaks.add(temp)
		breaks = sorted(breaks)
		chunks = [None]*k
		
		for i in xrange(k):
			if i == 0:
				chunks[i] = path[breaks[-1] : len(path)] + path[0 : breaks[0]]
			else:
				chunks[i] = path[breaks[i-1] : breaks[i]]

		best = (self.best_path, self.best_length)
		for flip in itertools.product([False, True], repeat = k):  #iterates over all possible choices of which chunks to reverse
			flipped_chunks = [None]*k
			for i in xrange(len(chunks)):
				if flip[i]:
					flipped_chunks[i] = chunks[i][::-1]
				else: 
					flipped_chunks[i] = chunks[i][:]
			for candidate in itertools.permutations(flipped_chunks[1:]):  #iterates over all possible permutations of chunk order, with chunk[0] first to eliminate rotation symmetry
				test = flipped_chunks[0][:]
				for chunk in candidate:
					test += chunk

				test = test[test.index(0):len(test)] + test[0:test.index(0)]
				
				length = self.path_length(test)
				if length < best[1]:
					best = (test, length)
		if best[1] < self.best_length:
			self.best_path = best[0]
			self.best_length = best[1]
			print self.best_length



	def iterate_3opt(self):
		pass

	def from_file(self, filename):
		with open(filename, "r") as f:
			test_length = int(f.readline())
			test_path = [int(line) for line in f]

			assert(len(test_path) == len(self.best_path))
			self.best_path = test_path

			self.best_length = self.path_length(self.best_path)

			assert(self.best_length == test_length)



#main function
def show_usage():
	"print help message"
	print "Usage:\t{0} [input_file_name] [soln_from_file_name]\n\tno arguments generates a random 2000 point problem".format(sys.argv[0])

def sigterm_handler(signum, frame):
	if "solver" in frame.f_globals.iterkeys():
		solver = frame.f_globals["solver"]
		with open("tsp_result.txt", "w") as f:
			length, path = solver.get_result()
			f.write("%d\n"%length)
			for point in path:
				f.write("%d\n"%point)
		# Create a figure with size 6 x 6 inches.
		fig = Figure(figsize=(6,6))

		# Create a canvas and add the figure to it.
		canvas = FigureCanvas(fig)

		# Create a subplot.
		ax = fig.add_subplot(111)

		# Generate the Scatter Plot.
		ax.scatter([b for a,b,c in solver.input], [c for a,b,c in solver.input], s=20);
		ax.plot([solver.points[i][0] for i in solver.best_path], [solver.points[i][1] for i in solver.best_path], color="red")
		# Save the generated Scatter Plot to a PNG file.
		canvas.print_figure('graph.png',dpi=500)
	exit(0)

if __name__ == '__main__':
	points = list()
	try:
		args = sys.argv
		if len(args) > 1:
			regex = re.compile("\s*(\d+)\s+(\d+)\s+(\d+)\s*") #matches a line that three integers separated by white space and stores the integer strings
			if len(args) == 2: 
				filename = args[1]
				test_file = None
			else: 
				filename = args[1]
				test_file = args[2]
			with open(filename, "r") as f:
				arrays = list()
				solutions = list()
				for line in f:
					m = regex.match(line)
					if m == None: continue
					point = tuple([int(e) for e in m.groups()])
					points.append(point)
		else:
			filename = None
			test_file = None
			points = zip(range(2000), [random.randint(0,2000) for i in xrange(2000)], [random.randint(0,2000) for i in xrange(2000)])
		solver = TSP_solver(points)
		signal.signal(signal.SIGTERM, sigterm_handler)
		signal.signal(signal.SIGINT, sigterm_handler)
		if test_file is not None:
			solver.from_file(test_file)
			while(True):pass
		solver.solve()   #will loop until sigterm or sigint
		with open(filename.split(".")[0] + "_soln.txt", "w") as f:
			f.write("%d\n"%length)
			for point in path:
				f.write("%d\n"%point)


		

	except EnvironmentError as e:  #ususally will be "file not found"
		print e
		sys.exit(1)
	except AssertionError as e:
		show_usage()
		sys.exit(0)


