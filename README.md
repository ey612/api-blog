# Flask Blog API

Flask 기반 블로그 REST API를 구현하고, pytest를 활용해 주요 기능을 자동으로 검증하는 개인 QA 프로젝트입니다.

회원가입, 로그인, 게시글 및 댓글 CRUD 기능을 제공하며, 정상·예외 상황에 대한 API 테스트와 테스트 데이터 격리를 통해 안정적인 테스트 환경을 구성했습니다.

## 기술 스택

- **Language:** Python 3.12
- **Backend:** Flask, Flask-SQLAlchemy, Flask-CORS
- **Database:** SQLite (로컬 및 테스트 환경), SQLAlchemy
- **Testing:** pytest
- **Deployment:** Render, Gunicorn

## 주요 기능

- 회원가입 및 로그인
- 게시글 생성, 조회, 수정, 삭제
- 댓글 생성, 조회, 수정, 삭제
- 필수 필드 누락 및 빈 문자열·공백 입력 검증
- 이메일 및 사용자 이름 중복 확인
- 비밀번호 해싱 및 로그인 정보 검증
- 로그인 처리 중 서버 오류 발생 시 내부 예외 정보 노출 방지

## 프로젝트 구조

```text
.
├── app.py                  # Flask 애플리케이션 생성 및 Blueprint 등록
├── config.py               # 환경변수 및 애플리케이션 설정
├── models.py               # 데이터베이스 모델
├── requirements.txt        # 프로젝트 의존성
├── render.yaml             # Render 배포 설정
├── routes/
│   ├── auth.py             # 회원가입 및 로그인 API
│   ├── posts.py            # 게시글 API
│   ├── comments.py         # 댓글 API
│   └── views.py
├── templates/
│   └── index.html          # 메인 페이지
└── tests/
    ├── conftest.py         # pytest fixture 및 테스트 DB 설정
    ├── helpers.py          # 테스트 사전 조건 생성용 공통 함수
    ├── test_register.py    # 회원가입 테스트
    ├── test_login.py       # 로그인 테스트
    ├── test_posts.py       # 게시글 테스트
    └── test_comments.py    # 댓글 테스트
```

## 로컬 실행 방법

### 1. 저장소 복제

```bash
git clone <저장소 URL>
cd <프로젝트 폴더>
```

### 2. 가상환경 생성 및 활성화

```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
```

### 3. 의존성 설치

```bash
python -m pip install -r requirements.txt
```

### 4. 환경변수 설정

프로젝트 최상위 경로에 `.env` 파일을 생성합니다.

```dotenv
DATABASE_URL=sqlite:///blog.db
SECRET_KEY=replace-with-your-own-secret-key
```

`SECRET_KEY`는 실제 사용 시 별도의 임의 문자열로 변경해야 합니다. `.env` 파일은 Git에 포함하지 않습니다.

### 5. 서버 실행

```bash
python app.py
```

기본 실행 주소: `http://localhost:5000`

## API 자동화 테스트

pytest를 사용하여 회원가입, 로그인, 게시글 및 댓글 API를 검증합니다.

| 테스트 파일 | 검증 대상 | 테스트 수 |
|---|---|---:|
| `test_register.py` | 회원가입 | 11 |
| `test_login.py` | 로그인 | 9 |
| `test_posts.py` | 게시글 CRUD | 8 |
| `test_comments.py` | 댓글 CRUD | 10 |
| **합계** | | **38** |

### 테스트 설계 및 구성

- 정상 및 비정상 요청에 대한 HTTP 상태 코드와 응답 데이터 검증
- 필수 필드 누락, 빈 문자열, 공백 입력 등의 예외 조건 검증
- `conftest.py`의 fixture를 이용한 테스트별 독립 SQLite DB 구성
- `helpers.py`를 통한 사용자 및 게시글 생성 사전 조건 재사용
- 필요한 경우 DB 재조회로 데이터 저장 및 변경 결과 검증

테스트 환경에서는 로컬 실행용 DB와 별도의 SQLite DB를 사용하여 테스트 간 데이터 간섭을 방지합니다.

### 전체 테스트 실행

```bash
python -m pytest tests/ -v
```

### 기능별 테스트 실행

```bash
python -m pytest tests/test_register.py -v
python -m pytest tests/test_login.py -v
python -m pytest tests/test_posts.py -v
python -m pytest tests/test_comments.py -v
```

## 배포 설정

Render에서 Gunicorn을 이용해 Flask 애플리케이션을 실행하도록 구성했습니다.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

배포 환경에서는 `DATABASE_URL`과 `SECRET_KEY`를 별도로 설정해야 합니다.

## 향후 개선

- GitHub Actions를 이용한 자동화 테스트 CI 구성
