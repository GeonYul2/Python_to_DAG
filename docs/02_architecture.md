# Architecture Overview

## 1) High-Level Components
- Pipeline Definition (Python/YAML)
- Parser → IR(Intermediate Representation)
- Validator (schema, naming, forbidden patterns)
- Code Generator (Airflow DAG template renderer)
- Runtime Utils (logging, callbacks, contracts, io helpers)

## 2) Intermediate Representation (IR)
IR은 “Airflow 독립적”인 추상 모델로 유지한다.
- pipeline_id
- schedule
- defaults (retries, timeout, owner, tags)
- tasks: [{task_id, type, callable/ref, params, env, upstream, contract, resources}]

Airflow 특화 설정은 generator 단계에서만 매핑한다.

## 3) Data Flow (Example)
1. Extract transcript (YouTube/URL)
2. Clean & chunk
3. Summarize (LLM)
4. Post-process (key takeaways, action items, code snippets)
5. Deliver (Markdown, Notion, Email 등)

## 4) Sequence Diagram (Mermaid)
```mermaid
sequenceDiagram
  participant U as User (Pipeline Def)
  participant P as Parser
  participant V as Validator
  participant G as Generator
  participant A as Airflow

  U->>P: python/yaml definition
  P->>P: build IR
  P->>V: IR
  V->>V: validate naming/contracts/compat
  V->>G: validated IR
  G->>G: render DAG template
  G->>A: produce dags/*.py


5) Non-Functional Architecture Rules

모든 환경 의존 값은 “명시적 config”로만 주입 (ENV, Airflow Variables/Connections)

변환기 자체는 side-effect 없이 동작 (파일 생성만)

운영 로직(알림/로그/계약)은 공통 유틸로 중앙화