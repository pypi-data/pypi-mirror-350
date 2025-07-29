import json
import os
from typing import Any, Callable, Iterable, Literal, TypeVar

from openai import AsyncOpenAI
from openai._utils import async_transform
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_content_part_param import (
    ChatCompletionContentPartParam,
)
from openai.types.chat.completion_create_params import CompletionCreateParams
from pydantic import BaseModel

from conflux import Handler, HandlerChain, Message
from conflux.base import handler
from conflux.exceptions import HandlerError
from conflux.mcp.client import ClientTransportType, MCPClient
from conflux.retrieval import Record, VectorDB


class OpenAiLLM(Handler):
    """Handler for generating a response using OpenAI's Language Model."""

    def __init__(
        self,
        role: str | None = None,
        model: str = "gpt-4o-mini",
        structure: type[BaseModel] | None = None,
        **openai_kwgs,
    ) -> None:
        self.role = role if role else "OpenAiLLM"
        self.model = model
        self.client = AsyncOpenAI(**openai_kwgs)
        self.structure = structure

    async def process(self, msg: Message, chain: HandlerChain) -> Message:
        """Generate a response using the message passed to this handler. If OpenAI api
        key is not set in the environment, then the api key can be passed as a variable
        in the HandlerChain.variables dictionary.

        Args:
            msg (Message): user response sent to OpenAI chatGPT.
            chain (HandlerChain): Casccade that this handler is a part of.

        Returns:
            Message: response from OpenAI chatGPT.
        """

        api_key = chain.variables.get("api_key", None)
        if api_key:
            self.client.api_key = api_key

        if msg.image:
            content = [
                {"type": "text", "text": str(msg)},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{msg.image}",
                        "detail": msg.info.get("image_detail", "auto"),
                    },
                },
            ]
        else:
            content = str(msg)

        # Add completion_config to the message if not already present
        completion_config = msg.info.get("completion_config", {})
        if "model" not in completion_config and self.model:
            completion_config["model"] = self.model
        if "response_format" in completion_config:
            structure = completion_config["response_format"]
            if not isinstance(structure, dict):
                self.structure = structure

        res = await self.request(completion_config, content)

        reply = ". ".join([str(ch.message.content) for ch in res.choices])
        if self.structure:
            response = Message(
                primary=reply,
                sender=self.role,
                openai_response=dict(res),
                structure=res.choices[0].message.parsed,  # type: ignore
            )
        else:
            response = Message(
                primary=reply, sender=self.role, openai_response=dict(res)
            )
        return response

    async def request(
        self,
        completion_config: dict,
        content: str | Iterable[ChatCompletionContentPartParam],
    ) -> ChatCompletion:
        if self.structure:
            completion_config["response_format"] = self.structure
            return await self.client.beta.chat.completions.parse(
                **completion_config,
                messages=[
                    {"role": "user", "content": content},
                ],
            )
        else:
            return await self.client.chat.completions.create(
                **completion_config,
                messages=[
                    {"role": "user", "content": content},
                ],
            )


class GeminiLLM(OpenAiLLM):
    def __init__(
        self,
        role: str | None = None,
        model: str = "gemini-2.5-flash-preview-05-20",
        structure: type[BaseModel] | None = None,
        **openai_kwgs,
    ) -> None:
        openai_kwgs["base_url"] = (
            "https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        api_key = os.getenv("GOOGLE_API_KEY")
        if "api_key" not in openai_kwgs and api_key:
            openai_kwgs["api_key"] = api_key
        super().__init__(role=role, model=model, structure=structure, **openai_kwgs)


class OpenRouterLLM(OpenAiLLM):
    def __init__(
        self,
        role: str | None = None,
        model: str = "anthropic/claude-sonnet-4",
        structure: type[BaseModel] | None = None,
        extra_headers: dict | None = None,
        extra_body: dict | None = None,
        **openai_kwgs,
    ) -> None:
        openai_kwgs["base_url"] = "https://openrouter.ai/api/v1"
        api_key = os.getenv("OPENROUTER_API_KEY")
        if "api_key" not in openai_kwgs and api_key:
            openai_kwgs["api_key"] = api_key
        self.extra_headers = extra_headers or {}
        self.extra_body = extra_body or {}
        super().__init__(role=role, model=model, structure=structure, **openai_kwgs)


class AssignRole(Handler):
    """Assign a role to the last message sent to this Handler by the current HandlerChain."""

    def __init__(self, role: str) -> None:
        self.role = role

    async def process(self, msg: Message, chain: HandlerChain) -> Message:
        return msg


class RetryHandlerChain(Handler):
    """Retry a HandlerChain until it produces some output before max_attempts.

    Args:
        sub_chain (HandlerChain): HandlerChain to be retried.
        max_attempts (int, optional): Maximum number of times to retry. Defaults to 3.
        role (str, optional): Role of the handler. Defaults to "RetryHandlerChain".
    """  # noqa: E501

    def __init__(
        self,
        sub_chain: HandlerChain,
        max_attempts: int = 3,
    ) -> None:
        self.role = "RetryHandlerChain"
        self.sub_chain = sub_chain
        self.max_attempts = max_attempts

    async def process(self, msg: Message, chain: HandlerChain) -> Message:
        attempts = 0

        while attempts < self.max_attempts:
            try:
                output = await self.sub_chain.run(msg)
                break
            except Exception as e:
                print(e)
                attempts += 1

        if attempts == self.max_attempts:
            raise HandlerError("RetryHandlerChain failed after max attempts")

        return output


class BatchInputOpenAiLLM(Handler):
    def __init__(
        self, role: str | None = None, model: str = "gpt-4o-mini", **openai_kwgs
    ) -> None:
        self.role = role if role else ""
        self.model = model
        # self.client = AsyncOpenAI(**openai_kwgs)

    async def process(self, msg: Message, chain: HandlerChain) -> str:
        """Generate a response using the message passed to this handler. If OpenAI api
        key is not set in the environment, then the api key can be passed as a variable
        in the HandlerChain.variables dictionary.

        Args:
            msg (Message): user response sent to OpenAI chatGPT.
            chain (HandlerChain): Casccade that this handler is a part of.

        Returns:
            Message: response from OpenAI chatGPT.
        """
        if not self.role:
            self.role = msg.sender

        if msg.image:
            content = [
                {"type": "text", "text": str(msg)},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{msg.image}",
                        "detail": msg.info.get("image_detail", "auto"),
                    },
                },
            ]
        else:
            content = str(msg)

        # Add completion_config to the message if not already present
        completion_config: dict = msg.info.get("completion_config", {})
        if "model" not in completion_config and self.model:
            completion_config["model"] = self.model

        messages = [{"role": "user", "content": content}]
        completion_config.update(messages=messages)
        # res = await self.client.chat.completions.create(
        #     **completion_config,
        #     messages=[
        #         {"role": "user", "content": content},
        #     ],
        # )
        data = await async_transform(
            completion_config,
            CompletionCreateParams,
        )

        # reply = ". ".join([str(ch.message.content) for ch in res.choices])
        # return Message(primary=reply, sender=self.role, openai_response=dict(res))

        assert "custom_id" in msg.info, (
            "unique id for the message is required in `info['custom_id']`"
        )
        line = {
            "custom_id": msg.info["custom_id"],
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": data,
        }
        line_s = json.dumps(line)
        return line_s


T = TypeVar("T", bound=Record)


class SimilarityRetriever(Handler):
    """Initialize a Retriever object.

    Args:
        index_db (VectorDB): The index database.
        k (int, optional): The number of records to retrieve. Defaults to 5.
        reranker (Callable[[list[Record]], list[Record]] | None, optional): The reranker function. Defaults to None.
        k_reranked (int, optional): The number of records to keep after reranking. Defaults to 3.
        join_policy (str | Callable[[list[Record]], str | Message], optional): The policy for joining the retrieved records. It can be a string or a callable function. Defaults to "\\\\n\\\\n".

            - If it is a string, the records will be joined using the string as a separator.
            - If it is a callable function, the function should accept a list of records and return a str or a Message.

    """

    role = "retriever"

    def __init__(
        self,
        index_db: VectorDB[T],
        k: int = 5,
        reranker: Callable[[Message, list[T]], list[T]] | None = None,
        k_reranked: int = 3,
        join_policy: str | Callable[[list[T]], str | Message] = "\n\n",
    ) -> None:
        self.index_db = index_db
        self.k = k
        self.join_policy = join_policy
        self.reranker = reranker
        self.k_reranked = k_reranked

    async def process(self, msg: Message, chain: HandlerChain) -> str | Message:
        """
        Process the given message and retrieve similar records.
        Args:
            msg (Message): The message to process.
            chain (HandlerChain): The handler chain.
        Returns:
            str | Message: The joined records as a string or a message.
        Raises:
            ValueError: If the join policy is invalid.
        """
        records = self.index_db.query(msg, k=self.k)
        chain.variables["query"] = msg
        chain.variables["records"] = records
        if self.reranker:
            records = self.reranker(msg, records)
            records = records[: self.k_reranked]
        if callable(self.join_policy):
            return self.join_policy(records)
        elif isinstance(self.join_policy, str):
            return self.join_policy.join(str(record) for record in records)
        else:
            raise ValueError("Invalid join policy.")


class SingleToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]


single_tool_call_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "SingleToolCall",
        "schema": {
            "type": "object",
            "properties": {
                "tool_name": {"type": "string"},
                "arguments": {"type": "object"},
            },
            "required": ["tool_name", "arguments"],
        },
    },
}


class ManyToolCalls(BaseModel):
    tool_calls: list[SingleToolCall]


many_tool_calls_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "ManyToolCalls",
        "schema": {
            "type": "object",
            "properties": {
                "tool_calls": {
                    "type": "array",
                    "items": single_tool_call_schema["json_schema"]["schema"],
                }
            },
            "required": ["tool_calls"],
        },
    },
}


class McpToolCall(Handler):
    role = "mcp_tool_call"

    def __init__(
        self,
        config: ClientTransportType,
        *,
        llm: type[Handler],
        tool_call_strategy: Literal["many", "single"] = "single",
        **llm_kwgs,
    ) -> None:
        self.config = config
        self.llm = llm
        self.client = MCPClient(config)
        self.tool_call_strategy = tool_call_strategy
        self.llm_kwgs = llm_kwgs

    async def single_tool_call(self, msg: Message) -> SingleToolCall:
        import json

        @handler
        async def prompt(msg: Message, chain: HandlerChain) -> str:
            prompt = "Given the following instruction, please call the correct tool with the correct arguments from the given list of tools. "
            prompt += f"# Instruction\n{msg}\n\n"
            prompt += "# Tools\n" + await self.client.list_tools()
            prompt += "\n\nCarefully choose the correct tool and arguments from the list of tools. "
            return prompt

        chain = prompt >> self.llm(structure=single_tool_call_schema, **self.llm_kwgs)  # type: ignore
        res = await chain.run(msg)
        return SingleToolCall(**json.loads(res.primary))

    async def many_tool_calls(self, msg: Message) -> ManyToolCalls:
        @handler
        async def prompt(msg: Message, chain: HandlerChain) -> str:
            prompt = "Given the following instruction, please call the correct tools with the correct arguments from the given list of tools. You can call multiple tools to complete the task."
            prompt += f"# Instruction\n{msg}\n\n"
            prompt += "# Tools\n" + await self.client.list_tools()
            prompt += "\n\nCarefully choose the correct tools and arguments from the list of tools. "
            return prompt

        chain = prompt >> self.llm(structure=many_tool_calls_schema)  # type: ignore
        res = await chain.run(msg)
        return ManyToolCalls(**json.loads(res.primary))

    async def process(self, msg: Message, chain: HandlerChain) -> str:
        async with self.client.client:
            if self.tool_call_strategy == "single":
                tool_call = await self.single_tool_call(msg)
                return await self.client.call_tool(
                    tool_call.tool_name, tool_call.arguments
                )
            else:
                tool_calls = await self.many_tool_calls(msg)
                results = []
                for tool_call in tool_calls.tool_calls:
                    result = await self.client.call_tool(
                        tool_call.tool_name, tool_call.arguments
                    )
                    results.append(result)
                return "\n\n".join(results)
