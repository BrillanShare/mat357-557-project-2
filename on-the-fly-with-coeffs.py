import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Seed the RNG for reproducibility
np.random.seed(42)


def generate_data(num_points):
    """Simulate time-series data for atmospheric pressure (random walk)."""
    time = np.linspace(0, 10, num_points)
    pressure = np.cumsum(np.random.normal(0, 0.1, num_points)) + 1013  # Start around standard atmospheric pressure
    return time, pressure


def calculate_epsilon(pressure):
    """Calculate the residual error bound epsilon."""
    return 0.1 * (np.max(pressure) - np.min(pressure))


def process_stream(real_time_data, epsilon, poly_degree, enable_plotting=True):
    """Process the incoming data stream with dynamic polynomial fitting."""

    fig, ax = plt.subplots()
    if enable_plotting:
        line, = ax.plot([], [], 'o', markersize=3, label='Data Points')  # Initialize empty plot for data points
        line_fit, = ax.plot([], [], label='Polynomial Fit')  # Initialize empty plot for polynomial fit
        plt.legend()
        plt.xlabel('Time (t)')
        plt.ylabel('Pressure (Pa)')
        plt.title('Real-time Polynomial Fitting on Time-Series Data')

    x_vals, y_vals = [], []
    coefficients = []
    previous_fit = None
    color_index = 0  # Toggle between color pairs

    # Define color pairs for alternating between segments
    colors = [('blue', 'orange'), ('green', 'magenta')]

    def update(frame):
        t, y = frame
        x_vals.append(t)
        y_vals.append(y)

        if len(x_vals) >= poly_degree + 1:  # We need at least poly_degree + 1 points to fit a polynomial
            poly = np.polyfit(x_vals, y_vals, poly_degree)
            current_fit = np.polyval(poly, x_vals)

            if previous_fit is None or np.max(np.abs(previous_fit - current_fit[-len(previous_fit):])) > epsilon:
                coefficients.append(poly)
                line.set_data(x_vals, y_vals)
                line_fit.set_data(x_vals, current_fit)
                ax.relim()  # Recompute the ax.dataLim
                ax.autoscale_view()  # Update ax.viewLim using the new dataLim
                # Reset for the next segment
                return line, line_fit
            elif previous_fit is None:
                previous_fit = current_fit

        return line, line_fit

    if enable_plotting:
        ani = FuncAnimation(fig, update, frames=real_time_data, blit=True, repeat=False)
        plt.show()

    return coefficients



def main():
    # Generate and process the data
    time, pressure = generate_data(1000)
    epsilon = calculate_epsilon(pressure)
    real_time_data = zip(time, pressure)
    poly_degree = 3  # Set the degree of the polynomial here
    coefficients = process_stream(real_time_data, epsilon, poly_degree, enable_plotting=True)


if __name__ == "__main__":
    main()



