import numpy as np
import matplotlib.pyplot as plt

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

def process_stream(real_time_data, epsilon):
    """Process the incoming data stream with dynamic polynomial fitting."""
    x_vals, y_vals = [], []
    coefficients = []
    previous_fit = None
    color_index = 0  # Toggle between color pairs

    # Define color pairs for alternating between segments
    colors = [('blue', 'orange'), ('green', 'magenta')]

    for t, y in real_time_data:
        x_vals.append(t)
        y_vals.append(y)

        if len(x_vals) >= 4:  # We need at least 4 points to fit a cubic polynomial
            poly = np.polyfit(x_vals, y_vals, 3)  # Fit a third-degree polynomial
            current_fit = np.polyval(poly, x_vals)

            # Check if the fit exceeds the epsilon or it's the first fit
            if previous_fit is not None and np.max(np.abs(previous_fit - current_fit[-len(previous_fit):])) > epsilon:
                coefficients.append(poly)
                data_color, fit_color = colors[color_index]
                plt.plot(x_vals, y_vals, 'o', markersize=3, color=data_color)
                plt.plot(x_vals, current_fit, color=fit_color)
                x_vals, y_vals = [x_vals[-1]], [y_vals[-1]]  # Start new segment with the last point
                previous_fit = np.polyval(poly, [x_vals[0]])
                color_index = 1 - color_index  # Toggle color index for next segment
            elif previous_fit is None:
                previous_fit = current_fit

    # Plot the last segment if not empty
    if len(x_vals) > 3:
        poly = np.polyfit(x_vals, y_vals, 3)
        coefficients.append(poly)
        current_fit = np.polyval(poly, x_vals)
        data_color, fit_color = colors[color_index]
        plt.plot(x_vals, y_vals, 'o', markersize=3, color=data_color)
        plt.plot(x_vals, current_fit, color=fit_color)

    plt.xlabel('Time (t)')
    plt.ylabel('Pressure (Pa)')
    plt.title('Real-time Polynomial Fitting on Time-Series Data')
    plt.show()
    return coefficients

# Generate and process the data
time, pressure = generate_data(1000)
epsilon = calculate_epsilon(pressure)
real_time_data = zip(time, pressure)
coefficients = process_stream(real_time_data, epsilon)
