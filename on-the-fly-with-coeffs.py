import numpy as np
import matplotlib.pyplot as plt


# Seed the RNG for reproducibility
np.random.seed(42)


def generate_data(num_points):
    """ Simulate time-series data for atmospheric pressure (random walk). """
    time = np.linspace(0, 10, num_points)
    pressure = np.cumsum(np.random.normal(0, 0.1, num_points)) + 1013  # Start around standard atmospheric pressure
    return time, pressure


def process_stream(segment_size):
    """ Process the incoming data stream with piecewise polynomial fitting using least squares """
    # Generate data
    time, pressure = generate_data(1000)
    coefficients = []

    # Color settings for alternating
    colors = [('blue', 'orange'), ('green', 'magenta')]  # Pair of colors for data points and fits
    color_index = 0  # Toggle between color pairs

    for i in range(0, len(time), segment_size):
        # Segment the data
        x_vals = time[i:i + segment_size]
        y_vals = pressure[i:i + segment_size]

        if len(x_vals) == segment_size:
            # Fit a polynomial using least squares
            poly = np.polyfit(x_vals, y_vals, 3)  # Third-degree polynomial
            coefficients.append(poly)

            # Optionally, plot each segment's fit
            data_color, fit_color = colors[color_index]
            plt.plot(x_vals, y_vals, 'o', markersize=2, color=data_color, label='Data Points' if i == 0 else "")
            plt.plot(x_vals, np.polyval(poly, x_vals), color=fit_color, label='Polynomial Fit' if i == 0 else "")
            color_index = 1 - color_index  # Toggle color index for next segment

    plt.xlabel('Time (t)')
    plt.ylabel('Pressure (Pa)')
    plt.title('Piecewise Polynomial Fitting on Time-Series Data')
    plt.legend()
    plt.show()
    return coefficients


# Use a segment size of 50 data points
coefficients = process_stream(50)
