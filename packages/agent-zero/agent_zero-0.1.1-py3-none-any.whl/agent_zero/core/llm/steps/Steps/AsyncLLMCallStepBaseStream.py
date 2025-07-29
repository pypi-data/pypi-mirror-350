import json
import re
import time
from typing import AsyncGenerator

from openai.types.chat import ChatCompletionChunk

from agent_zero.core.llm.steps.InferenceStepDebugObjects import time_process
from agent_zero.core.llm.steps.StepInterface.LLMCallStepInterface import LLMCallStepInterface
from agent_zero.helpers import get_current_timestamp


class AsyncLLMCallStepBaseStream(LLMCallStepInterface):

    @time_process
    async def process(self) -> AsyncGenerator[ChatCompletionChunk, ChatCompletionChunk]:
        start_time = time.time()

        print("LLM Request: ", get_current_timestamp(), len(json.dumps(self.messages)) / 4, flush=True)
        ttft_time, ttfs_time, prompt_tokens, completion_tokens = 0, 0, 0, 0
        is_first_token_generated = False
        is_first_sentence_complete = False
        accumulated_text = ''

        generator = self.llm.async_call_llm_stream(
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            tools=self.tools,
            tool_choice=self.tool_choice,
            parallel_tool_calls=self.parallel_tool_calls
        )

        async for answer_part in generator:
            delta = answer_part.choices[0].delta
            answer_text = getattr(delta, "content", "") or ""

            accumulated_text += answer_text

            # Record TTFT (Time to First Token)
            if not is_first_token_generated:
                ttft_time = round(time.time() - start_time, 4)
                is_first_token_generated = True

            # Detect the first complete sentence and record TTFS (Time to First Sentence)
            if not is_first_sentence_complete:
                if re.search(r'[.!?](?:\s|$)', accumulated_text):
                    ttfs_time = round(time.time() - start_time, 4)
                    is_first_sentence_complete = True
            prompt_tokens = self.estimate_tokens_from_messages(self.messages)
            if usage := answer_part.usage:
                prompt_tokens = usage.prompt_tokens
                completion_tokens = usage.completion_tokens
            else:
                yield answer_part

        self.collect_metrics(f"{prompt_tokens} / {completion_tokens}", None)

        self.init_input(self.messages, "messages")
        self.init_output([], "messages")

        self.metrics.extend(
            [
                {"key": "TTFT", "value": ttft_time},
                {"key": "TTFS", "value": ttfs_time},
                {"key": "time", "value": round(time.time() - start_time, 4)}
            ]
        )

    def estimate_tokens_from_messages(self, messages):
        # Function to estimate tokens for each message content
        def estimate_tokens(message_content):
            word_count = len(message_content.split())  # Count words
            estimated_tokens = word_count / 0.75  # Estimate tokens based on words
            return round(estimated_tokens)

        total_tokens = 0

        # Loop through each message in the list
        for message in messages:
            # Count tokens for message content
            content_tokens = estimate_tokens(message["content"] if "content" in message else "")
            
            # Add approximately 2 tokens for the 'role' (e.g., 'user' or 'assistant')
            role_tokens = 2

            # Sum up the tokens for this message
            total_tokens += content_tokens + role_tokens

        return total_tokens