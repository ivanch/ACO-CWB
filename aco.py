import numpy as np
from graph import Graph

class Ant:
	def __init__(self):
		self.visited_nodes = []

	def get_visited_nodes(self) -> list:
		return self.visited_nodes

	def visit_node(self, node: Graph.Node):
		self.visited_nodes.append(node)

class ACO:
	def __init__(self, graph: Graph, ants: int, alpha: float, beta: float, evaporation_rate: float, intensification: float, beta_evaporation_rate=0, choose_best=0.1):
		self.graph = graph
		self._generate_ants(ants)

		self.alpha = alpha
		self.beta = beta
		self.evaporation_rate = evaporation_rate
		self.intensification = intensification
		self.beta_evaporation_rate = beta_evaporation_rate
		self.choose_best = choose_best

	def _generate_ants(self, ants):
		self.ants = [Ant() for _ in range(ants)]

	def _get_next_node(self, from_node: Graph.Node):
		next_node = -1
		possible_nodes = self.graph.get_graph()[from_node.id] # Ids: Edges
		possible_nodes_ids = possible_nodes.keys() # Ids
		if np.random.random() <= self.choose_best:
			pheromones = []
			for val in possible_nodes.values():
				pheromones.append(val.pheromone)
			next_node = np.argmax(pheromones) # index only
			next_node = possible_nodes_ids[next_node]
		else:
			denominator = np.sum(possible_nodes_ids)
			probabilities = possible_nodes_ids / denominator
			next_node = np.random.choice(range(len(probabilities)), p=probabilities)
		return next_node

	def _apply_pheromone(self, edge: Graph.Edge):
		node.pheromone += 1

	def run(self, iterations=100):
		pass
		#for it in range(iterations):
