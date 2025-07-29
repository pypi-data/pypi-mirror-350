import asyncio

from conflux import HandlerChain, Message, handler
from conflux.handlers import McpToolCall, OpenAiLLM

config = {
    "mcpServers": {
        "explorer": {
            "url": "http://localhost:9090/yahoo-finance/sse",
            "transportType": "sse",
        }
    }
}


@handler
async def fetch_tool_list(msg: Message, chain: HandlerChain) -> str:
    chain.variables["query"] = msg.primary
    return f"User query: {msg.primary}?"


@handler
async def answer(msg: Message, chain: HandlerChain) -> str:
    return f"Please answer the following query:\n{chain.variables['query']}\n\nHere is the result from the relevant tool for the query:\n{msg}\n\nProvide a comprehensive answer to the query using the tool result."


def main():
    chain = (
        fetch_tool_list
        >> McpToolCall(config=config, llm=OpenAiLLM)
        >> answer
        >> OpenAiLLM()
    )
    return asyncio.run(
        chain.run(
            "What is the stock price of nifty 50 (^NSEI) today (23-05-2025)?",
        )
    )


if __name__ == "__main__":
    result = main()
    print(result)
