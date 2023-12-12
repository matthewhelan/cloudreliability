import os
import time
import threading
import random
import string

# Shared variable to control the running of threads
run_threads = True

# Threading locks
file_lock = threading.Lock()
print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    """Thread-safe print function."""
    with print_lock:
        print(*args, **kwargs)

def generate_random_string(length):
    """Generates a random string of the specified length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def write_data_to_file(file_path, length):
    """Generates and writes random data to a file, respecting the file lock."""
    while run_threads:
        data = generate_random_string(length) + '\n'
        with file_lock:
            with open(file_path, 'a') as file:
                file.write(data)
        time.sleep(5)

def simulate_fsync(file_path):
    """Simulates the fsync() call and measures its duration, acquiring the lock during operation."""
    while run_threads:
        with file_lock:
            start_time = time.time()
            with open(file_path, 'a') as file:
                os.fsync(file.fileno())
            end_time = time.time()
            duration = end_time - start_time
            safe_print(f"fsync() duration: {duration:.5f} seconds")
        time.sleep(10)

def start_thread(target_function, *args):
    """Starts a thread with the given target function and arguments."""
    thread = threading.Thread(target=target_function, args=args, daemon=True)
    thread.start()
    return thread

# Example usage
file_path = 'example_data.txt'

# Start the threads
fsync_thread = start_thread(simulate_fsync, file_path)
write_thread = start_thread(write_data_to_file, file_path, 1000000)

# Example to stop the threads after some time (e.g., 60 seconds)
time.sleep(30)
run_threads = False

# Wait for threads to finish
fsync_thread.join()
write_thread.join()

safe_print("All threads have completed.")