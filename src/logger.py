import csv
import os

def log_stats(filepath, stats):
    """
    Logs system stats including CPU, memory, disk, battery, and charging to a CSV file.
    Creates the CSV with a header if it doesn't exist.
    """
    header = ['timestamp', 'cpu', 'memory', 'disk', 'battery', 'charging']
    exists = os.path.exists(filepath)

    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)

        # Write header if file doesn't exist
        if not exists:
            writer.writerow(header)

        # Write stats row
        writer.writerow([
            stats['timestamp'],
            stats['cpu'],
            stats['memory'],
            stats['disk'],
            stats.get('battery', 'N/A'),
            stats.get('charging', 'N/A')
        ])
