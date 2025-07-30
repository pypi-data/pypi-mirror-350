import time
import sys


class StepTracker:
    def __init__(self, visualizer=None):
        self.steps = []
        self.visualizer = visualizer
        self.start_time = None
        self.end_time = None
        self.total_memory = 0

    def start(self, data):
        self.start_time = time.perf_counter()
        self.total_memory += sys.getsizeof(data)

    def log(self, index, value, target, match):
        self.steps.append({
            'index': index,
            'value': value,
            'target': target,
            'match': match
        })
        self.total_memory += sys.getsizeof(index) + sys.getsizeof(value) + sys.getsizeof(match)

    def end(self):
        self.end_time = time.perf_counter()

    def print_steps(self):
        print("\n--- Step-by-Step Trace ---")
        for i, step in enumerate(self.steps, 1):
            print(f"Step {i}: Checked index {step['index']} → "
                  f"Value = {step['value']} | "
                  f"Target = {step['target']} | "
                  f"{'MATCH' if step['match'] else 'NO MATCH'}")

    def print_summary(self):
        total_time = self.end_time - self.start_time if self.end_time else 0
        print("\n--- Benchmark Summary ---")
        print(f"Total comparisons: {len(self.steps)}")
        print(f"Estimated space used: {self.total_memory} bytes")
        print(f"Execution time: {total_time:.6f} seconds")

    def visualize(self):
        if self.visualizer:
            self.visualizer.visualize(self.steps)
