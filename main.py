import math
import csv

# Raio da terra em metros
EARTH_RADIUS = 6371 * (10 ** 3)

# Pi dividido por 180
PI_OVER_180 = math.pi / 180

class Graph:
  class Edge:
    def __init__(self, cost):
      self.cost = cost
    
    def __repr__(self):
      return "Edge(%.2f)" % (self.cost)

  class Node:
    def __init__(self, id, name, x, y):
      self.id = id
      self.name = name
      self.x = x
      self.y = y
    
    def __repr__(self):
      return "Node(%d, %s, (%d, %d))" % (self.id, self.name, self.x, self.y)

  def __init__(self):
    self.graph = {}
    self.nodes = []

  def add_edge(self, node_from, node_to, edge, bidirectional = False):
    if node_to.id not in self.graph:
      self.graph[node_to.id] = {}
      self.nodes.append(node_to)

    if node_from.id not in self.graph:
      self.graph[node_from.id] = {}
      self.nodes.append(node_from)

    self.graph[node_from.id][node_to.id] = edge

    if bidirectional:
      self.add_edge(node_to, node_from, edge)

  def print(self):
    print(self.graph)
    print(self.nodes)

# Função para calcular a distância entre duas coordenadas
def from_geo_coords_to_dist(coord_1, coord_2):
  lat_1, lng_1 = coord_1
  lat_2, lng_2 = coord_2
  
  fi_lat_1 = lat_1 * PI_OVER_180
  fi_lat_2 = lat_2 * PI_OVER_180

  delta_fi = (lat_2 - lat_1) * PI_OVER_180
  delta_lamba = (lng_2 - lng_1) * PI_OVER_180

  a1 = math.sin(delta_fi / 2) ** 2
  a2 = math.cos(fi_lat_1) * math.cos(fi_lat_2)
  a3 = math.sin(delta_lamba/2) ** 2
  
  a = a1 + a2 * a3
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  
  return EARTH_RADIUS * c

# Função para gerar um grafo a partir de um arquivo de coordenadas
def graph_from_file(filename):
  graph = Graph()
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rows = []
    for row in csv_reader:
      rows.append(row)

    for (i, row1) in enumerate(rows):
      for row2 in rows[i + 1:]:
        if row1[0] != row2[0]:
          coord_1 = (float(row1[2]), float(row1[3]))
          coord_2 = (float(row2[2]), float(row2[3]))
          cost = from_geo_coords_to_dist(coord_1, coord_2)

          node_from = Graph.Node(int(row1[0]), row1[1], 0, 0)
          node_to = Graph.Node(int(row2[0]), row2[1], 0, 0)
          edge = Graph.Edge(cost)

          graph.add_edge(node_from, node_to, edge, bidirectional = True)
      
    return graph     

if __name__ == '__main__':
  graph = graph_from_file('nodes.csv')
  graph.print()
