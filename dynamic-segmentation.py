import numpy as np
import matplotlib.pyplot as plt

# Seed the RNG for reproducibility
np.random.seed(42)

STANDARD_ATMOSPHERIC_PRESSURE = 1013

def generate_data(num_points):
    """Simulate time-series data for atmospheric pressure (random walk)."""
    time = np.linspace(0, 10, num_points)
    # Begin the random walk at the standard atmospheric pressure
    pressure = np.cumsum(np.random.normal(0, 0.1, num_points)) + STANDARD_ATMOSPHERIC_PRESSURE
    return time, pressure


def calculate_epsilon(percent_tolerance, y_values):
    """Calculate the residual error bound epsilon."""
    return percent_tolerance * (np.max(y_values) - np.min(y_values))


def calc_residual_error(x, y, coefficients):
    # Evaluate the polynomial at the x values
    fitted_y = np.polyval(coefficients, x)

    # Calculate the squared differences
    squared_errors = (y - fitted_y) ** 2

    # Calculate the residual sum of squares (RSS)
    RSS = np.sum(squared_errors)

    return RSS


def process_stream(real_time_data, error_bound_epsilon, poly_degree, enable_plotting=True):
    """Process the incoming data stream with dynamic polynomial fitting."""

    # temp storage for read data awaiting curve fitting
    t_vals_of_open_segment, y_vals_of_open_segment = [], []
    curr_fitted_curve_open_segment = None

    fitted_curves_closed_segments = []

    color_index = 0  # Toggle between contrasting color pairs

    # Define contrasting color pairs for alternating between segments
    colors = [('blue', 'orange'), ('green', 'magenta')]

    for t, y in real_time_data:
        t_vals_of_open_segment.append(t)
        y_vals_of_open_segment.append(y)

        # We need at least poly_degree + 1 points to fit a polynomial
        if len(t_vals_of_open_segment) < poly_degree + 1:
            # Not enough data points yet to attempt a curve fit
            assert curr_fitted_curve_open_segment is None, "There should NOT be a previous fitted curve."
            continue

        if len(t_vals_of_open_segment) == poly_degree + 1:
            # The current open segment just got enough data points to attempt a curve fit
            assert curr_fitted_curve_open_segment is None, "There should NOT be a previous fitted curve."
            curr_fitted_curve_open_segment = np.polyfit(t_vals_of_open_segment, y_vals_of_open_segment, poly_degree)

            # TODO: Hopefully an exceptional case:
            # TODO: Handle the possibility that the *initial* curve fit attempt fails
            # TODO: (the resulting residual error is not within epsilon)

        else:
            # The current open segment already had a fitted curve
            assert len(t_vals_of_open_segment) > poly_degree + 1, "Only remaining conditional possibility."
            assert curr_fitted_curve_open_segment is not None, "There should be a previous fitted curve."

            residual_error_of_curr_fit = calc_residual_error(t_vals_of_open_segment, y_vals_of_open_segment, curr_fitted_curve_open_segment)
            max_allowable_error_for_curr_fit = len(t_vals_of_open_segment) * error_bound_epsilon ** 2

            if residual_error_of_curr_fit > max_allowable_error_for_curr_fit:
                # The new data point causes the current fit to exceed the error bound. We must attempt a refit.
                candidate_refitted_curve_open_segment = np.polyfit(t_vals_of_open_segment, y_vals_of_open_segment, poly_degree)
                residual_error_of_curr_fit = calc_residual_error(t_vals_of_open_segment, y_vals_of_open_segment, candidate_refitted_curve_open_segment)

                if residual_error_of_curr_fit > max_allowable_error_for_curr_fit:
                    # rip. The new data point also causes the refitted curve to exceed the error bound...
                    # So we must close the existing open segment and begin a new open segment for the new data point.

                    # First, plot the curve for the segment that is about to be closed along with
                    # the points that correspond to it:
                    if enable_plotting:
                        data_color, fit_color = colors[color_index]
                        plt.plot(t_vals_of_open_segment, y_vals_of_open_segment, 'o', markersize=3, color=data_color)
                        current_fit_evaluated_y_vals = np.polyval(curr_fitted_curve_open_segment, t_vals_of_open_segment)
                        plt.plot(t_vals_of_open_segment, current_fit_evaluated_y_vals, color=fit_color)
                        color_index = 1 - color_index  # Toggle color index for next segment

                    fitted_curves_closed_segments.append(curr_fitted_curve_open_segment)
                    curr_fitted_curve_open_segment = None
                    # TODO: Store the starting t value for each polynomial piece along with its corresponding
                    # TODO: set of coefficients. (So we can find the correct polynomial for a value of t.)

                    # Clear out points that correspond to the segment that we just closed
                    t_vals_of_open_segment.clear()
                    y_vals_of_open_segment.clear()

                    # Begin the new segment with the point that couldn't be added to the segment we just closed
                    t_vals_of_open_segment.append(t)
                    y_vals_of_open_segment.append(y)
                    # Note that we can't attempt a curve fit again until we have at least (poly_degree + 1)
                    # data points in the open segment.

                else:
                    # The new data point with the refitted curve is within the error bound, so keep the refitted curve
                    curr_fitted_curve_open_segment = candidate_refitted_curve_open_segment


    # TODO: how does the paper code handle any remaining points still waiting in the open segment?

    # TODO: Close the final open segment, if there is one
    # if len(t_vals_of_open_segment) > poly_degree:
    #     curve_fit = np.polyfit(t_vals_of_open_segment, y_vals_of_open_segment, poly_degree)
    #     fitted_curves_closed_segments.append(curve_fit)
    #     GPT_current_fit = np.polyval(curve_fit, t_vals_of_open_segment)
    #     if enable_plotting:
    #         data_color, fit_color = colors[color_index]
    #         plt.plot(t_vals_of_open_segment, y_vals_of_open_segment, 'o', markersize=3, color=data_color)
    #         plt.plot(t_vals_of_open_segment, GPT_current_fit, color=fit_color)

    if enable_plotting:
        plt.xlabel('Time (t)')
        plt.ylabel('Pressure (Pa)')
        plt.title('Real-time Polynomial Fitting on Time-Series Data')
        plt.show()

    return fitted_curves_closed_segments


def main():
    # Generate and process the data
    times, pressures = generate_data(50)
    epsilon = calculate_epsilon(0.1, pressures)
    simulated_real_time_data = zip(times, pressures)
    poly_degree = 2  # Set the degree k of the polynomial here
    all_fitted_curves = process_stream(simulated_real_time_data, epsilon, poly_degree, enable_plotting=True)


if __name__ == "__main__":
    main()



