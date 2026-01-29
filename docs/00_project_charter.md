# Project Charter — PYTHON_TO_DAG

## 1. Problem Statement
현재 자동 생성된 DAG이 다음 문제를 반복적으로 유발:
- 구버전 Airflow 문법/패턴 사용
- 환경/요구사항(버전, 경로, 변수, 권한, 의존성)을 “암묵적으로” 가정
- 운영 품질(멱등성, 백필, 재시도/알림, 데이터 계약, 로깅)이 누락

## 2. Goal
Python/YAML 파이프라인 정의로부터 **운영 가능한 Airflow DAG**을 자동 생성/갱신하는 변환기/생성기 구축.

## 3. In Scope
- 파이프라인 정의(입력) → DAG 코드(출력) 변환
- 태스크 의존성/스케줄/리트라이/알림/태그/리소스 설정 반영
- 데이터 계약(스키마/파티션/파일 규칙) 검증 훅
- 테스트(골든 파일), 린트/포맷, CI에 적합한 구조

## 4. Out of Scope (초기)
- 완전 자동 인프라 프로비저닝(Terraform, Helm 등)
- 모든 오케스트레이터 호환(Argo, Dagster 등) — Airflow 중심
- 모든 외부 시스템 커넥터 구현 (우선 템플릿/인터페이스 제공)

## 5. Success Metrics
- 동일 입력 정의에 대해 DAG 코드가 **결정적(deterministic)** 으로 생성됨
- 신규 파이프라인 추가 시:
  - 정의 파일 작성 + 테스트 추가만으로 DAG 생성 가능
- 장애 대응:
  - 재시도/알림/로그 추적이 즉시 가능
  - 백필 시나리오 문서대로 수행 가능

## 6. Definition of Done
- `docs/01_functional_spec.md`의 Must 항목 전부 충족
- `docs/08_testing_strategy.md`의 테스트 체계 최소 1세트(단위+골든) 통과
- `docs/04_airflow_dag_guidelines.md`의 금지 패턴 미사용
- 샘플 파이프라인 2개 이상을 end-to-end로 생성 및 검증