import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from src.config import Config
from src.agents.state import ChunkingState
from src.services.vector_loader import load_chunks_to_vector_db, log_malformed_document

llm = ChatOpenAI(
    model=Config.MODEL_NAME,
    api_key=Config.OPENAI_API_KEY
)

def document_parser_node(state: ChunkingState) -> dict:
    """비정형 줄글 문서의 제목, 부제목, 본문 관계를 식별해 마크다운 규격으로 초고속 변환하는 노드"""
    raw_text = state.get("raw_document", "")

    system_prompt = (
        "You are an automated technical document restructuring agent.\n"
        "Analyze the raw unstructured text and convert it into a well-structured Markdown format using proper headings (#, ##, ###).\n"
        "Ensure data entities, sections, and contextual hierarchies are clearly preserved.\n"
        "Return ONLY the plain Markdown text."
    )

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": raw_text}
    ])

    return {"parsed_markdown": response.content}

def dynamic_chunker_node(state: ChunkingState) -> dict:
    """마크다운 태그를 기반으로 문맥 의미 단위가 소실되지 않도록 가변형 청크 리스트를 생성하는 노드"""
    markdown_text = state.get("parsed_markdown", "")
    adj = state.get("adjustment_factor", 0)

    system_prompt = (
        "You are a vector database pre-processing chunking coordinator.\n"
        "Slice the following Markdown text into optimal semantic chunks for RAG embedding.\n"
        "Each chunk must retain its upper heading context.\n"
        "Return ONLY a strict JSON format with key: 'chunks' (list of strings)."
    )

    user_content = f"보정 계수: {adj}\n대상 텍스트:\n{markdown_text}"
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ])

    try:
        res = json.loads(response.content)
        return {"final_chunks": res.get("chunks", [])}
    except Exception:
        return {"final_chunks": [], "pipeline_status": "STRUCT_ERROR", "error_log": "청크 JSON 파싱 오류 발생"}

def chunk_guardrail_node(state: ChunkingState) -> dict:
    """생성된 청크들의 데이터 품질(텍스트 길이 불균형, 문맥 단절 여부)을 평가하는 가드레일 노드"""
    if state.get("pipeline_status") == "STRUCT_ERROR":
        return {}
    
    chunks = state.get("final_chunks", [])

    if not chunks:
        return {"pipeline_status": "STRUCT_ERROR", "error_log": "생성된 처크 배열이 비어있습니다."}
    
    for index, chunk in enumerate(chunks):
        if len(chunk) < 20:
            return {
                "pipeline_status": "SHORT_CONTEXT",
                "error_log": f"인덱스 [{index}] 청크의 텍스트가 의미 단위를 형성하기에 너무 짧아 정보 유실 우려가 있습니다.",
                "adjustment_factor": state.get("adjustment_factor", 0) + 50
            }
        
    return {"pipeline_status": "VERIFIED"}
    
def storage_loader_node(state: ChunkingState) -> dict:
    """품질 가드레일 상태에 따라 최종 벡터 인덱스에 적재하거나 에러 스토리지를 호출하는 노드"""
    status = state.get("pipeline_status")
    chunks = state.get("final_chunks", [])
    err_log = state.get("error_log", "알 수 없는 전처리 오류")

    if status == "VERIFIED":
        success_msg = load_chunks_to_vector_db(chunks)
        return {"messages": [AIMessage(content=success_msg)]}
    else:
        failure_msg = log_malformed_document(err_log)
        return {"messages": [AIMessage(content=failure_msg)]}