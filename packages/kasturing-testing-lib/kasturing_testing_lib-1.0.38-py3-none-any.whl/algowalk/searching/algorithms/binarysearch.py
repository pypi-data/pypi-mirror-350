from algowalk.core.algorithm_base import AlgorithmBase

class LinearSearch(AlgorithmBase):
    def __init__(self, target):
        self.target = target
        self.steps = []

    def run(self, data):
        self.steps.clear()
        for i, val in enumerate(data):
            self.steps.append(f"Checking index {i}: {val}")
            if val == self.target:
                self.steps.append(f"Found at index {i}")
                return i
        self.steps.append("Not found")
        return -1

    def get_steps(self):
        return self.steps