import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate or load your dataset
x = np.linspace(0, 10, 100)  # Example x-coordinates
y = 2*x + 1 + np.random.randn(*x.shape)  # Example y-coordinates with some noise

# Step 2: Fit a best-fit line (least-squares method)
slope, intercept = np.polyfit(x, y, 1)  # 1 indicates a linear fit

# Step 3: Use the slope and intercept to reconstruct the y-values
y_reconstructed = slope*x + intercept

# Calculate deltas between original and reconstructed y-values
deltas = y - y_reconstructed

# Print datasets side by side in table format
print(" X     | Original Y | Reconstructed Y | Delta")
print("-------|------------|-----------------|-------")
for xi, yi, yi_reconstructed, delta in zip(x, y, y_reconstructed, deltas):
    print(f"{xi:5.2f} | {yi:10.2f} | {yi_reconstructed:15.2f} | {delta:5.2f}")

# Visualization
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'o', label='Original Data')
plt.plot(x, y_reconstructed, 'r', label='Best-fit Line')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data Compression using Best-fit Line')
plt.show()

# Evaluate the fit
mse = np.mean((y - y_reconstructed)**2)
print(f"\nMean Squared Error (MSE) between original and reconstructed data: {mse:.4f}")
