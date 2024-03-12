import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.animation import FuncAnimation

# Constants
g = 9.81  # Acceleration due to gravity in m/s^2
m_initial = 500  # Initial mass of the coaster car in kg
v_initial = 0  # Initial speed of the car at the first point in m/s


def chatgpt_sandbox(mass, initial_speed):
    print('chatgpt_sandbox\n')

    # Points defining the rollercoaster track
    points_int = [(0, 20), (2, 15), (4, 18), (6, 12), (8, 20), (10, 9), (12, 11), (14, 6), (16, 3), (18, 0)]

    # Cubic spline interpolation
    x_i, y_i = zip(*points_int)
    cs = CubicSpline(x_i, y_i)

    # Find local maxima (for the analysis, not needed for the animation)
    cs_prime = cs.derivative()
    cs_double_prime = cs_prime.derivative()
    roots = np.sort(cs_prime.roots())  # Ensure roots are in ascending order
    local_maxima = [root for root in roots if cs_double_prime(root) < 0 and min(x_i) < root < max(x_i)]

    # Highest local maximum (for the analysis, not needed for the animation)
    highest_local_max = max(local_maxima, key=lambda x: cs(x), default=0)

    # Initial and required potential energy calculations (for the analysis, not needed for the animation)
    initial_potential_energy = mass * g * cs(0)
    max_potential_energy_required = mass * g * cs(highest_local_max)
    cutoff_speed = np.sqrt(2 * (
                max_potential_energy_required - initial_potential_energy) / mass) if max_potential_energy_required > initial_potential_energy else 0
    total_initial_energy = initial_potential_energy + 0.5 * mass * initial_speed ** 2
    can_make_it = total_initial_energy >= max_potential_energy_required

    # Analysis results (not part of the animation)
    if can_make_it:
        print(
            f"The car with initial speed {initial_speed} m/s can make it to the end. (Cutoff speed: {cutoff_speed:.3f} m/s)")
    else:
        speed_deficit = cutoff_speed - initial_speed
        print(
            f"The car with initial speed {initial_speed} m/s cannot make it. It needs to start at least {speed_deficit:.3f} m/s faster (Min starting speed to make it: {cutoff_speed:.3f} m/s).")

    # Setup for animation
    fig, ax = plt.subplots()
    ax.plot(x_i, y_i, 'ro', label='Points')  # Plot the original points
    x_fine = np.linspace(min(x_i), max(x_i), 1000)
    ax.plot(x_fine, cs(x_fine), 'b-', label='Cubic Spline')  # Plot the spline
    car, = ax.plot([], [], 'go', markersize=10)  # Car marker, starting as empty
    ax.set_title('Rollercoaster Animation with Initial Speed')
    ax.set_xlabel('Distance')
    ax.set_ylabel('Elevation')
    ax.legend()
    ax.grid(True)

    def init():
        # Initialize the car marker position
        car.set_data([], [])
        return car,

    def animate(t):
        # Update the car marker position along the spline
        x = x_fine[int(t * len(x_fine) / 100)]  # Scale t to traverse the x_fine array
        y = cs(x)
        car.set_data(x, y)
        return car,

    # Create the animation
    ani = FuncAnimation(fig, animate, frames=100, init_func=init, blit=True, interval=50)
    ani.save('animation.gif', writer='pillow')

    plt.show()


# Initial check with the default mass and initial speed
chatgpt_sandbox(m_initial, v_initial)
