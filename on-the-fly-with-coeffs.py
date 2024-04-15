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


def process_stream(real_time_data, epsilon, poly_degree, enable_plotting=True):
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

        if len(x_vals) >= poly_degree + 1:  # We need at least poly_degree + 1 points to fit a polynomial
            poly = np.polyfit(x_vals, y_vals, poly_degree)  # Fit a polynomial of degree poly_degree
            current_fit = np.polyval(poly, x_vals)

            if previous_fit is not None and np.max(np.abs(previous_fit - current_fit[-len(previous_fit):])) > epsilon:
                coefficients.append(poly)
                if enable_plotting:
                    data_color, fit_color = colors[color_index]
                    plt.plot(x_vals, y_vals, 'o', markersize=3, color=data_color)
                    plt.plot(x_vals, current_fit, color=fit_color)
                x_vals, y_vals = [x_vals[-1]], [y_vals[-1]]  # Start new segment with the last point
                previous_fit = np.polyval(poly, [x_vals[0]])
                color_index = 1 - color_index  # Toggle color index for next segment
            elif previous_fit is None:
                previous_fit = current_fit

    # Close final segment
    if len(x_vals) > poly_degree:
        poly = np.polyfit(x_vals, y_vals, poly_degree)
        coefficients.append(poly)
        current_fit = np.polyval(poly, x_vals)
        if enable_plotting:
            data_color, fit_color = colors[color_index]
            plt.plot(x_vals, y_vals, 'o', markersize=3, color=data_color)
            plt.plot(x_vals, current_fit, color=fit_color)

    if enable_plotting:
        plt.xlabel('Time (t)')
        plt.ylabel('Pressure (Pa)')
        plt.title('Real-time Polynomial Fitting on Time-Series Data')
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



