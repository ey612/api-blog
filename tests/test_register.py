# tests/test_register.py
import pytest
from werkzeug.security import check_password_hash
from models import User

def test_register_success(client):
    response = client.post(
        "/api/register",
        json={
            "username": "qa_test_001",
            "email": "qa_test_001@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    body = response.get_json()
    assert isinstance(body["id"], int)
    assert body["username"] == "qa_test_001"
    assert body["email"] == "qa_test_001@example.com"
    assert "password" not in body



def test_register_duplicate_email(client):
    # 사전 조건: 동일한 이메일을 가진 사용자 생성
    first_response = client.post(
        "/api/register",
        json={
            "username": "qa_test_001",
            "email": "duplicate@example.com",
            "password": "TestPassword123!",
        },
    )
    assert first_response.status_code == 201

    # 테스트: 다른 사용자 이름으로 동일한 이메일을 사용해 회원가입 시도
    response = client.post(
        "/api/register",
        json={
            "username": "qa_test_002",
            "email": "duplicate@example.com",
            "password": "AnotherPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "❌ 이미 존재하는 이메일입니다."
    }


def test_register_duplicate_username(client):
    # 사전 조건: 기존 사용자 생성
    first_response = client.post(
        "/api/register",
        json={
            "username": "duplicate_user",
            "email": "first@example.com",
            "password": "TestPassword123!",
        },
    )
    assert first_response.status_code == 201

    # 동일한 사용자 이름, 다른 이메일로 회원가입 시도
    response = client.post(
        "/api/register",
        json={
            "username": "duplicate_user",
            "email": "second@example.com",
            "password": "AnotherPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "❌ 이미 존재하는 이름입니다."
    }


# TC-REG-004(사용자 이름 누락), 005(이메일 누락), 006(비밀번호 누락)
@pytest.mark.parametrize(
    "missing_field",
    ["username", "email", "password"],
)
def test_register_missing_required_field(client, missing_field):
    payload = {
        "username": "qa_test_001",
        "email": "qa_test_001@example.com",
        "password": "TestPassword123!",
    }

    # 이번 실행에서 검증할 필수 항목 하나만 제거
    payload.pop(missing_field)

    response = client.post("/api/register", json=payload)

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "❗필수 항목을 입력해주세요."
    }


'''
[TC-REG-007] 빈 사용자 이름으로 회원가입 시도
- 기존 api에서는 빈 문자열이나 공백만 있는 사용자 이름을 허용했으나,
- auth.py의 register() 함수에서 사용자 이름이 빈 문자열이거나 공백만 있는 경우를 거부하도록 로직을 추가
- 따라서, 빈 문자열이나 공백만 있는 사용자 이름으로 회원가입 시도 시
  400 상태 코드와 함께 적절한 오류 메시지를 반환하는지 검증

'''

def test_register_empty_username(client):
    response = client.post(
        "/api/register",
        json={
            "username": "",
            "email": "empty_username@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 400

# [TC-REG-008] 공백만 있는 사용자 이름
def test_register_whitespace_only_username(client):
    response = client.post(
        "/api/register",
        json={
            "username": "   ",
            "email": "whitespace_username@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "❗사용자 이름을 입력해주세요."
    }

# [TC-REG-009] 빈 이메일로 회원가입 시도
def test_register_empty_email(client):
    response = client.post(
        "/api/register",
        json={
            "username": "empty_email_user",
            "email": "",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "❗이메일을 입력해주세요."
    }


# [TC-REG-010] 빈 비밀번호로 회원가입 시도
def test_register_empty_password(client):
    response = client.post(
        "/api/register",
        json={
            "username": "empty_password_user",
            "email": "empty_password@example.com",
            "password": "",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "❗비밀번호를 입력해주세요."
    } 

# [TC-REG-011] 비밀번호 해싱 검증
def test_register_password_is_hashed(client, app):
    plain_password = "TestPassword123!"

    response = client.post(
        "/api/register",
        json={
            "username": "hash_test_user",
            "email": "password_hash@example.com",
            "password": plain_password,
        },
    )

    assert response.status_code == 201

    # 회원가입 후 테스트 DB에서 해당 사용자를 조회
    with app.app_context():
        user = User.query.filter_by(email="password_hash@example.com").first()

        assert user is not None
        
        # 저장된 비밀번호가 평문이 아닌지 확인
        assert user.password != plain_password

        # 저장된 해시로 원래 비밀번호를 검증할 수 있는지 확인
        assert check_password_hash(user.password, plain_password)