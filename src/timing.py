import time

class Timing:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start_time = time.time()
        print(f"Starting {self.name}...")

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        print(f"Finished {self.name}. {self.end_time - self.start_time:.2f} seconds")