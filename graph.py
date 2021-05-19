from traffic import get_expected_time, gen_traffic_cost

class Graph:
  class Edge:
    def __init__(self, cost, node_from, node_to):
      self.cost = cost
      self.virtual_cost = get_expected_time(cost, gen_traffic_cost())
      self.pheromone = 1.0
      self.node_from = node_from
      self.node_to = node_to

    def __repr__(self):
      return "Edge(%.2f, %.2f)" % (self.cost, self.virtual_cost)

    def eq(self, edge):
      return self.node_from == edge.node_from and self.node_to == edge.node_to
    
    def reroll_cost(self):
      self.virtual_cost = get_expected_time(self.cost, gen_traffic_cost())

  class Node:
    def __init__(self, id, name, point):
      self.id = id
      self.name = name
      self.point = point

    def __repr__(self):
      return "Node(%d, %s, (%f, %f))" % (self.id, self.name, self.point[0], self.point[1])

    def visit(self):
      self.visited = True

  def __init__(self):
    self.graph = {}
    self.nodes = []
    self.edges = []

  def get_graph(self) -> dict:
	  return self.graph
  
  def reroll_costs(self):
    for edge in self.edges:
      edge.reroll_cost()

  def remove_edge(self, node_from, node_to):
    edge1 = self.graph[node_from][node_to]
    edge2 = self.graph[node_to][node_from]
    for i, edge in enumerate(self.edges):
      if edge.eq(edge1) or edge.eq(edge2):
        self.edges.pop(i)
    self.graph[node_from].pop(node_to)
    self.graph[node_to].pop(node_from)

  def add_edge(self, edge: Edge, bidirectional = False):
    node_from = edge.node_from
    node_to = edge.node_to
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
      reverse_edge = self.Edge(edge.cost, edge.node_to, edge.node_from)
      self.add_edge(reverse_edge)

  def print(self):
    print(self.graph)
    print(self.nodes)