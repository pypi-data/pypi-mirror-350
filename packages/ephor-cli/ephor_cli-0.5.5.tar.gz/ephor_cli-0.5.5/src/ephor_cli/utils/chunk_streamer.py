from typing import AsyncIterable

from langchain_core.messages import (
    AIMessageChunk,
    ToolMessageChunk,
    message_chunk_to_message,
)


class ChunkStreamer:
    """
    Simple utility class for streaming and merging message chunks.
    Handles different types of chunks (AIMessageChunk, ToolMessageChunk).

    This class takes an AsyncIterable source of chunks and merges chunks of the
    same type into complete messages.
    """

    def __init__(self):
        self.is_cancelled = False
        self.messages = []
        self.merged_chunk = None

    def cancel(self):
        """Mark the streamer as cancelled."""
        self.is_cancelled = True

    def reset(self):
        """Reset the streamer to its initial state."""
        self.is_cancelled = False
        self.messages = []
        self.merged_chunk = None

    async def process(
        self, stream: AsyncIterable[AIMessageChunk | ToolMessageChunk]
    ) -> AsyncIterable[AIMessageChunk | ToolMessageChunk]:
        try:
            async for chunk in stream:
                if not self.merged_chunk:
                    self.merged_chunk = chunk
                elif isinstance(chunk, AIMessageChunk) and isinstance(
                    self.merged_chunk, AIMessageChunk
                ):
                    self.merged_chunk += chunk
                elif isinstance(chunk, ToolMessageChunk) and isinstance(
                    self.merged_chunk, ToolMessageChunk
                ):
                    self.merged_chunk += chunk
                else:
                    self.messages.append(message_chunk_to_message(self.merged_chunk))
                    self.merged_chunk = chunk

                yield chunk

                if self.is_cancelled:
                    break
        finally:
            if self.merged_chunk:
                self.messages.append(message_chunk_to_message(self.merged_chunk))
