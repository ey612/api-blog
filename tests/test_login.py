import pytest

# [TC-LOGIN-001] 정상 로그인
def test_login_success(client):

    # 1. 사전 조건: 회원가입으로 사용자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "login_test_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    # 2. 생성한 계정으로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )

    # 3. 로그인 결과 검증
    assert login_response.status_code == 200

    body = login_response.get_json()

    register_body = register_response.get_json()

    assert body["user_id"] == register_body["id"]
    assert body["username"] == "login_test_user"
    assert body["email"] == "login_test@example.com"

# [TC-LOGIN-002] 존재하지 않는 이메일로 로그인 시도
def test_login_unknown_email(client):

    # 1. 가입되지 않은 이메일로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123!",
        },
    )

    # 2. 로그인 결과 검증
    assert login_response.status_code == 401

    assert login_response.get_json() == {
        "error": "이메일 또는 비밀번호가 잘못되었습니다."
    }


# [TC-LOGIN-003] 잘못된 비밀번호로 로그인 시도
def test_login_wrong_password(client):

    # 1. 사전 조건: 회원가입으로 사용자 생성
    register_response = client.post(
    "/api/register",
    json={
        "username": "wrong_password_user",
        "email": "login_test@example.com",
        "password": "TestPassword123!",
    },
)

    assert register_response.status_code == 201


    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "WrongPassword123!",
        },
    )

    # 2. 로그인 결과 검증
    assert login_response.status_code == 401

    assert login_response.get_json() == {
        "error": "이메일 또는 비밀번호가 잘못되었습니다."
    }


#[TC-LOGIN-004][TC-LOGIN-005] 이메일과 비밀번호 누락
@pytest.mark.parametrize(
    "missing_field",
    ["email", "password"],
)
def test_login_missing_required_field(client, missing_field):
    payload = {
        "email": "qa_test_001@example.com",
        "password": "TestPassword123!",
    }

    # 이번 실행에서 검증할 필수 항목 하나만 제거
    payload.pop(missing_field)

    response = client.post("/api/login", json=payload)

    assert response.status_code == 400

    assert response.get_json() == {
        "error": "이메일과 비밀번호를 확인해주세요."
    }



# [TC-LOGIN-006] 빈 이메일 로그인 시도
def test_login_empty_email(client):

    # 1. 빈 이메일로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "",
            "password": "TestPassword123!",
        },
    )

    # 2. 로그인 결과 검증
    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "이메일을 입력해주세요."
    }


# [TC-LOGIN-007] 빈 비밀번호로 로그인 시도
def test_login_empty_password(client):
    register_response = client.post(
        "/api/register",
        json={
            "username": "empty_password_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201


    # 2. 빈 비밀번호로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "",
        },
    )

    # 3. 로그인 결과 검증
    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "비밀번호를 입력해주세요."
    }

# [TC-LOGIN-008] 공백 이메일로 로그인 시도
def test_login_whitespace_email(client):

    # 1. 공백 이메일로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "   ",
            "password": "TestPassword123!",
        },
    )

    # 2. 로그인 결과 검증
    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "이메일을 입력해주세요."
    }


# [TC-LOGIN-009] 공백 비밀번호로 로그인 시도
def test_login_whitespace_password(client):
    register_response = client.post(
        "/api/register",
        json={
            "username": "empty_password_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201


    # 2. 공백 비밀번호로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "   ",
        },
    )

    # 3. 로그인 결과 검증
    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "비밀번호를 입력해주세요."
    }