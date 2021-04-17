import math
import csv

from graph import Graph

# Raio da terra em metros
EARTH_RADIUS = 6371 * (10 ** 3)

# Escala dos pontos
SCALE = 1000

# Pi dividido por 180
PI_OVER_180 = math.pi / 180

# Função para calcular a distância entre duas coordenadas
def from_geo_coords_to_dist(coord_1: tuple, coord_2: tuple):
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

def get_position_from_geo_coords(coords: tuple):
  x = ((coords[1]* -1) + 180) * (EARTH_RADIUS * 2 / 360)
  y = ((coords[0] * -1) + 90) * (EARTH_RADIUS * 2 / 180)
  return (x, y)

# Função para gerar um grafo a partir de um arquivo de coordenadas
def graph_from_file(filename: str):
  graph = Graph()
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rows = []
    for row in csv_reader:
      rows.append(row)

    for (i, row1) in enumerate(rows):
      for row2 in rows[i + 1:]:
        coord_1 = (float(row1[2]), float(row1[3]))
        position_1 = get_position_from_geo_coords(coord_1)

        coord_2 = (float(row2[2]), float(row2[3]))
        position_2 = get_position_from_geo_coords(coord_2)

        cost = from_geo_coords_to_dist(coord_1, coord_2)

        node_to = Graph.Node(int(row1[0]), row1[1], position_1)
        node_from = Graph.Node(int(row2[0]), row2[1], position_2)
        edge = Graph.Edge(cost)

        graph.add_edge(node_from, node_to, edge, bidirectional = True)
      
    return graph
