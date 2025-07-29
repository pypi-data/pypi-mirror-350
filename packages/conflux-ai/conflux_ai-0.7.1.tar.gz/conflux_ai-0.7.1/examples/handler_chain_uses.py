import asyncio

from conflux import HandlerChain, Message, handler


@handler
async def upper_case(msg: Message, chain: HandlerChain) -> Message:
    return msg.upper()


@handler
async def remove_punctuation(msg: Message, chain: HandlerChain) -> str:
    return "".join([char for char in str(msg) if char.isalnum()])


@handler
async def reverse(msg: Message, chain: HandlerChain) -> Message:
    return msg[::-1]


def main():
    chain = upper_case >> remove_punctuation >> reverse
    msg = Message("You are awesome!")
    last_msg, history = asyncio.run(chain.run(msg, return_history=True))

    first_msg = history[0]  # = Message("You are awesome!")

    # `chain` is an immutable sequence of handlers
    # find a message with a specific role
    msg_rm_punc = [
        handler for handler in chain if handler.role == "remove_punctuation"
    ][0]

    # get last handler
    last_handler = chain[-1]
    assert last_handler.role == "reverse"

    print(first_msg, last_msg, msg_rm_punc, sep="\n")
