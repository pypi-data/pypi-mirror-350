from typing import Iterable, Protocol, Sequence, Union

from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_chunk import ChoiceDelta
from openai.types.shared_params.function_definition import FunctionDefinition

StreamOutputType = Union[str, ChatCompletionMessageToolCall]


class StreamProcessor(Protocol):
    def process(self, chunk: str) -> list[StreamOutputType]: ...
    def finalize(self) -> Sequence[StreamOutputType]: ...


class Transformation(Protocol):
    def create_stream_processor(self) -> StreamProcessor: ...

    def trans_param_messages(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        tools: Iterable[FunctionDefinition],
    ) -> Iterable[ChatCompletionMessageParam]: ...

    def trans_completion_message(
        self,
        message: ChatCompletionMessage,
    ) -> ChatCompletionMessage: ...

    def trans_completion_message_stream(
        self,
        processor: StreamProcessor,
        delta: ChoiceDelta,
        finalize: bool = False,
    ) -> ChoiceDelta: ...
