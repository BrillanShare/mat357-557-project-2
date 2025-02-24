import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial

# Step 1: Generate a simple dataset
x_all = np.linspace(0, 10, 100)  # Original x-coordinates
y_all = np.sin(x_all)  # Original y-coordinates, using a sine function for this example

# Step 2: Select a subset of points for interpolation
x_subset = x_all[::10]  # Select every 10th point for simplicity
y_subset = y_all[::10]

# Step 3: Use the subset to create a Lagrange polynomial
lagrange_poly = lagrange(x_subset, y_subset)
# The coefficients of the polynomial can be stored for "compression"
coefficients = Polynomial(lagrange_poly).coef

# Step 4: Use the stored coefficients to reconstruct the y-coordinates
reconstructed_y = np.polyval(coefficients[::-1], x_all)

# Step 5: Compare the original and reconstructed data
plt.figure(figsize=(10, 6))
plt.plot(x_all, y_all, label='Original Data')
plt.scatter(x_subset, y_subset, color='red', label='Selected Points for Interpolation')
plt.plot(x_all, reconstructed_y, label='Reconstructed Data', linestyle='--')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data Compression using Lagrange Polynomial Interpolation')
plt.show()

# Calculate and print the Mean Squared Error (MSE) between original and reconstructed data
mse = np.mean((y_all - reconstructed_y)**2)
print(f'Mean Squared Error (MSE) between original and reconstructed data: {mse:.4f}')
