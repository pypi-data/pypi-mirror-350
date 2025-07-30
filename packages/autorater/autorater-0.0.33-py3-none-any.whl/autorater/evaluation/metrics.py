class PairwiseMetric:
    def __init__(self, name="pairwise_metric"):
        self.name = name
        print(f"Initialized {self.name}")

    def calculate_dummy_score(self):
        # Placeholder for actual metric calculation
        return 0.75

class PointwiseMetric:
    def __init__(self, name="pointwise_metric"):
        self.name = name
        print(f"Initialized {self.name}")

    def calculate_dummy_score(self):
        # Placeholder for actual metric calculation
        return 0.90
