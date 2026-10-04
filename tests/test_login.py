
# tests/test_login.py
import pytest


# [TC-LOGIN-001] 정상 로그인 시 사용자 정보 및 200 응답 검증
def test_login_success(client):
    # 사전 조건: 로그인할 사용자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "login_test_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    # 생성한 계정으로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )

    # 로그인 응답의 상태 코드 및 사용자 정보 검증
    assert login_response.status_code == 200

    body = login_response.get_json()
    register_body = register_response.get_json()

    assert body["user_id"] == register_body["id"]
    assert body["username"] == "login_test_user"
    assert body["email"] == "login_test@example.com"


# [TC-LOGIN-002] 존재하지 않는 이메일로 로그인 시 401 응답 검증
def test_login_unknown_email(client):
    login_response = client.post(
        "/api/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 401
    assert login_response.get_json() == {
        "error": "이메일 또는 비밀번호가 잘못되었습니다."
    }


# [TC-LOGIN-003] 잘못된 비밀번호로 로그인 시 401 응답 검증
def test_login_wrong_password(client):
    # 사전 조건: 올바른 비밀번호로 사용자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "wrong_password_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    # 생성한 계정에 잘못된 비밀번호로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert login_response.status_code == 401
    assert login_response.get_json() == {
        "error": "이메일 또는 비밀번호가 잘못되었습니다."
    }


# [TC-LOGIN-004~005] 필수 필드 누락 시 400 응답 검증
@pytest.mark.parametrize(
    "missing_field",
    ["email", "password"],
)
def test_login_missing_required_field(client, missing_field):
    payload = {
        "email": "qa_test_001@example.com",
        "password": "TestPassword123!",
    }

    # 이번 테스트에서 검증할 필수 필드 하나만 제거
    payload.pop(missing_field)

    response = client.post("/api/login", json=payload)

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "이메일과 비밀번호를 확인해주세요."
    }


# [TC-LOGIN-006] 빈 문자열을 이메일로 전달했을 때 400 응답 검증
def test_login_empty_email(client):
    login_response = client.post(
        "/api/login",
        json={
            "email": "",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "이메일을 입력해주세요."
    }


# [TC-LOGIN-007] 빈 문자열을 비밀번호로 전달했을 때 400 응답 검증
def test_login_empty_password(client):
    # 사전 조건: 로그인할 사용자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "empty_password_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    # 빈 문자열을 비밀번호로 전달해 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "",
        },
    )

    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "비밀번호를 입력해주세요."
    }


# [TC-LOGIN-008] 공백만 입력한 이메일로 로그인 시 400 응답 검증
def test_login_whitespace_only_email(client):
    login_response = client.post(
        "/api/login",
        json={
            "email": "   ",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "이메일을 입력해주세요."
    }


# [TC-LOGIN-009] 공백만 입력한 비밀번호로 로그인 시 400 응답 검증
def test_login_whitespace_only_password(client):
    # 사전 조건: 로그인할 사용자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "whitespace_password_user",
            "email": "login_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    # 공백만 입력한 비밀번호로 로그인 요청
    login_response = client.post(
        "/api/login",
        json={
            "email": "login_test@example.com",
            "password": "   ",
        },
    )

    assert login_response.status_code == 400
    assert login_response.get_json() == {
        "error": "비밀번호를 입력해주세요."
    }
