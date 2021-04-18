from traffic import get_expected_time

class Graph:
  class Edge:
    def __init__(self, cost, traffic_cost):
      self.cost = cost
      self.virtual_cost = get_expected_time(cost, traffic_cost)
      self.pheromone = 1.0

    def __repr__(self):
      return "Edge(%.2f, %.2f)" % (self.cost, self.virtual_cost)

  class Node:
    def __init__(self, id, name, point):
      self.id = id
      self.name = name
      self.point = point

    def __repr__(self):
      return "Node(%d, %s, (%f, %f))" % (self.id, self.name, self.point[0], self.point[1])

  def __init__(self):
    self.graph = {}
    self.nodes = []
    self.edges = []

  def get_graph(self) -> dict:
	  return self.graph

  def add_edge(self, node_from: Node, node_to: Node, edge: Edge, bidirectional = False):
    if node_to.id not in self.graph:
      self.graph[node_to.id] = {}
      self.nodes.append(node_to)

    if node_from.id not in self.graph:
      self.graph[node_from.id] = {}
      self.nodes.append(node_from)

    if edge not in self.edges:
      self.edges.append(edge)

    self.graph[node_from.id][node_to.id] = edge

    if bidirectional:
      self.add_edge(node_to, node_from, edge)

  def print(self):
    print(self.graph)
    print(self.nodes)