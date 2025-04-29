import time

class Metrics:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.total_latency = 0.0
        self.request_count = 0

    def record_latency(self, latency_seconds: float):
        self.total_latency += latency_seconds
        self.request_count += 1

    def record_success(self):
        self.success_count += 1

    def record_failure(self):
        self.failure_count += 1

    def average_latency(self):
        if self.request_count == 0:
            return 0.0
        return self.total_latency / self.request_count

    def success_rate(self):
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return self.success_count / total

metrics = Metrics()
