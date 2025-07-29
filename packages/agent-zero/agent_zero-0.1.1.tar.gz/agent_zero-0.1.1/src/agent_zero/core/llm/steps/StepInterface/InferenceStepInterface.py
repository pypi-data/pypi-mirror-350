from abc import ABC, abstractmethod

from agent_zero.core.llm.steps.InferenceStepDebugObjects import time_process


class InferenceStepInterface(ABC):
    def __init__(self, step_name: str, stage_name: str, step_type: str):
        self.output_type = None
        self.input_type = None
        self.step_name = step_name
        self.stage_name = stage_name
        self.step_type = step_type
        self.inputs = []
        self.outputs = []
        self.metrics = []
        self.attributes = []

    @time_process
    @abstractmethod
    def process(self, current_input, *args, **kwargs):
        pass

    def init_input(self, input_data: str | list, input_type: str):
        if input_type not in ("text", "messages", "json_object"):
            raise ValueError(f"input type: {input_type} NOT SUPPORTED")
        self.input_type = input_type
        self.inputs = input_data

    def init_output(self, output_instance: str | list, output_type: str):
        if output_type not in ("text", "chunks", "messages", "json_object"):
            raise ValueError(f"output type: {output_type} NOT SUPPORTED")
        self.output_type = output_type
        self.outputs = output_instance

    def add_output(self, output_instance: dict | list):
        if isinstance(output_instance, list):
            self.outputs.extend(output_instance)
        else:
            self.outputs.append(output_instance)

    @abstractmethod
    def collect_metrics(self, *args):
        pass

    @abstractmethod
    def get_attributes(self) -> list:
        pass

    def collect_debug_info(self) -> dict:
        metrics = {
            "title": self.step_name,
            "stage": self.stage_name,
            "type": self.step_type,
            "inputs": {"type": self.input_type,
                       "value": self.inputs},
            "outputs": {"type": self.output_type,
                        "value": self.outputs},
            "metrics": self.metrics,
            "attributes": self.get_attributes()
        }
        return metrics
