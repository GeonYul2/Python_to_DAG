# Security & Privacy Baseline

## 1) Secrets Handling
- API Keys/Token은 코드/레포에 절대 포함 금지
- Airflow Connections/Variables 또는 Secret Backend 사용
- 로그에 민감정보 출력 금지 (마스킹)

## 2) Data Privacy
- transcript/summary에 개인정보가 포함될 수 있으면:
  - 저장 전 PII redaction 단계 옵션 제공
  - 샘플/테스트 데이터는 비식별

## 3) Access Control
- 출력 스토리지 권한 최소화
- 운영 환경과 로컬 환경의 버킷/경로 분리
