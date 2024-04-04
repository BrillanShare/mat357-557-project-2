import numpy as np
import math
import matplotlib.pyplot as plt
from types import SimpleNamespace as Namespace

CIRCLE_DEBUG = False
TANGENT_DEBUG = False
ARC_DEBUG = False
BREAK_ON_EXIT = True


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
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.grid(True)

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()


# == Custom point class ==========================================
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


# ================================================================

# == Custom pair class ===========================================
class Pair:
    def __init__(self, anchor, control):
        self.anchor = anchor
        self.control = control


# ================================================================

# ================================================================
class find:
    @staticmethod
    def dist(p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    @staticmethod
    def angle(center, edge):
        return math.degrees(math.atan2(edge.y - center.y, edge.x - center.x))

    @staticmethod
    def arc_degree(center, anchor, tan_p, clockwise=False):
        # Calculate angles in radians from the center to each point
        angle1_rad = np.arctan2(anchor.y - center.y, anchor.x - center.x)
        angle2_rad = np.arctan2(tan_p.y - center.y, tan_p.x - center.x)

        if clockwise:
            # For clockwise, if angle1 is less than angle2, it needs to wrap around
            if angle1_rad < angle2_rad:
                angle1_rad += 2 * np.pi
                # Convert the angle difference from radians to degrees
            return np.degrees(angle1_rad - angle2_rad)
        else:
            # For counterclockwise, if angle2 is less than angle1, it needs to wrap around
            if angle2_rad < angle1_rad:
                angle2_rad += 2 * np.pi
                # Convert the angle difference from radians to degrees
            return np.degrees(angle2_rad - angle1_rad)

    @staticmethod
    def tangents(center1, edge1, center2, edge2, internal=False):
        r1 = find.dist(center1, edge1)
        r2 = find.dist(center2, edge2)
        d = find.dist(center1, center2)

        # angle of the line connecting the centers of the circles
        # currently called alpha in desmos
        theta = np.arctan2(center2.y - center1.y, center2.x - center1.x)

        if internal:
            if r1 + r2 > d:  # Check if internal tangents exist
                print("No internal tangents exist")
                return []
            phi = np.arccos((r1 + r2) / d)
        else:
            if abs(r1 - r2) > d:  # Check if external tangents exist
                print("No external tangents exist")
                return []
            phi = np.arccos((r1 - r2) / d)

        angles = [theta + phi, theta - phi]
        tangents = []

        for angle in angles:
            if internal:
                x1 = center1.x + r1 * np.cos(angle)
                y1 = center1.y + r1 * np.sin(angle)
                x2 = center2.x - r2 * np.cos(angle)
                y2 = center2.y - r2 * np.sin(angle)
            else:
                x1 = center1.x + r1 * np.cos(angle)
                y1 = center1.y + r1 * np.sin(angle)
                x2 = center2.x + r2 * np.cos(angle)
                y2 = center2.y + r2 * np.sin(angle)

            tangents.append((Point(x1, y1), Point(x2, y2)))

        return tangents


# ================================================================
class plot:
    @staticmethod
    def point(point, label='', offset=(0.1, 0.1), color='blue'):
        plt.plot(point.x, point.y, 'o', zorder=3, color=color)
        if label:  # Check if label is not empty
            plt.text(point.x + offset[0], point.y + offset[1], label, zorder=3, color='red')

    @staticmethod
    def line(p1, p2, mode='--', color='blue'):
        if p2.x == p1.x:
            plt.vlines(x=p1.x, ymin=p1.y, ymax=p2.y, color=color)
        else:
            m = (p2.y - p1.y) / (p2.x - p1.x)
            b = p1.y - m * p1.x
            x_values = np.linspace(p1.x, p2.x, 100)
            plt.plot(x_values, m * x_values + b, mode, color=color)

    @staticmethod
    def circle(center, edge):
        r = find.dist(center, edge)
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center.x + r * np.cos(theta)
        y = center.y + r * np.sin(theta)
        plt.plot(x, y, ':', color='grey')

    @staticmethod
    def arc(center, start_point, end_point, clockwise=False):
        r = find.dist(center, start_point)  # Assume the radius is the same for start and end points

        # Get angles in degrees and then convert to radians
        start_angle_rad = np.radians(find.angle(center, start_point))
        end_angle_rad = np.radians(find.angle(center, end_point))

        # Adjust for clockwise or counterclockwise direction
        if clockwise:
            if start_angle_rad <= end_angle_rad:
                start_angle_rad += 2 * np.pi
        else:
            if end_angle_rad <= start_angle_rad:
                end_angle_rad += 2 * np.pi

        # Generate theta values considering the direction
        theta = np.linspace(start_angle_rad, end_angle_rad, 100, endpoint=True)

        # Calculate the x and y coordinates of the points on the arc
        x = center.x + r * np.cos(theta)
        y = center.y + r * np.sin(theta)

        plt.plot(x, y, '-g')  # Plot the arc with a green solid line

    @staticmethod
    def pair(anchor, control, number=0, show_circle=True):
        plot.line(anchor, control)
        plot.point(control, f'c{number}' if number > 0 else '')
        plot.point(anchor, f'a{number}' if number > 0 else '')
        if show_circle: plot.circle(control, anchor)


fig, ax = plt.subplots(figsize=(10, 10))


# ================================================================


def main():
    plot_debug = False  # show extra information

    # == starting conditions =========================================
    clockwise = False

    Points = [Point(1, 2), Point(4, 6),
              Point(-5, -4), Point(-4, -3),
              Point(1, 0), Point(0, 1)]

    Points = [Point(-20, 5), Point(-20, 14),
              Point(10, -15), Point(10, -10),
              Point(-5, 15), Point(-5, 22),
              Point(18, 18), Point(18, 22)]

    if len(Points) % 2 != 0:
        raise ValueError('There needs to be an even number of points!')
    # == needed definitions ==========================================
    tan_start, tan_end = Point(0, 0), Point(0, 0)

    def Anchor(i):
        return Points[np.clip((i - 1), 0, len(Points) // 2) * 2 + 1]

    def Control(i):
        return Points[np.clip((i - 1), 0, len(Points) // 2) * 2]




    anchor_zero = Anchor(0)
    control_zero = Control(0)

    # Looks like this is designed to be 1-based...
    # further, instead of crashing, 0 gives the same result as 1...that is confusing

    anchor_one = Anchor(1)
    control_one = Control(1)

    anchor_two = Anchor(2)
    control_two = Control(2)

    anchor_three = Anchor(3)
    control_three = Control(3)

    anchor_four = Anchor(4)
    control_four = Control(4)

    # out of range:
    # anchor_five = Anchor(5)
    # control_five = Control(5)


    # ================================================================

    print(f'{len(Points)} =========')
    for i in range(1, len(Points) // 2):
        print(f'{i}:Anchor{Anchor(i)} and Control{Control(i)} -> Anchor{Anchor(i + 1)} and Control{Control(i + 1)}')
        # == plot starting info ==========================================
        # with debug off, plots (in blue) and labels (in red) circle centers, circle edge points, and the radius connecting them
        # with debug on, also plots the circle in light gray
        plot.pair(Anchor(i), Control(i), i, plot_debug)
        plot.pair(Anchor(i + 1), Control(i + 1), i + 1, plot_debug)
        #note: the above double-draws all circles except for the first one and the last one

        # == find tangents ===============================================
        external_tangents = find.tangents(Control(i), Anchor(i), Control(i + 1), Anchor(i + 1), internal=False)
        internal_tangents = find.tangents(Control(i), Anchor(i), Control(i + 1), Anchor(i + 1), internal=True)

        if plot_debug:
            for line in external_tangents:
                plot.line(line[0], line[1])
            for line in internal_tangents:
                plot.line(line[0], line[1])

        # == find the tangent point in the corisponding direction ========
        c = 0 if clockwise else 1

        arc_deg_ext = find.arc_degree(Control(i), Anchor(i), external_tangents[c][0], clockwise)
        arc_deg_int = find.arc_degree(Control(i), Anchor(i), internal_tangents[c][0], clockwise)
        if arc_deg_ext < arc_deg_int:
            tan_start, tan_end = external_tangents[c][0], external_tangents[c][1]
        else:
            tan_start, tan_end = internal_tangents[c][0], internal_tangents[c][1]
        # == use the point to plot the line ==============================
        plot.arc(Control(i), Anchor(i), tan_start, clockwise) #
        plot.line(tan_start, tan_end, '-', 'g')
        # if inner was used, then flip
        if arc_deg_ext > arc_deg_int:
            clockwise = not clockwise
        plot.arc(Control(i + 1), tan_end, Anchor(i + 1), clockwise)

        if plot_debug:
            plot.point(tan_start)
            plot.point(tan_end)
    # ================================================================

    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Execute main() only if the script is run directly, not if it's imported as a module
    main()
