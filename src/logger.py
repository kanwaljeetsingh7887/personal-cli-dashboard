import csv
import os

def log_stats(filepath, stats):
    header = ['timestamp', 'cpu', 'memory', 'disk']
    exists = os.path.exists(filepath)
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow([stats['timestamp'], stats['cpu'], stats['memory'], stats['disk']])
