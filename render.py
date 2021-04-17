import sys
import matplotlib.pyplot as plt
from graph import Graph

PLOT_SIZE = 10000
MARGIN_H = 500
MARGIN_V = 500

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

  return (
    leftmost,
    rightmost,
    upmost,
    downmost,
  )

def zoom_point(point: tuple, bounding_box: tuple):
  l, r, u, d = bounding_box
  size_x = r - l
  size_y = u - d
  x = PLOT_SIZE * (r - point[0]) / size_x
  y = PLOT_SIZE * (u - point[1]) / size_y

  return (x, y)

def plot(graph: Graph):
  bounding_box = calc_bounding_box(graph)

  for node in graph.nodes:
    point = zoom_point(node.point, bounding_box)
    print(point)
    plt.plot(point[0], point[1], 'ro')

  plt.axis([-MARGIN_H, PLOT_SIZE + MARGIN_H, -MARGIN_V, PLOT_SIZE + MARGIN_V])
  plt.show()