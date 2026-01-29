# docs/AGENTS.md
# 협업 에이전트 운영 규칙 (AntiGravity / ChatGPT 공통)

## 0) 이 문서의 목적
이 레포는 “대화”가 아니라 **파일(SSOT) 중심**으로 협업한다.
- SSOT 1: `contracts/environment.yaml` (환경/타겟 버전/제약)
- SSOT 2: `contracts/testing.yaml` (Pre/Post Gate 테스트 규칙)
- SSOT 3: `docs/design/*` (입력 스펙/변환 규칙)

에이전트는 SSOT를 무시하고 추측(“최신”, “아마도”)하면 실패로 간주한다.

---

## 1) 역할 분담
### ChatGPT (문서/설계 담당)
- 계약(contracts) 정의/수정
- 변환 규칙(TRANSFORMATION_RULES) 설계
- 테스트 게이트(Pre/Post) 설계
- 실패 시나리오/운영 프로세스 정리

### AntiGravity (코드 생성/리팩터링 담당)
- SSOT를 **읽고**, 그 범위 내에서 코드/테스트/CI를 수정
- “돌아갈 것 같은 코드”가 아니라 “게이트를 통과하는 코드”를 낸다
- 변경은 항상 PR 단위(또는 patch 단위)로 제출한다

---

## 2) AntiGravity 필수 행동 규칙 (절대 금지 포함)
### (필수) 작업 시작 체크리스트
1) `contracts/environment.yaml` 먼저 읽기  
2) `contracts/testing.yaml` 먼저 읽기  
3) 타겟 Airflow/Python 버전에 맞는 import/operator 제한 확인: `docs/AIRFLOW_COMPATIBILITY.md`  
4) 기존 `tests/`를 먼저 실행해 baseline 확인 (가능하면)

### (절대 금지)
- 타겟 Airflow 버전/Provider 버전/Constraints를 **추측으로 변경**
- “최신 버전 설치”를 전제로 requirements/constraints를 바꿈
- DAG 코드를 생성하면서 **Airflow import 테스트(DagBag) 없이** 제출
- 테스트 실패를 “환경 문제”라고만 말하고 **재현 로그/원인 태그** 없이 종료

---

## 3) 변경 제출 형식 (AntiGravity 출력 포맷)
모든 변경은 아래 4가지를 포함해야 한다.

### A. 변경 파일 목록
- 수정/추가/삭제 파일을 경로 기준으로 나열

### B. 핵심 의사결정 3줄 요약
- 왜 바꿨는지 / 무엇이 달라졌는지 / 어떤 위험이 줄었는지

### C. 테스트 결과 (게이트 기준)
- Pre Gate: `pytest -q tests/pre`
- Post Gate: `pytest -q tests/post`
- 실패 시: 실패한 테스트명 + 핵심 로그 20줄 이내 + 원인 태그(P0~P3)

### D. 계약 영향 여부
- `contracts/*` 변경이면: “Breaking / Non-breaking” 명시 + 이유
- 계약 변경이 아닌데 계약과 충돌하면: “계약 변경 필요”로 이슈 분리

---

## 4) 실패 원인 태깅 (P0~P3)
- P0: 계약 위반(버전/의존성/타겟 무시) 또는 보안/데이터 파괴 위험
- P1: DAG import 실패(DagBag), 파싱 실패, 치명적 런타임 오류
- P2: 규칙 위반(네이밍/로깅/경로), 경고 수준 호환성 문제
- P3: 스타일/문서/사소한 개선

실패 시에는 `docs/failure_scenarios.md`에 케이스를 누적한다(1줄이라도).

---

## 5) “PYTHON_TO_DAG” 변환 작업의 필수 게이트
- Pre: 입력 Python 로직의 의미/계약 위반을 먼저 잡는다 (`tests/pre`)
- Post: 변환된 DAG가 최소한 import/파싱 가능해야 한다 (`tests/post`)
- Post 확장: 추후 `airflow tasks test`류의 실행 게이트는 옵션으로 확장

---

## 6) 커뮤니케이션 원칙 (짧고 재현 가능하게)
- “안됨” 금지 → “어떤 테스트가, 어떤 로그로, 어떤 계약과 충돌했는지”로 말한다
- 대화로 해결하지 말고 **파일로 남긴다**: ADR / failure_scenarios / PR 템플릿
