# 개발용 PostgreSQL 설정

팀원 각자의 컴퓨터에 PostgreSQL DB를 만들고, 저장소의 마이그레이션으로 동일한 테이블 구조를 구성합니다. `localhost`는 자신의 컴퓨터이므로 **실제 게시글 데이터는 팀원 간 공유되지 않습니다.** 같은 데이터를 함께 사용하려면 별도의 공용 PostgreSQL 서버와 접속 정보가 필요합니다. 현재 문서는 개인 개발 DB 기준입니다.

## DB 사용 및 배포 계획

- **현재 기능 개발 단계:** 팀원 각자의 로컬 PostgreSQL을 사용합니다. 모델과 마이그레이션을 Git으로 공유해 테이블 구조를 동일하게 유지합니다.
- **Render 배포 단계: Render PostgreSQL에 공용 DB를 생성하고, 배포하는 Flask 앱이 해당 DB에 연결되도록 구성할 예정입니다. 현재 공용 DB가 구성된 상태는 아닙니다.**
- **전환 방법:** 배포 환경의 `DATABASE_URL`을 공용 DB 접속 정보로 설정하고, 담당자 한 명이 해당 DB에 `python -m flask --app app db upgrade`를 실행합니다. 기존 모델과 마이그레이션을 그대로 사용합니다.
- **데이터 처리:** 각자의 로컬 테스트 데이터는 공용 DB로 자동 이전되지 않습니다. 필요한 데이터는 별도로 등록하거나 이전합니다.
- **접속 정보 관리:** 실제 접속 정보는 Render 환경변수 또는 개인 `.env`로 관리하며, Git과 이 문서에는 기록하지 않습니다. 배포 이후에도 개인 기능 개발과 삭제 테스트에는 로컬 DB를 사용합니다.

## 시작 전 준비

[프로젝트 README의 Python 환경 준비](../README.md#1-python-환경-준비)를 먼저 완료하세요. 아래 명령은 프로젝트 최상위에서 가상환경을 활성화한 상태로 실행합니다. DB 설정을 마치면 [README의 앱 실행 안내](../README.md#3-앱-실행)를 따르세요.

## 1. PostgreSQL 준비

개발용 서버 버전은 PostgreSQL 17을 기준으로 합니다. `psycopg`는 Python 드라이버이며 PostgreSQL 서버 자체를 설치하지 않습니다. 
이미 실행 중인 PostgreSQL 서버가 있다면 중복 설치하지 말고 해당 서버의 버전과 포트를 확인하세요.

### macOS: Homebrew

Homebrew가 설치되어 있다면:

```bash
brew install postgresql@17
brew services start postgresql@17
export PATH="$(brew --prefix postgresql@17)/bin:$PATH"
psql postgres
```

`export PATH=...` 설정은 현재 터미널에만 적용됩니다. 계속 사용하려면 해당 줄을 `~/.zshrc`에 추가합니다. 
Homebrew 기본 설치에서는 현재 macOS 사용자로 관리용 DB에 접속합니다.

### Windows 및 기타 환경

[PostgreSQL 공식 다운로드](https://www.postgresql.org/download/)에서 OS에 맞는 PostgreSQL 17을 설치하고 서버를 실행합니다. 
Windows 설치 시 관리자 계정 `postgres`의 비밀번호와 포트(기본값 `5432`)를 기억하세요.

Windows의 SQL Shell(psql)에서 서버 `localhost`, DB `postgres`, 포트 `5432`, 사용자 `postgres`와 설치할 때 정한 비밀번호로 접속합니다. 
`psql`이 PATH에 있다면 다음 명령도 가능합니다.

```bash
psql -h localhost -U postgres -d postgres -W
```

## 2. 앱 전용 계정과 빈 DB 생성

`psql`에 접속한 상태에서 실행합니다. 이미 만든 계정과 DB가 있다면 다시 생성하지 않습니다.

```sql
CREATE ROLE moajup_user WITH LOGIN;
\password moajup_user
CREATE DATABASE moajup OWNER moajup_user;
\q
```

`\password` 실행 후 비밀번호를 두 번 입력합니다. 입력 문자가 화면에 표시되지 않는 것은 정상입니다. 여기서 정한 비밀번호는 DB 접속용 개인 비밀번호 입니다.

## 3. 환경변수 설정

기존 `.env`가 없는 경우에만 예시 파일을 복사합니다.

```bash
cp .env.example .env
```

`.env`의 `CHANGE_ME`를 앞에서 정한 DB 비밀번호로 바꿉니다.

```dotenv
DATABASE_URL=postgresql+psycopg://moajup_user:CHANGE_ME@localhost:5432/moajup
```

- 계정: `moajup_user`, DB: `moajup`, 기본 포트: `5432`
- `.env`는 Git에 올리지 않습니다. `.env.example`에는 실제 비밀번호를 적지 않습니다.
- `load_dotenv()`가 값을 로딩하고 `app.py`가 `DATABASE_URL`을 `SQLALCHEMY_DATABASE_URI` 설정에 전달합니다.

## 4. 공유된 마이그레이션 적용

저장소에는 초기 마이그레이션이 포함되어 있습니다. 팀원은 `db init`이나 `db migrate`를 다시 실행하지 않고 다음 명령만 실행합니다.

```bash
python -m flask --app app db upgrade
python -m flask --app app db current
python -m flask --app app db heads
```

`current`의 버전이 `heads`의 최신 버전과 같으면 적용된 상태입니다. 최초 버전은 `e2b2e0a4c06d`이며, 이후 변경되면 저장소의 최신 버전을 기준으로 합니다.

생성되는 테이블:

| 테이블 | 역할 |
| --- | --- |
| `report_items` | 단톡방 제보: 안내 날짜·시간, 물건 이름, 특징, 단톡방 이름, 비밀번호 해시 |
| `found_items` | 직접 습득: 습득 날짜·시간·장소, 물건 이름, 특징, 보관 위치, 비밀번호 해시 |
| `alembic_version` | 마이그레이션 적용 버전 관리 |

두 게시글 테이블은 정수 기본키 `id`를 사용하며, 정의된 항목은 모두 NULL을 허용하지 않습니다. 빈 문자열 검증과 숫자 4자리 비밀번호 검증·해싱은 각 기능에서 처리합니다. 
모델의 `password_hash`에는 해시 결과만 저장합니다.

## 5. DB 연결 및 저장·조회 검증

개발 DB를 대상으로 Flask 셸을 실행합니다.

```bash
python -m flask --app app shell
```

다음 코드를 입력하면 연결된 DB·사용자와 테이블 목록을 확인할 수 있습니다.

```python
from extensions import db
from sqlalchemy import text, inspect

print(db.session.execute(text("SELECT current_database(), current_user")).one())
print(inspect(db.engine).get_table_names())
```

예상 결과는 `('moajup', 'moajup_user')`와 위의 세 테이블입니다.

같은 셸에서 두 모델의 데이터를 저장하고, 세션을 비운 뒤 다시 조회합니다.

```python
from datetime import date, time
from werkzeug.security import generate_password_hash, check_password_hash
from models import ReportItem, FoundItem

report = ReportItem(
    notice_date=date.today(), notice_time=time(14, 30),
    item_name="[테스트] 지갑", description="검정 카드 지갑",
    chat_room_name="테스트 단톡방",
    password_hash=generate_password_hash("0012"),
)
found = FoundItem(
    found_date=date.today(), found_time=time(15, 0),
    found_location="도서관", item_name="[테스트] 우산",
    description="파란 접이식 우산", storage_location="안내실",
    password_hash=generate_password_hash("0034"),
)
db.session.add_all([report, found])
db.session.commit()
report_id, found_id = report.id, found.id
db.session.remove()

saved_report = db.session.get(ReportItem, report_id)
saved_found = db.session.get(FoundItem, found_id)
assert saved_report is not None and saved_found is not None
assert saved_report.item_name == "[테스트] 지갑"
assert saved_found.storage_location == "안내실"
assert check_password_hash(saved_report.password_hash, "0012")
assert check_password_hash(saved_found.password_hash, "0034")
print("저장·조회 및 해시 검증 성공")
```

검증 후 같은 셸에서 방금 만든 두 건만 삭제하고 종료합니다.

```python
db.session.delete(saved_report)
db.session.delete(saved_found)
db.session.commit()
exit()
```

중간에 오류가 발생하면 다음 단계를 진행하지 말고 원인을 확인합니다. 트랜잭션 오류 후 셸에서 작업을 재시도하려면 `db.session.rollback()`을 먼저 실행합니다. 
커밋된 테스트 데이터는 롤백으로 삭제되지 않으므로 생성된 ID를 기준으로 정리합니다.

## 6. DB 모델 변경 시 팀 작업 순서

모델을 변경한 담당자가 최신 마이그레이션까지 적용한 DB에서 실행합니다.

```bash
python -m flask --app app db migrate -m "Describe model changes"
```

생성 파일의 `upgrade()`와 `downgrade()`를 검토한 뒤 `db upgrade`로 적용·검증합니다. `models.py`와 `migrations/`의 코드·설정 파일을 함께 커밋합니다. 자동 생성된 `__pycache__/`, `*.pyc`는 제외합니다. 
이미 공유·적용된 마이그레이션은 임의로 삭제하거나 다시 생성하지 않습니다.

다른 팀원은 변경 사항을 받은 뒤 `python -m flask --app app db upgrade`를 실행합니다. 테이블 관리는 마이그레이션으로 통일합니다.

## 자주 발생하는 오류

| 오류 | 확인할 내용 |
| --- | --- |
| `KeyError: 'DATABASE_URL'` | 프로젝트 최상위 `.env`에 변수가 있는지 확인 |
| `No module named 'psycopg'` 등 | 가상환경 활성화 및 `python -m pip install -r requirements.txt` 실행 |
| `connection refused` | PostgreSQL 서버 실행 여부, 호스트 및 포트 확인 |
| `password authentication failed` | 계정·비밀번호와 URL 인코딩 확인 |
| `database "moajup" does not exist` | 접속 대상 서버에 개발 DB를 생성했는지 확인 |
| `relation ... does not exist` | 대상 DB 확인 후 `db upgrade` 실행 |
| `role ... already exists` / `database ... already exists` | 기존 계정·DB를 확인하고 생성 단계 생략; 삭제 후 재생성하지 않기 |

오류를 공유할 때 실제 비밀번호나 전체 접속 URL은 제외합니다.

## 참고

- [PostgreSQL 공식 다운로드](https://www.postgresql.org/download/)
- [Homebrew PostgreSQL 17](https://formulae.brew.sh/formula/postgresql%4017)
- [Psycopg 공식 안내](https://www.psycopg.org/)
