class PairwiseMetricPromptTemplate:
    def __init__(self, template_string="Compare [input_A] with [input_B] based on [criterion]."):
        self.template_string = template_string
        print(f"Initialized PairwiseMetricPromptTemplate with template: '{self.template_string}'")

    def format(self, **kwargs):
        # In a real scenario, this would format the template with actual data
        return self.template_string.format(**kwargs)

class PointwiseMetricPromptTemplate:
    def __init__(self, template_string="Evaluate [input] based on [criterion]."):
        self.template_string = template_string
        print(f"Initialized PointwiseMetricPromptTemplate with template: '{self.template_string}'")

    def format(self, **kwargs):
        # In a real scenario, this would format the template with actual data
        return self.template_string.format(**kwargs)
