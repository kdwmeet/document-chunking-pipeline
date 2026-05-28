# Autonomous Multi-Format Document Structuring & Vector Chunking Optimization Pipeline

LangGraph와 최신 초고속/비용 효율화 모델인 gpt-5.4-nano를 기반으로 구축된 실시간 자율 멀티 포맷 문서 구조화 및 벡터 청킹(Chunking) 최적화 파이프라인 가이드 시스템입니다. 보고서, 매뉴얼, 규정집 등 다양한 형태의 비정형 텍스트 소스를 분석하여 논리적 계층 구조(H1, H2, 본문 등)를 파악하고 마크다운 파싱을 고속 수행합니다. 이후 데이터 품질 가드레일을 거쳐 문맥 유실이 없는 무결한 세만틱 청크만 가상 벡터 데이터베이스에 최종 적재하는 지능형 RAG 데이터 전처리 아키텍처를 구현했습니다.

---

## Key Features & Architecture

- 구조적 마크다운 파싱: 줄글 형태의 비정형 문서가 유입되면 gpt-5.4-nano 모델이 제목, 부제목, 본문, 항목 간의 상관관계를 추론하여 표준 마크다운 규격으로 초고속 변환합니다.
- 문맥 보존형 동적 청킹: 고정 길이 슬라이싱 방식에서 벗어나, 변환된 마크다운 태그를 기반으로 상위 계층 문맥(Context)이 끊기지 않는 가변형 세만틱 청크 배열을 생성합니다.
- 데이터 품질 가드레일(Chunk Quality Guardrail): 생성된 청크들의 텍스트 길이 불균형이나 정보 파편화 리스크를 실시간 스크리닝합니다. 데이터 완성도 기준에 미달하는 불량 청크가 감지되면 시스템 적재를 자동으로 차단합니다.
- 자율 보정 피드백 루프: 파편화 위험(SHORT_CONTEXT) 탐지 시, 에이전트가 자율적으로 청킹 분할 임계치 보정 계수(Adjustment Factor)를 적용하여 그래프 역방향으로 상태를 회귀시키고 재분할을 실시합니다.

---

## Tech Stack

- Framework: LangGraph (v0.2+), LangChain (v0.3+)
- LLM Core: OpenAI gpt-5.4-nano (초저지연, 고효율 추론 모델)
- Environment & Dependency Manager: uv (Fast Python package installer)
- Frontend Dashboard: Streamlit (v1.35+)

---

## Project Directory Structure

엔터프라이즈 사내 지식 관리 시스템(KMS) 및 RAG 데이터 인프라 표준 규격을 준수하여 문서 추출 레이어, 가드레일 검증 노드, 가상 벡터 스토리지 인터페이스를 엄격히 분리했습니다.
```
document-chunking-pipeline/
├── src/
│   ├── main.py                 # Streamlit RAG 데이터 파이프라인 관제 대시보드
│   ├── config.py               # API 키 및 청킹 크기 임계치 설정 관리
│   ├── agents/                 # LangGraph 기반 지능형 파싱 워크플로우
│   │   ├── state.py            # 원문, 파싱 마크다운, 계층 청크 배열 상태 정의
│   │   ├── graph.py            # 청크 무결성 검증 실패 시 재분할 루프 그래프 빌드
│   │   └── nodes.py            # 구조적 파싱, 계층별 동적 청킹, 가드레일 검증 노드
│   └── services/               # 벡터 스토리지 인프라 인터페이스 레이어
│       └── vector_loader.py    # 가상 벡터 DB 적재 및 불량 청크 격리 툴
├── requirements.txt            # 명시적 패키지 의존성 목록
└── .env                        # 환경 변수 보안 설정 파일
```
---

## Quick Start

### 1. Prerequisites & Installation

본 프로젝트는 초고속 파이썬 패키지 매니저인 uv를 사용해 가상환경을 구축합니다.

# 저장소 클론 및 이동
```
git clone https://github.com/your-username/document-chunking-pipeline.git
cd document-chunking-pipeline
```
# uv를 이용한 가상환경 생성 및 활성화
```
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
# 의존성 패키지 일괄 설치
```
uv pip install -r requirements.txt
```
### 2. Environment Variables Setup

프로젝트 최상위 루트 디렉토리에 .env 파일을 생성하고 발급받은 OpenAI API 키를 입력합니다.
```
OPENAI_API_KEY=your_openai_api_key_here
```
### 3. Running the Application

파이썬의 모듈 탐색 경로(sys.path) 충돌을 방지하기 위해 PYTHONPATH 환경변수를 주입하여 모듈 모드로 실행합니다.
```
Windows (PowerShell):
$env:PYTHONPATH="."
streamlit run src/main.py
```
```
Windows (CMD):
set PYTHONPATH=.
streamlit run src/main.py
```
```
Mac / Linux:
PYTHONPATH=. streamlit run src/main.py
```
---

## Production-Ready Architecture Point (포트폴리오 핵심 어필 포인트)

1. 상용 레벨 RAG 성능의 핵심인 데이터 무결성 확보
   - 단순히 고정 문자 수 기준 분할(CharacterTextSplitter)을 수행하는 완구용 파이프라인이 아닌, AI가 문서 구조를 논리적으로 해체하고 품질 거버넌스 가드레일을 거쳐 인덱싱하는 프로덕션 수준의 RAG 데이터 전처리 지식을 입증합니다.
2. 대규모 구조화 연산 인프라 비용 극적 보존
   - 사내 수많은 문서 아카이브와 규정집을 전수 청킹 가공할 때 대형 플래그십 모델을 상시 배치하면 천문학적인 API 단가가 청구됩니다. 초고속 경량화 모델인 gpt-5.4-nano를 전처리 파서 및 가드레일 판별 레이어에 조합함으로써 파이프라인의 처리 속도(Throughput)를 극대화하고 운영 단가를 획기적으로 낮췄습니다.

## 실행 화면