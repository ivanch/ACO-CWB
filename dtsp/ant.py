import random

class Ant:
	def __init__(self, alpha, beta, num_nodes, edges):
		self.alpha = alpha
		self.beta = beta
		self.num_nodes = num_nodes
		self.edges = edges
		self.tour = None
		self.distance = 0.0

	def _select_node(self):
		unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour]
		exploration = random.uniform(0.0,1.0)
		if exploration < 0.10: #randomly explore
			min = float("inf")
			for unvisited_node in unvisited_nodes:
				if self.edges[self.tour[-1]][unvisited_node].weight < min:
					min = self.edges[self.tour[-1]][unvisited_node].weight
					min_node = unvisited_node
			explored_node = min_node
			return explored_node
		else:
			roulette_wheel = 0.0
			for unvisited_node in unvisited_nodes: 
				roulette_wheel += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
									pow((1.0 / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
			random_value = random.uniform(0.0, 1.0)
			wheel_position = 0.0
			
			for unvisited_node in random.sample(unvisited_nodes,len(unvisited_nodes)):
				wheel_position += (pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
									pow((1.0 / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)) / roulette_wheel
				if wheel_position >= random_value:
					return unvisited_node

	def find_tour(self):
		self.tour = [random.randint(0, self.num_nodes - 1)]
		while len(self.tour) < self.num_nodes:
			self.tour.append(self._select_node())
		return self.tour

	def get_distance(self):
		self.distance = 0.0
		for i in range(self.num_nodes):
			self.distance += self.edges[self.tour[i]][self.tour[(i + 1) % self.num_nodes]].weight
		return self.distance
