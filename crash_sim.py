import os
import random
import string
import numpy as np
import matplotlib.pyplot as plt
import os



def perform_write_simulation(fsync_frequencies, total_length, num_iterations):
    """
    Perform an actual write simulation where data is written to a file and fsync is called at specified frequencies.
    Only one random crash per iteration is simulated, and the average data loss is calculated.

    :param fsync_frequencies: List of fsync frequencies to test
    :param total_length: Total length of data to write (in bytes)
    :param num_iterations: Number of iterations to run the simulation
    :return: Dictionary of average data losses for each fsync frequency
    """
    average_data_losses = {freq: [] for freq in fsync_frequencies}
    file_path = "simulation_file.dat"

    for freq in fsync_frequencies:
        fsync_interval = int(total_length * freq)
        iteration_losses = []

        for _ in range(num_iterations):
            with open(file_path, "wb") as file:
                # Write data and call fsync at intervals
                for i in range(0, total_length, fsync_interval):
                    # Write up to fsync_interval bytes
                    write_size = min(fsync_interval, total_length - i)
                    file.write(os.urandom(write_size))
                    file.flush()  # Ensure data is written from internal buffer to OS buffer
                    os.fsync(file.fileno())  # Ensure data is written to disk from OS buffer

                # Simulate crash by getting a random crash time
                crash_time = np.random.randint(0, total_length)
                last_fsync_time = (crash_time // fsync_interval) * fsync_interval
                data_loss = crash_time - last_fsync_time
                iteration_losses.append(data_loss)

            # Clean up the file after each iteration
            os.remove(file_path)

        average_loss = np.mean(iteration_losses)
        average_data_losses[freq].append(average_loss / (1024 * 1024))  # Convert bytes to MB

    return average_data_losses

total_length = 1048576  # 1 MB
fsync_frequencies = [.01, .05, .10, .15, .20]  # Frequencies of fsync calls
num_iterations = 100

# Perform the actual write simulation and get average data losses
average_data_losses_actual_write = perform_write_simulation(fsync_frequencies, total_length, num_iterations)

# Plotting the average data loss for different fsync frequencies
plt.figure(figsize=(8, 6))

# Convert dictionary to lists for plotting
frequencies_actual_write = list(average_data_losses_actual_write.keys())
average_losses_actual_write = [loss[0] for loss in average_data_losses_actual_write.values()]

plt.plot(frequencies_actual_write, average_losses_actual_write, marker='o', linestyle='-')
plt.xlabel('Fsync Increments')
plt.ylabel('Average Data Loss (MB)')
plt.title('Average Data Loss vs Fsync Frequency')
plt.xticks(frequencies_actual_write)
plt.grid(True)

plt.show()
