from coords import graph_from_file
from render import plot

if __name__ == '__main__':
  graph = graph_from_file('nodes.csv')
  plot(graph)
