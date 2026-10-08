# OSS_TEAM_1
26년 2학기 오픈소스소프트웨어 1팀 (Gitter) 레포지토리입니다.

# moajub
학과 단톡방마다 흩어져 있던 분실물 공지를 한곳에 모은 캠퍼스 통합 분실물 서비스

## 스크린샷
- 추가 예정 

## 주요 기능
| 기능 | 설명 | 담당 |
|------|------|------|
| view | 조회 | 이정주 |
| register | 등록 | 이지민 |
| search | 검색 | 김민서 (팀장) |
| delete | 삭제 | 강정우 |

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| 언어 | Python 3.13 (현재 개발 환경: 3.13.3) |
| 백엔드 | Flask, Blueprint |
| 화면 | Jinja2, HTML, CSS, JavaScript 파일 구조 |
| DB | PostgreSQL 17 기준, Psycopg 3 |
| ORM / 마이그레이션 | Flask-SQLAlchemy, Flask-Migrate / Alembic |
| 환경변수 | python-dotenv |

## 설치와 실행 (Python 3.12 이상, 3.13에서 테스트)

### 시작하기

저장소를 내려받은 후 Python 환경 준비 → DB 설정 → 앱 실행 순서로 진행합니다. 
Python 패키지는 `requirements.txt`로 설치하며, PostgreSQL 서버는 별도로 준비합니다.

### 1. Python 환경 준비

프로젝트 최상위(`app.py`가 있는 폴더)에서 실행합니다. 현재 개발 환경은 Python 3.13.3이며, 팀에서도 Python 3.13을 사용합니다.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

이미 `.venv`가 있다면 생성은 생략하고 활성화부터 진행합니다. 이후 명령은 가상환경이 활성화된 터미널 기준입니다.
PowerShell에서 활성화가 차단된다면 활성화 대신 `.\.venv\Scripts\python.exe`를 아래 명령의 `python` 자리에 사용해도 됩니다.

### 2. DB 설정

[개발용 DB 설정 문서](docs/database.md)를 따라 PostgreSQL 설치, 개인 `.env` 설정, 마이그레이션 적용 및 연결 검증을 완료하세요. 앱 실행 전에 DB 설정이 필요합니다.

### 3. 앱 실행

```bash
python app.py
```

브라우저에서 `http://127.0.0.1:5000`에 접속합니다. 현재 앱은 로컬 개발용 디버그 모드이며, DB 준비와 화면의 등록·검색·삭제 기능 구현은 별도 작업입니다.

종료하려면 터미널에서 `Ctrl + C`를 누릅니다. VS Code에서 import 경고가 보이면 Python 인터프리터로 프로젝트의 `.venv`를 선택하세요.

### 팀 개발 및 배포 계획

현재는 각자의 로컬 DB로 개발합니다. 테이블 구조는 모델과 마이그레이션으로 공유하며, 실제 데이터는 각자 별도로 저장됩니다.

- 모델 변경 시 담당자가 마이그레이션을 생성·검토하고 모델과 함께 커밋합니다.
- 팀원은 변경 사항을 받은 뒤 가상환경에서 `python -m flask --app app db upgrade`를 실행합니다.
- 의존성이 변경되면 `requirements.txt`를 갱신하고, 팀원은 `python -m pip install -r requirements.txt`로 설치합니다.
- `.env`, `.venv/`, `__pycache__/`는 커밋하지 않습니다. 실제 비밀번호는 예시 파일이나 문서에도 적지 않습니다.

- Render 배포 시 공용 PostgreSQL을 구성할 예정입니다. 전환 방법과 데이터 처리 방침은 [DB 문서](docs/database.md#db-사용-및-배포-계획)를 참고하세요.

## 사용법

- 추가 예정

## 팀원
| 이름 | 역할 | GitHub |
|------|------|--------|
| 김민서 | 팀장 | MinseoKim01 |
| 이정주 | 개발 리드 | maylily17-web |
| 이지민 | 리뷰, 품질 담당 | VrynMN |
| 강정우 | 문서 담당 | kjwoo0306 |

기여 방법은 [CONTRIBUTING.md](CONTRIBUTING.md), 
행동 수칙은 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)를 참고하세요.

## 라이선스
MIT License — see [LICENSE](LICENSE)
