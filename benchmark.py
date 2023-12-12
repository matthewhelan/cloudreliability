import os
import random
import string
import time
import matplotlib.pyplot as plt
import numpy as np

def generate_random_string(length):
    """Generates a random string of the specified length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def write_data_with_variable_flush_frequency(file_path, total_length, fsync_frequency):
    """Writes data to a file and flushes based on a given frequency of total write."""
    fsync_times = []  # List to store the duration of each flush
    start_time = time.time()
    fsync_interval = int(total_length * fsync_frequency)

    with open(file_path, 'a') as file:
        characters_written = 0
        while characters_written < total_length:
            remaining_chars = total_length - characters_written
            data = generate_random_string(min(fsync_interval, remaining_chars))
            file.write(data)
            characters_written += len(data)

            if characters_written % fsync_interval == 0 or characters_written >= total_length:
                fsync_start = time.time()
                os.fsync(file.fileno())  # Force write to disk
                fsync_end = time.time()
                fsync_times.append(fsync_end - fsync_start)

    total_time = time.time() - start_time
    return fsync_times, total_time

# Parameters for the experiment
total_length = 1048576 # 1 MB
fsync_frequencies = [0.01, 0.05, 0.10, 0.15, 0.20]  # Frequencies of fsync calls
repetitions = 100

# Running the experiment
results = {}
for fsync_frequency in fsync_frequencies:
    experiment_data = {'fsync_times': [], 'total_times': []}
    for _ in range(repetitions):
        file_path = f'example_data_{fsync_frequency}.txt'
        os.remove(file_path) if os.path.exists(file_path) else None
        fsync_times, total_time = write_data_with_variable_flush_frequency(file_path, total_length, fsync_frequency)
        experiment_data['fsync_times'].extend(fsync_times)
        experiment_data['total_times'].append(total_time)
    results[fsync_frequency] = experiment_data

# Print or process the results
for fsync_frequency, value in results.items():
    print(f"Fsync Frequency: {fsync_frequency*100}%, Fsync Times: {value['fsync_times']}, Total Times: {value['total_times']}")


# Prepare data for plotting
fsync_frequencies_percent = [freq * 100 for freq in fsync_frequencies]
average_fsync_times = [np.mean(data['fsync_times']) for data in results.values()]
average_total_times = [np.mean(data['total_times']) for data in results.values()]

overall_fsync_times = [average_fsync_times[i] * (1 / freq) for i, freq in enumerate(fsync_frequencies)]

# Plotting average fsync times
plt.figure(figsize=(12, 6))

# Plot for average fsync times per operation
plt.subplot(1, 2, 1)
plt.bar(fsync_frequencies_percent, average_fsync_times, color='blue')
plt.xlabel('Fsync Increments (% of total write)')
plt.ylabel('Average Fsync Time per Operation (s)')
plt.title('Average Fsync Time per Operation vs Fsync Frequency')
plt.xticks(fsync_frequencies_percent)

# Plot for overall fsync times
plt.subplot(1, 2, 2)
plt.bar(fsync_frequencies_percent, overall_fsync_times, color='green')
plt.xlabel('Fsync Increments (% of total write)')
plt.ylabel('Overall Fsync Time (s)')
plt.title('Overall Fsync Time vs Fsync Frequency')
plt.xticks(fsync_frequencies_percent)

plt.tight_layout()
plt.show()
