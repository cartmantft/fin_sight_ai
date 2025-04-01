# FinSight AI 개발 진행 상황 보고서

## 작업 요약

*   프런트엔드 프로젝트 (Next.js) 생성 및 기본 설정 완료
*   백엔드 프로젝트 (FastAPI) 생성 및 기본 설정 완료
*   프런트엔드와 백엔드 연결 확인 (API 호출 성공)
*   PostgreSQL 데이터베이스 연결 설정 및 CRUD 기능 구현
*   pgvector 확장 설치 시도 (계속 실패)

## 문제점 및 해결 방안

*   pgvector 확장 설치 실패: PostgreSQL 버전 문제 및 패키지 설치 문제 발생
*   해결 방안: pgvector 설치 대신 BM25 또는 TF-IDF를 사용한 의미 기반 검색 구현 고려

## 향후 작업 계획

*   BM25 또는 TF-IDF를 사용하여 의미 기반 검색 기능 구현
*   UI/UX 상세 설계
*   데이터 모델링
*   API 엔드포인트 설계
