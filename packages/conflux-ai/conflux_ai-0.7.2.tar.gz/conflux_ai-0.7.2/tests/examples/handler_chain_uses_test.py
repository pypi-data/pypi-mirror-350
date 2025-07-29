from unittest.mock import patch

import examples.handler_chain_uses as example
from conflux.handlers import OpenAiLLM


def openai_llm_init_side_effect(self, *args, **kwargs):
    self.role = "llm"


async def dummy_openai_llm_process_side_effect(hanlder, msg, chain):
    return msg


def test_handler_chain_uses():
    with patch.object(OpenAiLLM, "__init__", openai_llm_init_side_effect):
        with patch(
            "conflux.handlers.OpenAiLLM.process", dummy_openai_llm_process_side_effect
        ):
            example.main()
