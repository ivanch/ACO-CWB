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

def plot(graph: Graph):
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

  #plt.plot([x[0], x[1], x[0], x[2]], [y[0], y[1], y[0], y[2]], '-y')
  plt.plot(edge_x, edge_y, '-y')
  plt.plot(point_x, point_y, 'ro')
  plt.axis([
    -MARGIN_X,
    PLOT_SIZE + MARGIN_X,
    -MARGIN_Y,
    PLOT_SIZE + MARGIN_Y
  ])

  plt.show()
