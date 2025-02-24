from pickle import FALSE
import numpy as np
import math
import matplotlib.pyplot as plt
from types import SimpleNamespace as Namespace

import requests

# show extra information
TEXT_DEBUG = False
PLOT_DEBUG = False

plt.subplots(figsize=(10, 10))

# == Custom point class ==========================================
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __str__(self):
    return f"({self.x}, {self.y})"
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class plot:
# ================================
  @staticmethod
  def point(point, label='', offset=(0.1, 0.1), color='blue'):
    plt.plot(point.x, point.y, 'o', zorder=3, color=color)
    if label:  # Check if label is not empty
      plt.text(point.x + offset[0], point.y + offset[1], label, zorder=3, color='red')
# ================================
  @staticmethod
  def line(p1, p2, mode='--', color='blue'):
    if p2.x == p1.x:
      plt.vlines(x=p1.x, ymin=p1.y, ymax=p2.y, color=color, linestyles='dashed')
    else:
      m = (p2.y - p1.y) / (p2.x - p1.x)
      b = p1.y - m * p1.x
      x_values = np.linspace(p1.x, p2.x, 100)
      plt.plot(x_values, m * x_values + b, mode, color=color)
# ================================
  @staticmethod
  def pair(anchor, control, number=0):
      plot.line(anchor, control)
      if TEXT_DEBUG:
        plot.point(control, f'c{number}' if number > 0 else '')
        plot.point(anchor, f'a{number}' if number > 0 else '')
      else:
        plot.point(control)
        plot.point(anchor)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# =- [MATH HELPER FUNCTIONS] =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class find:
# ================================
  @staticmethod
  def dist(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
# ================================
  @staticmethod
  def angle(center, edge):
    return math.atan2(edge.y - center.y, edge.x - center.x)
# ================================
  @staticmethod
  def t_on_arc(arc, t):
    center, r, theta_start, theta_end, clockwise = arc

    if clockwise:
      if theta_end > theta_start:
        theta_end -= 2 * np.pi
    else:
      if theta_end < theta_start:
        theta_end += 2 * np.pi
    theta_t = theta_start + t * (theta_end - theta_start)
    return Point(
        center.x + r * np.cos(theta_t),
        center.y + r * np.sin(theta_t))
# ================================
  @staticmethod
  def t_on_line(line, t):
    return Point(
        line[0].x + t * (line[1].x - line[0].x),
        line[0].y + t * (line[1].y - line[0].y))
# ================================
  @staticmethod
  def t(t, equation):
    i, t = divmod(t, 1)
    i = int(i)
    i %= len(equation) #to ensure that the section is within the length

    if i % 3 == 1:
      return find.t_on_line(equation[i], t)
    else:
      return find.t_on_arc(equation[i], t)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def rotate_points(x_list, y_list, angle_degrees):
    # Convert angle from degrees to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate the center of mass (centroid)
    centroid_x = sum(x_list) / len(x_list)
    centroid_y = sum(y_list) / len(y_list)

    # Translate points to origin (center of mass at origin)
    translated_x = [x - centroid_x for x in x_list]
    translated_y = [y - centroid_y for y in y_list]

    # Rotation matrix
    rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                                [np.sin(angle_radians),  np.cos(angle_radians)]])

    # Rotate points
    rotated_points = [np.dot(rotation_matrix, [x, y]) for x, y in zip(translated_x, translated_y)]

    # Translate points back
    rotated_x_list = [point[0] + centroid_x for point in rotated_points]
    rotated_y_list = [point[1] + centroid_y for point in rotated_points]

    return rotated_x_list, rotated_y_list

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def my_interpolate(x_list, y_list, clockwise=False):

# == translating into native point class for easier calculation
  points = []
  for i in range(len(x_list)):
    points.append(Point(x_list[i], y_list[i]))

# ===============================================
  if TEXT_DEBUG:
    print('Points:')
    for point in points:
      print(f'{point}')
    print('')

# == needed definitions =========================
  def Anchor(i):
    return points[np.clip(i, 0, len(points)//2)*2+1]
  def Control(i):
    return points[np.clip(i, 0, len(points)//2)*2]
# ===============================================

  if TEXT_DEBUG:
    for i in range(len(points)//2):
      print(f'#{i+1}:\nC:{Control(i)}\nA:{Anchor(i)}\n')

  equation = []

  # going from one control and anchor to the next pair
  for i in range(len(points)//2-1):
    if TEXT_DEBUG:
      print(f'#{i+1}:\nC:{Control(i)}  ->  C:{Control(i+1)}\nA:{Anchor(i)}      A:{Anchor(i+1)}\n')

    if PLOT_DEBUG:
      plot.pair(Anchor(i), Control(i), i)

# == find the angles for the matching tangents ==
    center1 = Control(i)
    edge1 = Anchor(i)
    r1 = find.dist(center1, edge1)

    center2 = Control(i+1)
    edge2 = Anchor(i+1)
    r2 = find.dist(center2, edge2)

    d = find.dist(center1, center2)

    theta = np.arctan2(center2.y - center1.y, center2.x - center1.x)

    if abs(r1 - r2) > d:  # Check if external tangents exist
      print("No external tangents exist")
      return []
    phi = np.arccos((r1 - r2) / d)

    angle = (theta + phi) if clockwise else (theta - phi)

# == store the values for the equation ==========
    # point on circle 1
    x1 = center1.x + r1 * np.cos(angle)
    y1 = center1.y + r1 * np.sin(angle)

    # point on circle 2
    x2 = center2.x + r2 * np.cos(angle)
    y2 = center2.y + r2 * np.sin(angle)

    tan_start, tan_end = Point(x1, y1), Point(x2, y2)

    equation.append((center1, r1,
                     find.angle(center1, edge1),     # theta_start
                     find.angle(center1, tan_start), # theta_end
                     clockwise))
    equation.append((tan_start, tan_end))
    equation.append((center2, r2,
                     find.angle(center2, tan_end), # theta_start
                     find.angle(center2, edge2),   # theta_end
                     clockwise))

# ===============================================
    if PLOT_DEBUG:
      plot.point(tan_start)
      plot.point(tan_end)

  if PLOT_DEBUG:
    plot.pair(Anchor(len(points)//2-1), Control(len(points)//2-1), i,)

  if TEXT_DEBUG:
    for i in range(len(equation)):
      if i % 3 == 1:
        print(f'{i}) == line =======================\ntan_start: {equation[i][0]}\n  tan_end: {equation[i][1]}\n')
      else:
        print(f'{i}) == arc ========================\n     center: {equation[i][0]}\n          r: {equation[i][1]}\ntheta_start: {equation[i][2]}\n  theta_len: {equation[i][3]}\n')

  return equation

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def my_function(t, equation, num_points=1000):
    # Generate a sequence of t values
    values = np.linspace(0, len(equation) - 0.001, num_points)

    # Initialize lists to store the x and y coordinates
    x_coords, y_coords = [], []

    # Calculate points along the path
    for i in values:
        point = find.t(i, equation)
        x_coords.append(point.x)
        y_coords.append(point.y)

    # Plot the path
    plt.plot(x_coords, y_coords, 'g-')  # 'b-' specifies a blue line

    #plot.point(find.t(t, equation), color='black')

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Scenario:
  def __init__(self, x, y, c, a):
    self.x_list = x
    self.y_list = y
    self.clockwise = c
    self.angle = a

def main():

  #True is clockwise
  #False is counter-clockwise
  #angle in degrees to rotate the points before interpolating them with our method

  # given points
  Scenarios = [
    # Report Cover Image
    Scenario(
      x=[1, 3, 5, 6, 8, 10, 12, 13, 15, 17, 18, 20],
      y=[2, 1, 3, 4, 3, 5, 4, 6, 5, 7, 6, 8],
      c=False,
      a=0
    ),


    #NON-ROTATED - DEMONSTRATION SEQUENCES

    Scenario(
      [0, 2, 3, 5, 6, 9], # Demonstration point set #1
      [2, 1, 0, 1, 2, 0],
      True,
      0
    ),
    Scenario(
      [0, 1, 2, 4, 5, 6], # Demonstration point set #2
      [0, 1, 2, 4, 3, 1],
      True,
      0
    ),
    Scenario(
      [0, 1, 2, 4, 5, 9, 10], # Demonstration point set #3 (odd number of points, so invalid input)
      [2, 1, 2, 5, 6, 5, 5],
      True,
      0
    ),
    Scenario(
      [0, 1, 2, 3, 4, 5, 6, 7], # Demonstration point set #4
      [0, 0, 0, 0, 2, 0, 0, 0],
      True,
      0
    ),
    Scenario(
      [0, 1, 2, 4, 6, 7, 9, 10], # Demonstration point set #5
      [5, 2, 1, 0, 1, 3, 4, 2],
      True,
      0
    ),

    # ROTATED  - DEMONSTRATION SEQUENCE 5
    Scenario(
      [0, 1, 2, 4, 6, 7, 9, 10], # Demonstration point set #5, 30 degrees
      [5, 2, 1, 0, 1, 3, 4, 2],
      True,
      30
    ),
    Scenario(
      [0, 1, 2, 4, 6, 7, 9, 10], # Demonstration point set #5, 60 degrees
      [5, 2, 1, 0, 1, 3, 4, 2],
      True,
      60
    ),
    Scenario(
      [0, 1, 2, 4, 6, 7, 9, 10], # Demonstration point set #5, 180 degrees
      [5, 2, 1, 0, 1, 3, 4, 2],
      True,
      180
    ),

    # Showcase 1
    Scenario(
      x=[0, 1, 2.4, 3.4, 4.8, 5.8, 7.2, 8.2, 9.6, 10.6, 12.0, 13.0, 14.4, 15.4, 16.8, 17.8],
      y=[0, 0.4, 1.8, 2.2, 0.8, 1.2, 2.6, 3.0, 1.6, 2.0, 3.4, 3.8, 2.4, 2.8, 4.2, 4.6],
      c=True,
      a=0
    ),

    # Showcase 2
    Scenario(
      x=[2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 18, 20],
      y=[1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8],
      c=True,
      a=0
    ),

    # Showcase 3
    Scenario(
      x=[3, 4, 6, 8, 10, 11, 13, 15, 16, 18, 19, 21],
      y=[0, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6],
      c=False,
      a=0
    ),

    # Showcase 4
    Scenario(
      x=[0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 16, 18],
      y=[1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 10, 9],
      c=True,
      a=0
    ),


  ]

  plt.grid(True)
  plt.axis('equal')  # Ensure the plot's aspect ratio is equal
  plt.xlabel('x')
  plt.ylabel('y')
  plt.tight_layout()

  for scenario in Scenarios:
    if len(scenario.x_list)%2 != 0:
      print('There needs to be an even number of points!')
      #raise ValueError('There needs to be an even number of points!')
      continue

    x_list, y_list = rotate_points(scenario.x_list, scenario.y_list, scenario.angle)

    if PLOT_DEBUG:
      points = []
      for i in range(len(scenario.x_list)):
        points.append(Point(x_list, y_list))


    equation = my_interpolate(x_list, y_list, scenario.clockwise)

    my_function(6, equation)

    plt.grid(True)
    plt.axis('equal')  # Ensure the plot's aspect ratio is equal
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-5, 25)
    plt.ylim(-6, 15)
    #plt.tight_layout()
    plt.show()


