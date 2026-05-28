from langgraph.graph import StateGraph, END
from src.agents.state import ChunkingState
from src.agents.nodes import document_parser_node, dynamic_chunker_node, chunk_guardrail_node, storage_loader_node

def route_by_chunk_quality(state: ChunkingState) -> str:
    status = state.get("pipeline_status")

    if status == "SHORT_CONTEXT" and state.get("adjustment_factor", 0) <= 100:
        return "rechunk"
    return "load"

def create_chunking_graph():
    workflow = StateGraph(ChunkingState)

    workflow.add_node("parser", document_parser_node)
    workflow.add_node("chunker", dynamic_chunker_node)
    workflow.add_node("guardrail", chunk_guardrail_node)
    workflow.add_node("loader", storage_loader_node)

    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "chunker")
    workflow.add_edge("chunker", "guardrail")
    workflow.add_conditional_edges(
        "guardrail",
        route_by_chunk_quality,
        {
            "load": "loader",
            "rechunk": "chunker"
        }
    )

    workflow.add_edge("loader", END)
    
    return workflow.compile()

compiled_chunk_graph = create_chunking_graph()