def load_chunks_to_vector_db(chunks: list) -> str:
    """가드레일을 통과한 무결한 계층형 청크 배열을 가상 벡터 DB에 커밋하는 툴"""
    return f"적재 성공: 총 [{len(chunks)}]개의 고품질 세만틱 청크가 벡터 인덱스에 저장되었습니다."

def log_malformed_document(reason: str) -> str:
    """계층 붕괴 또는 텍스트 오염으로 청킹이 불가능한 원문을 오류 스토리지로 우회시키는 툴"""
    return f"파이프라인 차단: 구조화 검패 실패로 레코드가 격리되었습니다. (이유: {reason})"