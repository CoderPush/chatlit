# mock_openai.py

import time
from collections import namedtuple
import random


def start_choice():
    return {"delta": {"role": "assistant"}, "finish_reason": None, "index": 0}


def stop_choice():
    return {"delta": {}, "finish_reason": "stop", "index": 0}


class MockChatCompletion:
    @classmethod
    def create(cls, model, messages, stream=False, pl_tags=None):
        response_template = {
            "id": "mocked_openai_id",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "usage": {
                "prompt_tokens": len(messages),
                "completion_tokens": len(messages),
            },
            "choices": [
                {"delta": {"role": "assistant", "content": "This is a mock response."}}
            ],
        }

        if stream:
            mock_response = "You're seeing a mock response so that we can avoid paying API fees under development."

            # generate mock_responses to be an array of words from full_response
            mock_chunks = mock_response.split()

            response_template["choices"][0] = start_choice()
            yield response_template

            for content in mock_chunks:
                time.sleep(0.4)  # simulate delay
                response_template["choices"][0]["delta"]["content"] = (
                    content + " "
                )  # Set 'delta' content
                yield response_template

            response_template["choices"][0] = stop_choice()
            yield response_template
        else:
            time.sleep(0.5)  # simulate delay
            yield namedtuple("Struct", response_template.keys())(
                *response_template.values()
            )


class MockCompletion:
    @classmethod
    def create(cls, engine, prompt, temperature, max_tokens):
        # generate a mock title with a random number
        mock_title = f"Convo {random.randint(0, 1000)}"
        response = {
            "id": "mocked_openai_id",
            "object": "text.completion",
            "created": int(time.time()),
            "model": engine,
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": max_tokens,
            },
            "choices": [{"text": mock_title}],
        }
        return response


class MockOpenAI:
    ChatCompletion = MockChatCompletion
    Completion = MockCompletion
