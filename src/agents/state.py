from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChunkingState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_documents: str
    parsed_markdown: str
    final_chunks: list
    pipeline_status: str
    error_log: str
    adjustment_factor: int