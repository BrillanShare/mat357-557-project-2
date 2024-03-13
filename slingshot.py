import numpy as np
from matplotlib import patches
import matplotlib.pyplot as plt

CIRCLE_DEBUG = False
TANGENT_DEBUG = False
ARC_DEBUG = False
BREAK_ON_EXIT = False

fig, ax = plt.subplots(figsize=(10, 10))

def plot_circle(center, edge_point, radius, ax, label, center_color='r'):
    circle = plt.Circle(center, radius, fill=False, label=label, linestyle='dotted')
    ax.add_artist(circle)
    ax.plot(center[0], center[1], 'o', color=center_color)  # Center point
    ax.plot(edge_point[0], edge_point[1], 'o', color=center_color)  # Edge point


def plot_arc_on_circle(center, radius, start_point, end_point, ax, arc_color='g'):
    # find the angle in degrees
    start_angle = np.rad2deg(np.arctan2(start_point[1] - center[1], start_point[0] - center[0]))
    end_angle = np.rad2deg(np.arctan2(end_point[1] - center[1], end_point[0] - center[0]))

    # Make sure that start angle is less than end angle
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle

    # Creating arc
    arc = patches.Arc(center, 2*radius, 2*radius, theta1=start_angle, theta2=end_angle,
              edgecolor=arc_color, linewidth=2)

    ax.add_patch(arc)

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

def setup_plot():
    global fig, ax
    fig, ax = plt.subplots(figsize=(10, 10))

def configure_plot_and_show():
    # Set plot details
    ax.set_aspect('equal')

    # Adjust limits
    xmin, xmax, ymin, ymax = ax.axis()
    x_range = xmax - xmin
    y_range = ymax - ymin
    ax.axis([xmin - 0.5 * x_range, xmax + 0.5 * x_range, ymin - 0.5 * y_range, ymax + 0.5 * y_range])
    ax.axis([-4, 20, -4, 12])

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Circles, Points, Connecting Lines, and Arcs')

    # Set legend position
    # TODO: Restore legend (had to disable when factored out this function
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.grid(True)

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()

def main():
    points = [(3, 3), (1, 5), (10, 6), (12, 7), (12, 1), (13, 2)]

    radii = []
    center_colors = ['b', '#800080', '#FFC0CB']  # Colors for C0, C2, C4
    for i, center_color in zip(range(0, len(points), 2), center_colors):
        center = points[i]
        edge = points[i + 1]
        radius = np.sqrt((center[0] - edge[0])**2 + (center[1] - edge[1])**2)
        radii.append(radius)
        if CIRCLE_DEBUG:
            setup_plot()
        plot_circle(center, edge, radius, ax, f'Circle {(i//2)+1}', center_color=center_color)
        if CIRCLE_DEBUG:
            configure_plot_and_show()
            breakpoint()

    # Tangent lines and arcs between C0 and C2
    tangents_C0_C2 = find_external_tangents(points[0], radii[0], points[2], radii[1])
    for i, tangent in enumerate(tangents_C0_C2):
        linestyle = '-' if i == 0 else '--'
        if TANGENT_DEBUG:
            setup_plot()
        ax.plot([tangent[0][0], tangent[1][0]], [tangent[0][1], tangent[1][1]], color='red', linestyle=linestyle)
        if TANGENT_DEBUG:
            configure_plot_and_show()
            breakpoint()

    # Adjusting the arc on C0 to start from P1 and go clockwise to the tangent point
    if ARC_DEBUG:
        setup_plot()
    plot_arc_on_circle(points[0], radii[0], points[3], tangents_C0_C2[0][0], ax)
    if ARC_DEBUG:
        configure_plot_and_show()
        breakpoint()


    if ARC_DEBUG:
        setup_plot()
        # Arc on C2 from the tangent point to P3, ensuring it's clockwise
    plot_arc_on_circle(points[2], radii[1], tangents_C0_C2[0][1], points[3], ax)
    if ARC_DEBUG:
        configure_plot_and_show()
        breakpoint()

    # Tangent lines and arcs between C2 and C4, ensuring the arc on C4 is clockwise
    tangents_C2_C4 = find_external_tangents(points[2], radii[1], points[4], radii[2])
    for tangent in tangents_C2_C4:
        if TANGENT_DEBUG:
            setup_plot()
        ax.plot([tangent[0][0], tangent[1][0]], [tangent[0][1], tangent[1][1]], 'r-')
        if TANGENT_DEBUG:
            configure_plot_and_show()
            breakpoint()

    if ARC_DEBUG:
        setup_plot()
    plot_arc_on_circle(points[4], radii[2], tangents_C2_C4[0][1], points[5], ax)
    if ARC_DEBUG:
        configure_plot_and_show()
        breakpoint()

    configure_plot_and_show()

    if BREAK_ON_EXIT:
        breakpoint()

if __name__ == "__main__":
    # Execute main() only if the script is run directly, not if it's imported as a module
    main()



