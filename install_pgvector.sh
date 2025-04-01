#!/bin/bash
set -e

# PostgreSQL 17 이미지 실행
docker run --name finsight-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres:17

# 잠시 대기 (PostgreSQL 시작 시간 확보)
sleep 10

# pgvector 설치 (컨테이너 내부)
docker exec -it finsight-db bash -c "apt-get update && \
    apt-get install -y gcc postgresql-server-dev-all git make && \
    git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install"

# pgvector 확장 생성 (PostgreSQL 접속 후)
docker exec -it finsight-db bash -c "psql -U postgres -d postgres -c \"CREATE EXTENSION vector;\""
