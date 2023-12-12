import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the expected amount of data loss
def calculate_data_loss(total_length, fsync_frequency, crash_times):
    """Calculate the expected data loss for given crash times and fsync frequency."""
    fsync_interval = int(total_length * fsync_frequency)
    data_losses = []

    for crash_time in crash_times:
        # Calculate the amount of data written since the last fsync
        last_fsync_time = (crash_time // fsync_interval) * fsync_interval
        data_loss = crash_time - last_fsync_time
        data_losses.append(data_loss)

    return np.mean(data_losses)

# Parameters for the calculation
total_length = 1048576  # 1 MB
fsync_frequencies = [.01, .05, .10, .15, .20]  # Frequencies of fsync calls
num_crashes = 10  # Number of simulated crashes


adjusted_normal_crash_times = np.random.normal(loc=total_length / 2, scale=total_length / 2, size=num_crashes)
adjusted_normal_crash_times = np.clip(adjusted_normal_crash_times, 0, total_length)

# Creating more variability in the random distribution
adjusted_random_crash_times = np.random.random(size=num_crashes) * total_length

# Uniform distribution with random spacing to increase variability
adjusted_uniform_crash_times = np.sort(np.random.uniform(0, total_length, num_crashes))

# Calculating expected data loss in MB
def calculate_data_loss_mb(total_length, fsync_frequency, crash_times):
    data_loss_bytes = calculate_data_loss(total_length, fsync_frequency, crash_times)
    return data_loss_bytes / (1024 * 1024)  # Convert bytes to MB

# Calculating expected data loss for each distribution and fsync frequency
expected_data_losses_adjusted_random = [calculate_data_loss_mb(total_length, freq, adjusted_random_crash_times) for freq in fsync_frequencies]
expected_data_losses_adjusted_uniform = [calculate_data_loss_mb(total_length, freq, adjusted_uniform_crash_times) for freq in fsync_frequencies]
expected_data_losses_adjusted_normal = [calculate_data_loss_mb(total_length, freq, adjusted_normal_crash_times) for freq in fsync_frequencies]

# Plotting the expected data loss for different distributions and fsync frequencies
plt.figure(figsize=(12, 6))

# Plot for adjusted random distribution
plt.subplot(1, 3, 1)
plt.plot(fsync_frequencies, expected_data_losses_adjusted_random, marker='o', color='red')
plt.xlabel('Fsync Increments')
plt.ylabel('Expected Data Loss (MB)')
plt.title('Random Distribution')
plt.xticks(fsync_frequencies)
plt.grid(True)

# Plot for adjusted uniform distribution
plt.subplot(1, 3, 2)
plt.plot(fsync_frequencies, expected_data_losses_adjusted_uniform, marker='o', color='blue')
plt.xlabel('Fsync Increments')
plt.ylabel('Expected Data Loss (MB)')
plt.title('Uniform Distribution')
plt.xticks(fsync_frequencies)
plt.grid(True)

# Plot for adjusted normal distribution
plt.subplot(1, 3, 3)
plt.plot(fsync_frequencies, expected_data_losses_adjusted_normal, marker='o', color='green')
plt.xlabel('Fsync Increments')
plt.ylabel('Expected Data Loss (MB)')
plt.title('Normal Distribution')
plt.xticks(fsync_frequencies)
plt.grid(True)

plt.tight_layout()
plt.show()