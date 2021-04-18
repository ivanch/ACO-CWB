import sys
import matplotlib.pyplot as plt
from graph import Graph

PLOT_SIZE = 10000
MARGIN_X = 500
MARGIN_Y = 500

def calc_bounding_box(graph):
  leftmost = sys.maxsize
  rightmost = -sys.maxsize
  upmost = -sys.maxsize
  downmost = sys.maxsize

  for node in graph.nodes:
    x = node.point[0]
    y = node.point[1]

    if x < leftmost:
      leftmost = x
    
    if x > rightmost:
      rightmost = x

    if y < downmost:
      downmost = y
    
    if y > upmost:
      upmost = y

  size_x = rightmost - leftmost
  size_y = upmost - downmost
  return (
    rightmost,
    upmost,
    size_x,
    size_y,
  )

def zoom_point(point: tuple, bounding_box: tuple):
  r, u, size_x, size_y = bounding_box
  aspect_ratio = size_x / size_y
  x = aspect_ratio * PLOT_SIZE * (r - point[0]) / size_x
  y = PLOT_SIZE * (u - point[1]) / size_y

  return (x, y)

def plot_path(path: list, point_x: list, point_y: list):
  path_x = []
  path_y = []

  path_edges = [(path[x], path[x + 1]) for x in range(len(path) - 1)]

  for (c, n) in path_edges:
    path_x.append(point_x[c])
    path_x.append(point_x[n])
    path_y.append(point_y[c])
    path_y.append(point_y[n])

  plt.plot(path_x, path_y, '-g')
  plt.plot(path_x[:2], path_y[:2], '-m')

def plot(graph: Graph, path: list):
  bounding_box = calc_bounding_box(graph)
  point_x = []
  point_y = []

  edge_x = []
  edge_y = []


  for node in graph.nodes:
    point = zoom_point(node.point, bounding_box)
    point_x.append(point[0])
    point_y.append(point[1])

  for key, x in enumerate(point_x):
    for x2 in point_x[key + 1:]:
      edge_x.append(x)
      edge_x.append(x2)

  for key, y in enumerate(point_y):
    for y2 in point_y[key + 1:]:
      edge_y.append(y)
      edge_y.append(y2)

  plt.plot(edge_x, edge_y, '-y')
  plt.plot(point_x, point_y, 'ro')
  plt.plot(point_x[0], point_y[0], 'bo')

  plot_path(path, point_x, point_y)

  plt.axis([
    -MARGIN_X,
    PLOT_SIZE + MARGIN_X,
    -MARGIN_Y,
    PLOT_SIZE + MARGIN_Y
  ])

  plt.show()
