# OSS_TEAM_1 - 모아줍 (MoaJoop)

> **26년 2학기 오픈소스소프트웨어 팀 1 레포지토리입니다.**  
> 분실물 및 습득물을 손쉽게 등록, 조회, 검색, 삭제할 수 있는 웹 서비스입니다.

---

## 🛠 외부 프로그램 및 기술 스택
- **Backend**: Python 3.x, Flask
- **Database**: Supabase (PostgreSQL)
- **보안/인증**: bcrypt (4자리 비밀번호 단방향 해싱 및 검증)
- **Deployment**: Vercel
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS / Jinja2 Template)

---

## 🚀 로컬 개발 환경 실행 방법 (Getting Started)

### 1. 사전 요구사항
- **Python 3.10 이상**

### 2. 패키지 설치
프로젝트 루트 디렉토리에서 필요한 라이브러리를 설치합니다.

```bash
# Windows (py 런처 사용 시)
py -m pip install -r requirements.txt

# 또는 기본 pip 사용 시
pip install -r requirements.txt
```

> *(선택 사항)* 가상환경을 구성하여 실행하려면:
> ```bash
> py -m venv venv
> .\venv\Scripts\activate
> pip install -r requirements.txt
> ```

### 3. 웹 애플리케이션 실행
Flask 개발 서버를 구동합니다.

```bash
# Windows
py app.py

# 또는
python app.py
```

### 4. 웹페이지 접속 및 확인
서버 구동 후 웹 브라우저에서 아래 주소로 접속합니다.

- **접속 주소**: [http://127.0.0.1:5000](http://127.0.0.1:5000) (또는 [http://localhost:5000](http://localhost:5000))

> **💡 안내**: 서버를 종료하려면 터미널 창에서 `Ctrl + C`를 누르시면 됩니다.

---

## 📂 프로젝트 파일 및 디렉토리 구조

프로젝트는 기능별 협업(`feature/*` 브랜치) 시 코드 충돌을 최소화할 수 있도록 라우트, 템플릿, 정적 파일이 기능 단위로 모듈화되어 있습니다.

```text
모아줍(OSS)/
├── app.py                     # Flask 애플리케이션 생성 및 블루프린트 등록
├── storage.py                 # Supabase 데이터베이스 연동 및 CRUD(저장/조회/삭제) 모듈
├── auth.py                    # bcrypt 기반 비밀번호 4자리 단방향 해싱 및 인증 모듈
├── requirements.txt           # 파이썬 의존성 패키지 목록
├── .env.example               # 환경변수(Supabase URL, API KEY 등) 템플릿
├── vercel.json                # Vercel 배포 설정
│
├── api/                       # Vercel 배포용 서버리스 진입점
│   └── index.py               # Vercel WSGI 핸들러 연동
│
├── routes/                    # 기능별 Flask Blueprint 라우트 분리
│   ├── __init__.py            # Blueprint 패키지 초기화 (routes 폴더를 하나의 파이썬 패키지로 인식하게 해주는 초기화 파일)
│   ├── main.py                # 메인 대시보드 및 통계 카드 데이터 제공 라우트 (메인 페이지 접속 시 필요한 데이터 연동)
│   ├── view.py                # feature/view: 분실물 목록 및 상세 조회 라우트 (분실물 목록 및 상세보기 페이지 로직)
│   ├── register.py            # feature/register: 제보형/직접 습득형 분실물 등록 라우트 (분실물/습득물 등록 처리 로직)
│   ├── search.py              # feature/search: 키워드 및 다중 조건 필터링 검색 라우트 (건별 키워드 검색 로직)
│   └── delete.py              # feature/delete: 비밀번호 검증 및 게시글 삭제 라우트 (게시글 삭제 처리 및 비밀번호 확인 로직)
│
├── templates/                 # Jinja2 HTML 템플릿
│   ├── base.html              # 공통 레이아웃 (헤더바, 네비게이션, 푸터)
│   ├── index.html             # 메인 페이지 (히어로 섹션, 요약 통계 카드)
│   ├── list.html              # feature/view: 전체 분실물 카드 목록 UI
│   ├── detail.html            # feature/view & delete: 게시글 상세 보기 및 삭제 인터페이스
│   ├── register.html          # feature/register: 제보형 / 직접 습득형 등록 폼
│   └── search.html            # feature/search: 다중 조건 검색 및 필터링 결과 UI
│
└── static/                    # 정적 리소스 파일
    ├── css/
    │   ├── style.css          # 기본 레이아웃, 공통 UI (헤더, 푸터, 히어로 섹션) 스타일
    │   ├── card.css           # 분실물 카드 및 요약 통계 카드 스타일
    │   └── form.css           # 등록 폼, 검색 입력창, 삭제 모달 스타일
    ├── js/
    │   ├── main.js            # 메인 대시보드 인터랙션 및 실시간 통계 반영 스크립트
    │   ├── register.js        # 등록 폼 전환(제보형/습득형) 및 4자리 비밀번호 유효성 검사
    │   ├── search.js          # 검색어 공백 제거 전처리 및 다중 필터링 로직
    │   └── delete.js          # 삭제 모달 제어, 비밀번호 검증 요청 및 예외 처리
    └── images/
        └── .gitkeep           # 이미지 폴더 추적용 파일
```

### 📄 파일별 세부 역할 설명

| 파일/디렉토리 경로 | 역할 및 상세 설명 |
| :--- | :--- |
| **`app.py`** | Flask 애플리케이션 진입점. 각 기능별 라우트(Blueprint)를 등록하고 앱 설정을 초기화합니다. |
| **`storage.py`** | Supabase 클라이언트를 초기화하고 게시글 등록(Insert), 조회(Select), 완전 삭제(Delete)를 수행하는 저장소 모듈입니다. |
| **`auth.py`** | `bcrypt`를 이용해 게시글 등록 시 입력된 4자리 비밀번호를 안전하게 단방향 해싱하고, 삭제 시 입력값과 저장된 해시값을 검증합니다. |
| **`requirements.txt`** | 프로젝트 실행에 필요한 라이브러리 목록 (`flask`, `supabase`, `bcrypt`, `python-dotenv` 등)을 명시합니다. |
| **`.env.example`** | Supabase URL, Supabase Anon Key 등 민감한 환경변수 설정 예시를 담고 있습니다. |
| **`vercel.json` / `api/index.py`** | Vercel 플랫폼에 Flask 서버리스 앱으로 빌드 및 배포하기 위한 설정 파일과 진입점입니다. |
| **`routes/`** | 기능별로 분리된 컨트롤러 디렉토리로, 팀원들이 브랜치별로 독립적인 라우팅 로직을 작성할 수 있습니다. |
| **`templates/`** | 서버에서 렌더링할 HTML 파일들로, 공통 레이아웃(`base.html`)을 기반으로 상속받아 화면을 구성합니다. |
| **`static/css/`** | 화면 영역별(공통 레이아웃, 카드 형태 컴포넌트, 폼 및 모달)로 스타일시트를 분리 관리합니다. |
| **`static/js/`** | 프론트엔드 비동기 요청, 폼 입력값 유효성 검증(4자리 숫자 검사), 텍스트 전처리 등을 담당합니다. |

---

## 🌿 기능 브랜치 및 파일 매핑 가이드

각 기능 개발 시 아래 담당 파일들을 중점적으로 작업하면 다른 팀원과의 충돌을 방지할 수 있습니다.

| 기능 (Branch) | 백엔드 라우트 / 모듈 | 화면 템플릿 | 스타일 & 스크립트 |
| :--- | :--- | :--- | :--- |
| **공통 (main)** | `app.py`, `routes/main.py` | `base.html`, `index.html` | `style.css`, `card.css`, `main.js` |
| **1. 조회 (`feature/view`)** | `routes/view.py`, `storage.py` | `list.html`, `detail.html` | `card.css` |
| **2. 등록 (`feature/register`)** | `routes/register.py`, `storage.py`, `auth.py` | `register.html` | `form.css`, `register.js` |
| **3. 검색 (`feature/search`)** | `routes/search.py` | `search.html` | `form.css`, `search.js` |
| **4. 삭제 (`feature/delete`)** | `routes/delete.py`, `storage.py`, `auth.py` | `detail.html` (삭제 모달) | `form.css`, `delete.js` |

---

## 📋 주요 기능 설계 및 이슈 명세

### 1. 공통 기능: 메인페이지 구현
- 서비스 메인 화면 레이아웃 및 전체적인 대시보드 구성
- **[Issue 1-1]** 메인페이지 기본 레이아웃 구현 — 헤더바, 하단바, 히어로 섹션(메인 화면 상단에 가장 크게 눈에 띄는 핵심 메시지 및 주요 버튼 영역) UI 구성 및 기본 페이지 구조 세팅
- **[Issue 1-2]** 상단 요약 통계 카드 UI 구현 — 전체 등록, 단톡방 제보, 직접 습득 건수 집계 및 실시간 반영
- **[Issue 1-3]** 공통 라우팅 및 페이지 이동 연동 — 메인 페이지, 분실물 등록, 분실물 검색 간의 페이지 이동(라우팅) 처리

### 2. 조회 기능 (`feature/view`): 분실물 목록 및 상세 조회
- 전체 등록된 분실물 게시글 목록을 카드 형태로 시각화하고, 특정 분실물 클릭 시 세부 정보를 확인
- **[Issue 2-1]** 전체 분실물 카드 목록 UI 구현 — 저장된 분실물 목록 데이터를 조회, 연동하여 카드 형태의 목록으로 출력
- **[Issue 2-2]** 분실물 게시글 상세 보기 기능 — 목록에서 선택한 게시글의 세부 정보 상세 출력
- **[Issue 2-3]** 빈 목록 및 데이터 로딩 예외 처리 — 등록된 게시글이 없을 때 예외 안내 화면 출력

### 3. 등록 기능 (`feature/register`): 2가지 형태의 분실물/습득물 등록
- **제보형 (학과 단톡방 공지 내용 등록)**: 안내 날짜, 시간, 물건 이름, 특징, 단톡방 이름, 비밀번호 4자리
- **습득형 (오프라인 직접 습득 등록)**: 습득 날짜, 시간, 습득 장소, 물건 이름, 특징, 둔 장소(보관 위치), 비밀번호 4자리
- **[Issue 3-1]** 등록 폼 입력 UI 구성 — 제보형/직접 습득형 정보 입력 화면 구현 (라디오 버튼/탭 전환)
- **[Issue 3-2]** 비밀번호 입력값 숫자 4자리 유효성 검사 — 숫자가 아니거나 4자리가 아닐 때 에러 메시지 출력 예외 처리
- **[Issue 3-3]** 비밀번호 단방향 해싱 (`bcrypt` 사용) 모듈 개발 — 보안을 위해 입력받은 4자리 비밀번호를 암호화 해싱 (`auth.py`)
- **[Issue 3-4]** 등록 데이터 저장소 (`storage.py`) 연동 — 입력받은 게시글 정보 및 해싱된 비밀번호를 저장소에 정상 저장 후 목록 페이지로 이동

### 4. 검색 기능 (`feature/search`): 다양한 조건 기반 검색
- 날짜, 물건명, 특징, 단톡방 이름, 장소 등의 키워드로 원하는 분실물 필터링 조회
- **[Issue 4-1]** 검색 인터페이스 구성
- **[Issue 4-2]** 텍스트 전처리 및 키워드 매칭 로직 개발 — 공백 제거 및 부분 일치(Contains) 기반 필터링 파이프라인 구축
- **[Issue 4-3]** 다중 조건 (장소, 물건명 등) 필터링 검색 연산 구현 — 수집된 조건들을 조합하여 일치하는 데이터셋 추출

### 5. 삭제 기능 (`feature/delete`): 비밀번호 기반 게시글 삭제
- 로그인 없이도 등록 시 설정한 비밀번호 4자리가 일치하면 삭제 가능
- **[Issue 5-1]** 삭제 인터페이스 구성 — 삭제 대상 게시글 선택 화면, 4자리 비밀번호 입력 폼 구성 및 입력값 형식 검증
- **[Issue 5-2]** 비밀번호 해싱 및 검증 로직 개발 — 입력 비밀번호를 해싱하여 저장된 해시값과 비교하는 인증 파이프라인 구축 (`auth.py`)
- **[Issue 5-3]** 인증 실패 예외 처리 및 재시도 로직 구현 — 비밀번호 불일치 시 에러 메시지 출력 및 재입력 유도
- **[Issue 5-4]** 검증 완료 데이터 삭제 연산 구현 — 인증 통과 시 `storage.py`를 통해 DB에서 해당 항목 완전 삭제 후 목록 갱신
