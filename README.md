# PYTHON_TO_DAG (with Antigravity) — Production-Grade Spec Pack

이 저장소는 **Python 기반 파이프라인을 Airflow DAG로 일관되게 변환/생성**하기 위한 설계 문서/스펙/운영 가이드를 포함합니다.  
개발은 **Antigravity(구현)** + **ChatGPT(기획/명세/가드레일)**의 코워크 형태로 진행합니다.

## Why
- Antigravity가 컨텍스트를 충분히 반영하지 못해 **구버전 DAG/환경 설정 무시/요구사항 누락**이 반복되는 문제를 방지
- DAG 생성/수정이 사람 손을 덜 타도록 **명세 기반 자동화(재현성/멱등성/관측성)** 확보
- “돌아가기만 하는 DAG”이 아니라 **운영 가능한 DAG**(재시도/백필/알림/데이터 계약/로깅)을 목표로 함

## What (Outputs)
- `dags/` : 생성된 Airflow DAG 파일
- `pipelines/` : DAG로 바뀌기 전 “파이프라인 정의” (Python 또는 YAML)
- `docs/` : 스펙/규칙/실패 시나리오/테스트 전략/관측성/보안
- `tests/` : 변환기/생성기 테스트 (골든 파일 기반)

## Non-Negotiables (절대 준수)
- **Airflow version / Provider version / Python version**은 문서에 명시된 범위 내에서만 가정한다.
- DAG는 반드시:
  - 멱등성(idempotent)
  - 백필(backfill) 가능
  - 장애 시 재시도/알림/로그 상관관계(correlation_id) 제공
  - 스키마/데이터 계약을 만족
- “작동 예시”는 **환경 무시**하고 작성하지 않는다. (경로/권한/의존성/변수는 명시적으로)

## Folder Structure
```text
.
├── dags/                       # Generated DAGs
├── pipelines/                  # Pipeline definitions (input to generator)
│   ├── python/                 # Python-defined pipelines
│   └── yaml/                   # YAML-defined pipelines
├── src/
│   ├── python_to_dag/          # Core transformer/generator
│   ├── airflow_templates/      # Jinja templates for DAG codegen
│   └── utils/
├── docs/
├── tests/
└── tools/

How to Work (Collaboration Contract)

ChatGPT: 스펙/문서/테스트 기준/수용 기준 정의, 구현 방향 가드

Antigravity: 실제 코드/템플릿/통합, 스펙 충족 증명(테스트/예제)

구현자는 docs/10_handoff_prompt_for_antigravity.md를 최우선 소스 오브 트루스로 삼는다.