# Conflux

[![PyPI version](https://img.shields.io/pypi/v/conflux-ai.svg)](https://pypi.org/project/conflux-ai/) [![License](https://img.shields.io/github/license/AI-LENS/Conflux)](LICENSE)

A simple Python library to build prompt pipelines and applications with Large Language Models (LLMs). Conflux is designed for flexibility, composability, and ease of use, making it easy to create complex LLM workflows.

**Key Features:**

- Build modular, composable LLM pipelines with minimal code
- Integrate with OpenAI, Gemini, FAISS, and more
- Full control over prompt engineering and execution
- Intuitive, Pythonic API for rapid prototyping and production

**Use Cases:**

- Prompt chaining and orchestration
- Retrieval-augmented generation (RAG)
- Tool-calling and agent workflows
- Custom LLM-powered applications

## Core Concept

> **Note:** The following diagram uses Mermaid syntax. If your Markdown viewer does not support Mermaid, please refer to the [docs](https://ai-lens.github.io/Conflux/) for a static image.

```mermaid
graph LR
    subgraph "HandlerChain"
        A[Handler 1] -->|Message| B[Handler 2]
        B -->|Message| C[Handler 3]
    end
    Input["Input (Message)"] --> A
    C --> Output["Output (Message)"]
```

A **HandlerChain** is a sequence of handlers that process messages step by step. This enables you to build complex LLM workflows by composing simple, reusable components.

Conflux has three main components:

- **Messages**: Entities in an application communicate through `Message` objects.
- **Handlers**: `Message`s are passed through `Handler`s that can modify, transform, or format the message.
- **HandlerChains**: `Handler`s are chained together to form a `HandlerChain`, which executes handlers in order.

## Installation

**Requirements:**

- Python 3.12+
- Windows, macOS, or Linux

Install the core package:

```bash
pip install conflux-ai
```

Or, if you use FAISS for similarity search:

```bash
pip install -U conflux-ai[faiss]
```

## Example Usage

Below is a simple example that generates a company name and tagline using OpenAI's LLM. (Requires an OpenAI API key set as the `OPENAI_API_KEY` environment variable.) You can also replace `OpenAiLLM` with `GeminiLLM` to use Google's Gemini LLM using `GOOGLE_API_KEY`.

```python
import asyncio
from conflux import HandlerChain, Message, handler
from conflux.handlers import OpenAiLLM

@handler
async def company_name(msg: Message, chain: HandlerChain) -> str:
    chain.variables["product"] = msg.primary
    return (
        f"What would be an appropriate name for a business specializing in {msg.primary}?"
        "Only mention the company name and nothing else."
    )

@handler
async def company_tagline(msg: Message, chain: HandlerChain) -> str:
    return (
        f"What would be an appropriate tagline for a business specializing in {chain.variables['product']}"
        f" and with company name {msg.primary}?\nFormat your output in the following"
        f" format:\n{msg.primary}: <tagline>"
    )

def main():
    name_and_tagline_generator = (
        company_name >> OpenAiLLM() >> company_tagline >> OpenAiLLM()
    )
    res = asyncio.run(name_and_tagline_generator("bike"))
    print(res)

if __name__ == "__main__":
    main()  # Example output: Socket: The best socks in the world
```

# Advanced Examples

Explore more advanced usage patterns and integrations in the `examples/` directory:

- [MCP Tool Call Example](https://github.com/AI-LENS/Conflux/blob/main/examples/mcp_tool_call.py): How to call tools from an MCP (Model Context Protocol) server as part of your handler chain.
- [Retrieval-Augmented Generation (RAG) Example](https://github.com/AI-LENS/Conflux/blob/main/examples/rag_example.py): How to build a RAG pipeline using OpenAI embeddings and a FAISS vector index.

For more, see the [`examples`](https://github.com/AI-LENS/Conflux/tree/main/examples) folder in the repository.

## Why Conflux?

Applications with LLMs can get complex quickly. Conflux is designed for simplicity and scalability, giving you control over prompts and execution while maintaining an intuitive API. Unlike more rigid frameworks, Conflux lets you customize every step of your pipeline.
