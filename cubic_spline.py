import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

def cubic_spline():
    # Constants
    g = 9.81  # Acceleration due to gravity (m/s^2)

    # Input points (x_i, y_i) - Replace these with your actual points
    x_i = np.array([0, 1, 2, 3, 4, 5])  # x-coordinates
    y_i = np.array([10, 8, 5, 7, 3, 0])  # y-coordinates (elevation)

    # Ensure the starting point is the highest for maximum potential energy
    y_0 = np.max(y_i)

    # Cubic spline interpolation
    cs = CubicSpline(x_i, y_i)

    # Define a function for the rollercoaster ride f(x)
    def f(x):
        return cs(x)

    # Define a function to calculate "fun" (velocity squared) based on elevation difference
    def fun(x):
        return 2 * g * (y_0 - f(x))

    # Plotting
    x_vals = np.linspace(x_i[0], x_i[-1], 1000)
    y_vals = f(x_vals)
    fun_vals = fun(x_vals)

    plt.figure(figsize=(14, 6))

    # Plot the rollercoaster track
    plt.subplot(1, 2, 1)
    plt.plot(x_vals, y_vals, label='Rollercoaster Track')
    plt.scatter(x_i, y_i, color='red')  # Plot the original points
    plt.title('Rollercoaster Track')
    plt.xlabel('Distance')
    plt.ylabel('Elevation')
    plt.legend()

    # Plot the "fun" over the track
    plt.subplot(1, 2, 2)
    plt.plot(x_vals, fun_vals, label='"Fun" (Velocity Squared)', color='green')
    plt.title('"Fun" Along the Track')
    plt.xlabel('Distance')
    plt.ylabel('"Fun" (Velocity Squared)')
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    cubic_spline()
