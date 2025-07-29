from agent_zero.core.llm.steps.StepInterface.InferenceStepInterface import InferenceStepInterface


class PhantomStep(InferenceStepInterface):

    def collect_metrics(self, *args):
        pass

    def get_attributes(self) -> list:
        pass

    def __init__(self, step_name: str, stage_name: str, step_type: str = 'phantom step'):
        super().__init__(step_name, stage_name, step_type)

    def process(self, current_input, *args, **kwargs):
        pass

    def collect_debug_info(self) -> dict:
        metrics = {
            "title": self.step_name,
            "stage": self.stage_name,
            "type": self.step_type,
            "inputs": {"value": self.inputs, "type": self.input_type},
            "outputs": {"value": self.outputs, "type": self.output_type},
            "metrics": [],
            "attributes": []
        }
        return metrics
