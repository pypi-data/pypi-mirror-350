import time
from agent_zero.core.llm.steps.InferenceStepDebugObjects import time_process
from agent_zero.core.llm.steps.StepInterface.LLMCallStepInterface import LLMCallStepInterface


class AsyncLLMCallStepBase(LLMCallStepInterface):

    @time_process
    async def process(self) -> (str, list | None):
        start_time = time.time()

        answer = await self.llm.async_call_llm(messages=self.messages,
                                               temperature=self.temperature,
                                               max_tokens=self.max_tokens,
                                               top_p=self.top_p,
                                               response_type=self.response_type,
                                               tools=self.tools,
                                               tool_choice=self.tool_choice,
                                               parallel_tool_calls=self.parallel_tool_calls)

        self.collect_metrics(None, None)
        self.metrics.extend(
            [
                {"key": "time", "value": round(time.time() - start_time, 4)}
            ]
        )
        if not answer.get('content'):
            answer['content'] = ""

        self.init_input(self.messages, "messages")
        self.init_output([answer], "messages")

        tool_calls = answer.get('tool_calls')

        return answer['content'], tool_calls
