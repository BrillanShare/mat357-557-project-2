import numpy as np
import matplotlib.pyplot as plt

def plot_circle(center, edge_point, radius, ax, label, center_color='r'):
    circle = plt.Circle(center, radius, fill=False, label=label, linestyle='dotted')
    ax.add_artist(circle)
    ax.plot(center[0], center[1], 'o', color=center_color)  # Center point
    ax.plot(edge_point[0], edge_point[1], 'o', color=center_color)  # Edge point

def plot_arc_to_tangent(center, radius, start_point, tangent_point, ax, color='g'):
    start_angle = np.arctan2(start_point[1] - center[1], start_point[0] - center[0])
    end_angle = np.arctan2(tangent_point[1] - center[1], tangent_point[0] - center[0])
    if start_angle > end_angle:
        end_angle += 2 * np.pi
    angles = np.linspace(start_angle, end_angle, 100)
    x_arc = center[0] + radius * np.cos(angles)
    y_arc = center[1] + radius * np.sin(angles)
    ax.plot(x_arc, y_arc, color=color, linewidth=2)

def find_external_tangents(c1, r1, c2, r2):
    d = np.linalg.norm(np.array(c2) - np.array(c1))
    theta = np.arctan2(c2[1] - c1[1], c2[0] - c1[0])
    phi = np.arccos((r1 - r2) / d)
    angles = [theta + phi, theta - phi]
    tangents = []
    for angle in angles:
        x1 = c1[0] + r1 * np.cos(angle)
        y1 = c1[1] + r1 * np.sin(angle)
        x2 = c2[0] + r2 * np.cos(angle)
        y2 = c2[1] + r2 * np.sin(angle)
        tangents.append(((x1, y1), (x2, y2)))
    return tangents

points = [(3, 3), (1, 5), (10, 6), (12, 7), (12, 1), (13, 2)]
fig, ax = plt.subplots(figsize=(10, 10))

radii = []
center_colors = ['b', '#800080', '#FFC0CB']  # Blue for C0, Purple for C2, Pink for C4
for i, center_color in zip(range(0, len(points), 2), center_colors):
    center = points[i]
    edge = points[i + 1]
    radius = np.sqrt((center[0] - edge[0])**2 + (center[1] - edge[1])**2)
    radii.append(radius)
    plot_circle(center, edge, radius, ax, f'Circle {(i//2)+1}', center_color=center_color)

# Tangent lines and arcs between C0 and C2
tangents_C0_C2 = find_external_tangents(points[0], radii[0], points[2], radii[1])
for i, tangent in enumerate(tangents_C0_C2):
    linestyle = '-' if i == 0 else '--'
    ax.plot([tangent[0][0], tangent[1][0]], [tangent[0][1], tangent[1][1]], color='red', linestyle=linestyle)

# Ensure the arc on C0 starts from P1 and goes clockwise to the tangent point
plot_arc_to_tangent(points[0], radii[0], points[1], tangents_C0_C2[0][0], ax)

# Arc on C2 from the tangent point to P3, ensuring it's clockwise
plot_arc_to_tangent(points[2], radii[1], tangents_C0_C2[0][1], points[3], ax)

# Tangent lines and arcs between C2 and C4, ensuring the arc on C4 is clockwise
tangents_C2_C4 = find_external_tangents(points[2], radii[1], points[4], radii[2])

for tangent in tangents_C2_C4:
    ax.plot([tangent[0][0], tangent[1][0]], [tangent[0][1], tangent[1][1]], 'r-')

plot_arc_to_tangent(points[4], radii[2], tangents_C2_C4[0][1], points[5], ax)

# Set plot details
ax.set_aspect('equal')

# Adjust limits
xmin, xmax, ymin, ymax = ax.axis()
x_range = xmax - xmin
y_range = ymax - ymin
ax.axis([xmin - 0.5 * x_range, xmax + 0.5 * x_range, ymin - 0.5 * y_range, ymax + 0.5 * y_range])

plt.xlabel('x')
plt.ylabel('y')
plt.title('Circles, Points, Connecting Lines, and Arcs')

# Set legend position
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.grid(True)

# Adjust layout and show plot
plt.tight_layout()
plt.show()