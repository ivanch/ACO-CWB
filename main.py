from coords import graph_from_file
from render import Render
from aco import ACO
import matplotlib.pyplot as plt

plt.ion()
render = Render(plt)

def on_iteration_completed(best_path, best_distance):
  plt.clf()
  render.plot(graph, best_path)

if __name__ == '__main__':
  graph = graph_from_file('nodes.csv')

  aco = ACO(graph = graph, ants = 1000, evaporation_rate = 0.1, intensification = 1, choose_best = 0.15)
  best_path, best_distance = aco.run(iterations = 20, on_iteration_completed = on_iteration_completed)

  plt.show()