import numpy as np
import random
from graph import Graph
from typing import List
import sys
import matplotlib.pyplot as plt

'''
TODO: Levar em consideração o tráfego
Atualmente, só é levado em consideraão o peso dos nós
'''

class Ant:
	def __init__(self):
		self.path = []
		self.visited_nodes = []
		self.current_node = None
		self.travel_distance = 0

	def visit_node(self, node: int, cost: float):
		self.travel_distance += cost
		self.visited_nodes.append(node)
		self.path.append(node)
		self.current_node = node

	def clear(self):
		self.travel_distance = 0
		self.visited_nodes.clear()
		self.path.clear()

class ACO:
	def __init__(self, graph: Graph, ants: int, evaporation_rate: float, intensification: float, choose_best = 0.15):
		self.graph = graph
		self.ants = List[Ant]
		self._generate_ants(ants)

		self.evaporation_rate = evaporation_rate
		self.intensification = intensification
		self.choose_best = choose_best

	def _generate_ants(self, ants):
		self.ants = [Ant() for _ in range(ants)]

	# Retorna um dict {Id: Edge} de possíveis nós com base em nós já visitados
	def _get_possible_nodes(self, from_node: int, visited_nodes: List[int]) -> dict:
		# possíveis nós a partir do nó a partir
		possible_nodes = self.graph.get_graph()[from_node].copy() # {Ids: Edges}

		# remover nós já visitados
		for i in visited_nodes:
			if i in possible_nodes.keys():
				possible_nodes.pop(i)

		# remover nó inicial APENAS se houver outros nós, nó inicial deve ser o último a ser visitado
		if len(possible_nodes) >= 2 and 0 in possible_nodes.keys():
			possible_nodes.pop(0)

		return possible_nodes

	# Com base num nó, escolhe o próximo nó que será visitado por aquela formiga
	def _get_next_node(self, possible_nodes: dict) -> int:
		next_node = -1

		possible_nodes_ids = list(possible_nodes.keys()) # Ids
		pheromones = []

		for val in possible_nodes.values():
			pheromones.append(val.pheromone)

		if np.random.random() <= self.choose_best: # escolhe o melhor nó para ir, com base nos feromônios
			next_node = np.argmax(pheromones) # retorna o índice com maior número de feromônios
			next_node = possible_nodes_ids[next_node]
		else: # escolhe um nó aleatório para ir
			denominator = np.sum(pheromones)
			if denominator == 0:
				next_node = random.choice(possible_nodes_ids)
			else:
				probabilities = [x / denominator for x in pheromones]
				next_node = np.random.choice(range(len(probabilities)), p=probabilities)
				next_node = possible_nodes_ids[next_node]

		return next_node

	def _get_edge_cost(self, from_node: int, to_node: int) -> float:
		return self.graph.get_graph()[from_node][to_node].virtual_cost


	# Intensifica o feromônio de uma aresta
	def _apply_pheromone(self, path: List[int]):
		previous_node = path[0]
		for i in range(1, len(path)):
			next_node = path[i]
			self.graph.get_graph()[previous_node][next_node].pheromone += self.intensification
			previous_node = next_node

	# Aplica evaporização de feromônios de todas as arestas do grafo
	def _apply_evaporation(self):
		edges = self.graph.edges
		for i in range(len(edges)):
			edges[i].pheromone *= (1 - self.evaporation_rate)

	# Principal método da classe: roda a simulação
	def run(self, iterations=80) -> List[int]:
		best_path = []
		best_distances = []
		for iteration in range(iterations):
			print("Iteration %d/%d" % (iteration + 1, iterations))
			best_path = []
			best_distance = sys.maxsize

			for i in range(len(self.ants)):
				# Formiga começa no nó inicial
				self.ants[i].visit_node(self.graph.nodes[0].id, 0)

				path_found = False
				while not path_found:
					ant = self.ants[i]
					possible_nodes = self._get_possible_nodes(ant.current_node, ant.visited_nodes)

					# Se não houver nenhum nó próximo possível, significa que a formiga percorreu todo o percurso
					# Nesse caso, o for continuará para a próxima formiga
					if len(possible_nodes) == 0:
						ant.visited_nodes.clear()
						ant.visited_nodes.append(ant.current_node)
						possible_nodes = self._get_possible_nodes(ant.current_node, ant.visited_nodes)

						cost = self._get_edge_cost(ant.current_node, 0)
						ant.visit_node(self.graph.nodes[0].id, cost)

						# Verifica se a formiga fez o melhor caminho
						if ant.travel_distance < best_distance:
							best_distance = ant.travel_distance
							best_path = ant.path.copy()

						# Limpa informações da formiga para fazer com que ela faça outro percurso depois
						ant.clear()

						path_found = True
					else:
						previous_node = ant.current_node
						next_node = self._get_next_node(possible_nodes)
						cost = self._get_edge_cost(previous_node, next_node)

						ant.visit_node(next_node, cost)

			self._apply_pheromone(best_path)
			self._apply_evaporation()

			print("Melhor caminho:", best_path)
			print("Melhor distância:", best_distance)
			print("\n")

			best_distances.append(best_distance)

		plt.plot(range(len(best_distances)), best_distances)
		plt.savefig('best distances.png', dpi=300, bbox_inches='tight')
		plt.clf()

		return best_path, best_distances[-1]