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

### 방법 B: DBeaver 연결 가이드 (권장)

DBeaver를 사용하여 Docker에 실행 중인 PostgreSQL에 접속하는 상세 방법입니다.

1. **DBeaver 실행 및 새 연결 생성**
   - 상단 메뉴에서 `Database` -> `New Database Connection` 선택 (또는 플러그 아이콘 클릭).
   - `PostgreSQL` 아이콘 선택 후 `Next` 클릭.

2. **Connection Settings (연결 설정) 입력**
   `Main` 탭에서 다음 정보를 입력합니다:

   | 항목 (Field) | 입력값 (Input) | 설명 |
   | --- | --- | --- |
   | **Host** | `localhost` | 로컬 환경의 Docker 포트로 접속 |
   | **Port** | `5435` | `docker-compose.yml`의 `ports` 설정(`5435:5432`)에 따름 |
   | **Database** | `alpha_sentinel` | 기본 DB 이름 |
   | **Username** | `user` | 기본 사용자 이름 |
   | **Password** | `password` | 기본 비밀번호 |

3. **Driver Properties (드라이버 속성) 확인** (필요시)
   - 보통 기본 설정으로 작동하지만, 접속이 안 될 경우 `Driver Properties` 탭에서 SSL 모드가 `disable`인지 확인해보세요 (로컬 개발 환경).

4. **Test Connection (연결 테스트)**
   - 설정 창 하단의 `Test Connection ...` 버튼을 클릭합니다.
   - `Connected` 성공 메시지가 뜨면 `Finish`를 눌러 저장합니다.

5. **트러블슈팅 (접속 실패 시)**
   - **Connection refused**: 도커 컨테이너가 켜져 있는지 확인하세요 (`docker ps`).
   - **Authentication failed**: `.env` 파일이나 `docker-compose.yml`의 환경변수 비밀번호가 맞는지 확인하세요.
   - **Port conflict**: `docker-compose.yml`에서 호스트 포트를 `5435`로 변경했으므로, DBeaver에서도 반드시 **5435** 포트를 사용해야 합니다.

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
