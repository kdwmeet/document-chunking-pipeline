import streamlit as st
from langchain_core.messages import AIMessage
from src.agents.graph import compiled_chunk_graph

st.set_page_config(page_title="RAG Data Pipeline Sandbox", layout="wide")
st.title("자율 멀티 포맷 문서 구조화 및 벡터 청킹 최적화 파이프라인")

col1, col2 = st.columns(2)

with col1:
    st.subheader("대용량 비정형 원천 문서 스트림 주입")

    sample_doc = st.radio(
        "테스트용 비정형 텍스트 문서 선택",
        ["사내 가상 환경 규정 가이드라인 문서", "구조가 손상된 불량 비정형 데이터"]
    )

    if sample_doc == "사내 가상 환경 규정 가이드라인 문서":
        default_text = "제1조 목적: 이 규정은 사내 시스템 가상환경 구축 도구의 표준을 정함을 목적으로 한다. 제2조 표준 도구: 파이썬 패키지 및 가상환경 관리 매니저로는 uv를 전사 표준으로 채택한다. 설치 속도와 격리 성능이 뛰어나기 때문이다."
    else:
        default_text = "알 수 없는 문서 스트림 데이터 유입 시도됨. 본문 없음. 에러코드 404."

    raw_doc_stream = st.text_area("비정형 소스 문서 데이터", value=default_text, height=150)

    if st.button("실시간 RAG 전처리 파이프라인 가동"):
        initial_input = {
            "messages": [],
            "raw_document": raw_doc_stream,
            "parsed_markdown": "",
            "final_chunks": [],
            "pipeline_status": "INIT",
            "error_log": "",
            "adjustment_factor": 0
        }

        output_state = compiled_chunk_graph.invoke(initial_input)
        st.session_state.chunk_result = output_state
        st.success("자율 계층 파싱 및 가드레일 유효성 검수 루프가 완료되었습니다.")

with col2:
    st.subheader("파이프라인 구조화 분석 및 벡터 적재 모니터")

    if "chunk_result" in st.session_state:
        res = st.session_state.chunk_result
        status = res.get("pipeline_status")

        st.markdown("**변환된 논리 계층형 마크다운 구조:**")
        st.code(res.get("parsed_markdown", ""), language="markdown")

        st.markdown("---")
        st.markdown("**최종 분할 완료된 Semantic Chunks:**")
        st.json(res.get("final_chunks", []))

        st.markdown("---")
        if status == "VERIFIED":
            st.success(f"데이터 품질 상태: {status} (벡터 데이터베이스 적재 안전 확인)")
        else:
            st.error(f"데이터 품질 상태: {status} (파편화 리스크로 인한 가드레일 차단)")
            st.warning(f"품질 경고 사유: {res.get('error_log')}")

        if res.get("messages"):
            st.markdown("---")
            st.info(f"스토리지 엔진 인프라 제어 피드백:\n{res['messages'][-1].content}")

    else:
        st.info("좌측 입력창에 텍스트 소스를 배치하고 파이프라인을 구동하면 실시간 마크다운 파싱 구조가 이곳에 렌더링됩니다.")
