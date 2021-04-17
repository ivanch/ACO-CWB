import math
from ant import Ant

class ACO:
	def __init__(self, colony_size=10, elitist_weight=1.0, min_scaling_factor=0.001, alpha=1.0, beta=3.0,
				 rho=0.1, pheromone_deposit_weight=1.0, initial_pheromone=1.0, jump_pheromone=1.5, steps=100, nodes=None, labels=None, previous_path=None):
		self.colony_size = colony_size
		self.elitist_weight = elitist_weight
		self.min_scaling_factor = min_scaling_factor
		self.rho = rho
		self.pheromone_deposit_weight = pheromone_deposit_weight
		self.steps = steps
		self.num_nodes = len(nodes)
		self.nodes = nodes
		if labels is not None:
			self.labels = labels
		else:
			self.labels = range(1, self.num_nodes + 1)
		self.edges = [[None] * self.num_nodes for _ in range(self.num_nodes)]
		for i in range(self.num_nodes):
			for j in range(i + 1, self.num_nodes):
				self.edges[i][j] = self.edges[j][i] = self.Edge(i, j, math.sqrt(
					pow(self.nodes[i][0] - self.nodes[j][0], 2.0) + pow(self.nodes[i][1] - self.nodes[j][1], 2.0)),
																initial_pheromone)
		if previous_path != None:
			for i in range(len(previous_path)):
				if (previous_path[i-1] in labels) and (previous_path[i] in labels):
					for j in range(len(labels)): #find index-1
						if previous_path[i-1] == labels[j]:
							for k in range(len(labels)):#find index-2
								if previous_path[i] == labels[k]:
									self.edges[j][k].pheromone = jump_pheromone
									self.edges[k][j].pheromone = jump_pheromone
		self.global_best_tour = None
		self.global_best_distance = float("inf")

	def _add_pheromone(self, tour, distance, weight=1.0):
		pheromone_to_add = self.pheromone_deposit_weight / distance
		for i in range(self.num_nodes):
			self.edges[tour[i]][tour[(i + 1) % self.num_nodes]].pheromone += weight * pheromone_to_add

	def add_ants(self, quantity = 100):
		alpha = 1.0
		beta = 3.0
		self.ants = [Ant(alpha, beta, self.num_nodes, self.edges) for _ in range(self.colony_size)]

	def run(self):
		for step in range(self.steps):
			for ant in self.ants:
				self._add_pheromone(ant.find_tour(), ant.get_distance())
				if ant.distance < self.global_best_distance:
					self.global_best_tour = ant.tour
					self.global_best_distance = ant.distance
			self._add_pheromone(self.global_best_tour, self.global_best_distance, weight=self.elitist_weight)
			for i in range(self.num_nodes):
				for j in range(i + 1, self.num_nodes):
					self.edges[i][j].pheromone *= (1.0 - self.rho)

		print('Route Sequence: {0} '.format(','.join(str(self.labels[i]) for i in self.global_best_tour)))
		print('\nDistance of tour: {0}\n'.format(round(self.global_best_distance, 2)))