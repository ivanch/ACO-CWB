from coords import graph_from_file
from render import plot
from aco import ACO

if __name__ == '__main__':
  graph = graph_from_file('nodes.csv')

  aco = ACO(graph = graph, ants = 1000, evaporation_rate = 0.1, intensification = 1, choose_best = 0.15)
  best_path = aco.run(iterations = 20)

  plot(graph, best_path)