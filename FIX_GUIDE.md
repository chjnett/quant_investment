# 오류 해결 가이드 (Fix Guide)

## 1. Python 패키지 설치 오류 해결
**문제**: `npm`은 Node.js 패키지 관리자입니다. Python 라이브러리(`requirements.txt`, `psycopg2-binary` 등) 설치에는 사용할 수 없습니다.

**해결 방법**: `npm install` 대신 `pip install`을 사용해야 합니다.

터미널에 다음 명령어를 입력하세요:
```bash
pip install -r requirements.txt
```

## 2. NPM ERESOLVE 오류 해결
**문제**: `package.json`에 명시된 `eslint-config-next`의 최신 버전(v15+)이 `eslint` v9 이상을 요구하지만, 현재 `eslint` v8이 설정되어 있어 충돌이 발생했습니다.

**해결 방법**:
두 가지 방법 중 하나를 선택하세요.

### 방법 A: --legacy-peer-deps 옵션 사용 (간편)
의존성 충돌을 무시하고 설치하는 방법입니다.
```bash
npm install --legacy-peer-deps
```

### 방법 B: package.json 버전 수정 (권장)
제가 `package.json`을 수정하여 `eslint-config-next` 버전을 호환되는 버전(14.x)으로 변경해 두겠습니다. 이 파일을 저장한 후 다시 `npm install`을 실행하면 오류 없이 설치됩니다.

```bash
# package.json 수정 후
npm install
```
