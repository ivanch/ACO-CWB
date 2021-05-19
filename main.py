from coords import graph_from_file
from render import Render
from aco import ACO
import matplotlib.pyplot as plt

plt.ion()
render = Render(plt)
overall_best_path = [0]

def on_iteration_completed(best_path, best_distance):
  plt.clf()
  render.plot(graph, best_path, overall_best_path)

if __name__ == '__main__':
  graph = graph_from_file('nodes.csv')
  traveled_distance = 0

  while(True):
    aco = ACO(graph = graph, ants = 500, evaporation_rate = 0.1, intensification = 1, choose_best = 0.15)

    best_path, best_distance = aco.run(start_path = overall_best_path,
                                       iterations = 15, on_iteration_completed = on_iteration_completed)

    plt.show()
    on_iteration_completed(best_path, best_distance)

    overall_best_path_len = len(overall_best_path)

    if overall_best_path_len == len(graph.nodes):
      overall_best_path.append(0)
      break

    overall_best_path.append(best_path[overall_best_path_len])

    traveled_distance = aco.get_distance_in_path(overall_best_path)

    print("Melhor caminho no geral:", overall_best_path)
    print("Melhor distância no geral:", traveled_distance)

    graph.reroll_costs()
    input("Go to next node...\n")

  print("Melhor caminho no geral:", overall_best_path)
  print("Melhor distância no geral:", traveled_distance)
  plt.show()
  on_iteration_completed(best_path, best_distance)
