class MetricPromptTemplateExamples:
    def __init__(self):
        self.examples = [
            {"input": "Example 1", "output": "Good"},
            {"input": "Example 2", "output": "Bad"}
        ]
        print("Initialized MetricPromptTemplateExamples")

    def get_example(self, index):
        return self.examples[index]

    def add_example(self, input_data, output_data):
        self.examples.append({"input": input_data, "output": output_data})
