# PostgreSQL Docker Setup & Usage Guide

이 가이드는 `docker-compose.yml`을 사용하여 PostgreSQL 데이터베이스를 실행, 관리 및 접속하는 방법을 설명합니다.

## 1. 데이터베이스 실행 (Start Database)

프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 PostgreSQL 컨테이너만 백그라운드 모드로 시작합니다.

```bash
docker-compose up -d db
```

> **참고:** 최신 버전의 Docker Compose를 사용하는 경우 `docker-compose` 대신 `docker compose` 명령어를 사용할 수 있습니다.

## 2. 실행 상태 및 로그 확인 (Check Status)

데이터베이스가 정상적으로 실행되었는지 확인하려면 로그를 조회합니다.

```bash
docker-compose logs -f db
```

출력 로그에서 `database system is ready to accept connections` 메시지가 보이면 DB가 정상적으로 준비된 것입니다. (로그 확인을 종료하려면 `Ctrl + C`를 누르세요).

## 3. 데이터베이스 접속 (Connect to Database)

### 방법 A: 터미널에서 직접 접속 (via CLI)
실행 중인 도커 컨테이너 내부로 진입하여 `psql` 도구를 사용해 접속합니다.

```bash
docker exec -it alpha-sentinel-db psql -U user -d alpha_sentinel
```

- **명령어 설명**:
  - `alpha-sentinel-db`: 컨테이너 이름 (docker-compose.yml에 정의됨)
  - `-U user`: 사용자 이름 (기본값: user)
  - `-d alpha_sentinel`: 데이터베이스 이름 (기본값: alpha_sentinel)

### 방법 B: 외부 DB 클라이언트 사용 (DBeaver, TablePlus 등)
로컬 PC에 설치된 데이터베이스 관리 도구를 사용하여 접속할 때 아래 정보를 사용하세요.

| 설정 항목 | 값 (Value) | 비고 |
| --- | --- | --- |
| **Host** | `localhost` | |
| **Port** | `5432` | `docker-compose.yml`의 ports 설정 참고 |
| **Database** | `alpha_sentinel` | 환경변수 `POSTGRES_DB` 값 |
| **User** | `user` | 환경변수 `POSTGRES_USER` 값 |
| **Password** | `password` | 환경변수 `POSTGRES_PASSWORD` 값 |

## 4. 환경 변수 설정 (Configuration)

기본 접속 정보는 `docker-compose.yml` 파일 내에 정의되어 있습니다. 보안을 위해 운영 환경에서는 `.env` 파일을 생성하여 값을 덮어쓰는 것이 좋습니다.

**.env 파일 예시:**
```ini
POSTGRES_USER=my_secure_user
POSTGRES_PASSWORD=my_secure_password
POSTGRES_DB=my_production_db
```

## 5. 데이터 저장소 (Volumes)
데이터는 도커 볼륨 `postgres_data`에 영구 저장됩니다. 컨테이너를 삭제하더라도 데이터는 유지됩니다.
데이터를 완전히 초기화하려면 다음 명령어로 볼륨을 삭제하세요 (주의: 데이터가 영구 삭제됩니다).

```bash
docker-compose down -v
```
