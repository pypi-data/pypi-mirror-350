from unittest.mock import patch

import examples.company_name_w_decorator as example
from conflux.handlers import OpenAiLLM

llm_call_count = 0


def openai_llm_init_side_effect(self, *args, **kwargs):
    self.role = "llm"


async def company_name_openai_llm_process_side_effect(hanlder, msg, chain):
    global llm_call_count
    if llm_call_count == 0:
        llm_call_count += 1
        return "The Sock Spot"
    else:
        return "The Sock Spot: Step into Comfort"


def test_company_name_w_decorator():
    global llm_call_count
    llm_call_count = 0
    with patch.object(OpenAiLLM, "__init__", openai_llm_init_side_effect):
        with patch(
            "conflux.handlers.OpenAiLLM.process",
            company_name_openai_llm_process_side_effect,
        ):
            example.main()
