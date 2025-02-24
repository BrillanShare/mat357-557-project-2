import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def generate_data(num_points):
    """ Simulate time-series data for atmospheric pressure (random walk). """
    time = np.linspace(0, 10, num=num_points)
    pressure = np.cumsum(np.random.normal(0, 0.1, num_points)) + 1013  # Start around standard pressure
    return time, pressure


def fit_polynomial(x, y, degree=3):
    """ Fit a polynomial of given degree to the data. """
    polynomial_features = PolynomialFeatures(degree=degree)
    x_poly = polynomial_features.fit_transform(x.reshape(-1, 1))
    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly)
    return y_poly_pred


def plot_data(time, pressure, pressure_fit):
    """ Plot the original data and the fitted polynomial curve. """
    plt.figure(figsize=(10, 5))
    plt.plot(time, pressure, label='Actual Pressure')
    plt.plot(time, pressure_fit, label='Fitted Curve', color='red')
    plt.title('Piecewise Polynomial Curve Fitting for Time-Series Data')
    plt.xlabel('Time')
    plt.ylabel('Atmospheric Pressure')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    # Generate simulated atmospheric pressure data
    time, pressure = generate_data(1000)

    # Segment the data (simple segmentation by number of points for demonstration)
    segment_size = 100
    pressure_fit = np.array([])
    for start in range(0, len(time), segment_size):
        end = min(start + segment_size, len(time))
        segment_fit = fit_polynomial(time[start:end], pressure[start:end], degree=2)
        pressure_fit = np.concatenate((pressure_fit, segment_fit))

    # Plotting the fitted data
    plot_data(time, pressure, pressure_fit)


if __name__ == "__main__":
    main()
