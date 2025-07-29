class ConfluxError(Exception):
    pass


class HandlerChainError(ConfluxError):
    pass


class HandlerError(ConfluxError):
    pass


class UnsupportedHandlerChain(HandlerChainError):
    def __init__(self, obj1, obj2) -> None:
        print(obj1)
        super().__init__(
            f"Unsupported HandlerChain between {str(obj1)} and {str(obj2)}."
            " HandlerChain is supported between `Handler`s and `HandlerChain`s"
        )


class ChatInterruptionError(Exception):
    pass


class HandlerChainOutputValidationError(Exception):
    pass
