# API Key 발급 및 설정 가이드

시스템 작동을 위해 다음 3가지 API Key가 필요합니다.

## 1. FRED API Key (미국 연준 경제 데이터)
미국의 금리, 물가, 고용 등 거시 경제 데이터를 가져오기 위해 필요합니다.

1. **사이트 접속**: [FRED API Key Request](https://fred.stlouisfed.org/docs/api/api_key.html)
2. **회원가입/로그인**: 계정이 없다면 무료로 가입합니다.
3. **키 발급**: 간단한 사용 목적(예: "Personal Investment Research")을 입력하고 API Key를 발급받습니다.
4. **설정**: 32자리의 영문+숫자 조합 키를 `.env` 파일의 `FRED_API_KEY`에 입력하세요.

## 2. Open DART API Key (한국 금융감독원 공시)
한국 기업의 공시 보고서(사업보고서 등) 목록을 조회하기 위해 필요합니다.

1. **사이트 접속**: [Open DART 인증키 신청](https://opendart.fss.or.kr/uss/umt/EgovMberInsertView.do)
2. **신청**: 이메일 주소 인증을 통해 즉시 발급 가능합니다.
3. **설정**: 발급된 API Key를 `.env` 파일의 `DART_API_KEY`에 입력하세요.

## 3. API_SECRET_KEY (내부 보안 키)
우리 Frontend(Next.js)와 Backend(Python)가 서로 통신할 때, 외부의 해킹 시도를 막기 위한 비밀번호입니다. 정해진 형식은 없으며 복잡한 문자열이면 됩니다.

**생성 방법 (터미널)**:
아래 명령어를 터미널에 입력하여 무작위 보안 키를 생성할 수 있습니다.
```bash
openssl rand -hex 32
```
나온 결과(예: `a1b2...`)를 복사하여 `.env` 파일의 `API_SECRET_KEY`에 입력하세요.

---

## 📝 .env 파일 수정 예시

`c:\workspace2\퀀트_투자\alpha-sentinel-os\.env` 파일을 열고 아래와 같이 채워주세요.

```env
DATABASE_URL=postgresql://user:pass@... (이미 설정됨)
OPENAI_API_KEY=sk-... (이미 있다면 유지)

# 새로 추가할 부분
FRED_API_KEY=abcdef123456...
DART_API_KEY=12345678...
API_SECRET_KEY=generated_secret_key_here
```
