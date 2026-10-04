
#tests/test_comments.py
import pytest


# [TC-COM-001] 정상 댓글 생성 시 댓글 정보 및 201 응답 검증
def test_create_comment_success(client):
    # 사전 조건: 댓글 작성자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "comment_test_user",
            "email": "comment_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 사전 조건: 댓글을 작성할 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "댓글 테스트 게시글",
            "content": "댓글을 작성할 게시글입니다.",
            "user_id": user_id,
        },
    )
    assert post_response.status_code == 201

    post_id = post_response.get_json()["id"]

    # 댓글 생성 요청
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "첫 번째 댓글입니다.",
            "user_id": user_id,
        },
    )

    # 생성 응답의 상태 코드 및 댓글 정보 검증
    assert comment_response.status_code == 201

    comment = comment_response.get_json()
    assert isinstance(comment["id"], int)
    assert comment["post_id"] == post_id
    assert comment["content"] == "첫 번째 댓글입니다."
    assert comment["user_id"] == user_id
    assert "created_at" in comment


# [TC-COM-002] 댓글 목록 조회 시 생성한 댓글 및 200 응답 검증
def test_get_comments_success(client):
    # 사전 조건: 댓글 작성자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "comment_list_test_user",
            "email": "comment_list_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 사전 조건: 댓글을 작성할 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "댓글 목록 테스트 게시글",
            "content": "댓글 목록을 조회할 게시글입니다.",
            "user_id": user_id,
        },
    )
    assert post_response.status_code == 201

    post_id = post_response.get_json()["id"]

    # 사전 조건: 조회할 댓글 생성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "댓글 목록 조회 테스트 댓글입니다.",
            "user_id": user_id,
        },
    )
    assert comment_response.status_code == 201

    comment_id = comment_response.get_json()["id"]

    # 댓글 목록 조회 요청
    comments_response = client.get(f"/api/posts/{post_id}/comments")

    assert comments_response.status_code == 200

    comments = comments_response.get_json()
    assert isinstance(comments, list)
    assert len(comments) == 1

    # 생성한 댓글의 정보 검증
    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "댓글 목록 조회 테스트 댓글입니다."
    assert comments[0]["user_id"] == user_id
    assert "created_at" in comments[0]


# [TC-COM-003] 댓글 수정 시 응답 및 저장 결과 검증
def test_update_comment_success(client):
    # 사전 조건: 댓글 작성자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "comment_update_test_user",
            "email": "comment_update_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 사전 조건: 댓글을 작성할 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "댓글 수정 테스트 게시글",
            "content": "댓글을 수정할 게시글입니다.",
            "user_id": user_id,
        },
    )
    assert post_response.status_code == 201

    post_id = post_response.get_json()["id"]

    # 사전 조건: 수정할 댓글 생성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "수정 전 댓글입니다.",
            "user_id": user_id,
        },
    )
    assert comment_response.status_code == 201

    comment_id = comment_response.get_json()["id"]

    # 댓글 수정 요청
    update_response = client.put(
        f"/api/comments/{comment_id}",
        json={
            "content": "수정 후 댓글입니다.",
        },
    )

    # 수정 응답의 상태 코드 및 댓글 정보 검증
    assert update_response.status_code == 200

    updated_comment = update_response.get_json()
    assert updated_comment["id"] == comment_id
    assert updated_comment["content"] == "수정 후 댓글입니다."
    assert updated_comment["user_id"] == user_id
    assert updated_comment["post_id"] == post_id
    assert "created_at" in updated_comment

    # 수정 내용의 실제 저장 여부를 댓글 목록 조회로 검증
    get_response = client.get(f"/api/posts/{post_id}/comments")

    assert get_response.status_code == 200

    comments = get_response.get_json()
    assert len(comments) == 1
    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "수정 후 댓글입니다."


# [TC-COM-004] 댓글 삭제 시 응답 및 삭제 결과 검증
def test_delete_comment_success(client):
    # 사전 조건: 댓글 작성자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "comment_delete_test_user",
            "email": "comment_delete_test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 사전 조건: 댓글을 작성할 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "댓글 삭제 테스트 게시글",
            "content": "댓글을 삭제할 게시글입니다.",
            "user_id": user_id,
        },
    )
    assert post_response.status_code == 201

    post_id = post_response.get_json()["id"]

    # 사전 조건: 삭제할 댓글 생성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "삭제 전 댓글입니다.",
            "user_id": user_id,
        },
    )
    assert comment_response.status_code == 201

    comment_id = comment_response.get_json()["id"]

    # 댓글 삭제 요청
    delete_response = client.delete(f"/api/comments/{comment_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "댓글 삭제 완료."

    # 삭제 후 댓글 목록이 비어 있는지 검증
    get_response = client.get(f"/api/posts/{post_id}/comments")

    assert get_response.status_code == 200

    comments = get_response.get_json()
    assert isinstance(comments, list)
    assert len(comments) == 0


# [TC-COM-005] 존재하지 않는 게시글에 댓글 생성 시 404 응답 검증
def test_create_comment_nonexistent_post(client):
    # 사전 조건: 댓글 작성자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "comment_nonexistent_post_user",
            "email": "comment_nonexistent_post@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 존재하지 않는 게시글 ID로 댓글 생성 요청
    nonexistent_post_id = 999999

    comment_response = client.post(
        f"/api/posts/{nonexistent_post_id}/comments",
        json={
            "content": "존재하지 않는 게시글에 대한 댓글입니다.",
            "user_id": user_id,
        },
    )

    assert comment_response.status_code == 404
    assert comment_response.get_json()["error"] == "게시글을 찾을 수 없습니다."


# [TC-COM-006] 존재하지 않는 게시글의 댓글 목록 조회 시 404 응답 검증
def test_get_comments_nonexistent_post(client):
    nonexistent_post_id = 999999

    comments_response = client.get(
        f"/api/posts/{nonexistent_post_id}/comments"
    )

    assert comments_response.status_code == 404
    assert comments_response.get_json()["error"] == "게시글을 찾을 수 없습니다."


# [TC-COM-007] 존재하지 않는 댓글 수정 시 404 응답 검증
def test_update_comment_nonexistent(client):
    nonexistent_comment_id = 999999

    update_response = client.put(
        f"/api/comments/{nonexistent_comment_id}",
        json={
            "content": "존재하지 않는 댓글을 수정하려고 합니다.",
        },
    )

    assert update_response.status_code == 404
    assert update_response.get_json()["error"] == "댓글을 찾을 수 없습니다."


# [TC-COM-008] 존재하지 않는 댓글 삭제 시 404 응답 검증
def test_delete_comment_nonexistent(client):
    nonexistent_comment_id = 999999

    delete_response = client.delete(
        f"/api/comments/{nonexistent_comment_id}"
    )

    assert delete_response.status_code == 404
    assert delete_response.get_json()["error"] == "댓글을 찾을 수 없습니다."


# [TC-COM-009~010] 댓글 생성 시 필수 필드 누락에 대한 400 응답 검증
@pytest.mark.parametrize("missing_field", ["content", "user_id"])
def test_create_comment_missing_fields(client, missing_field):
    # 사전 조건: 댓글 작성자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "comment_missing_field_user",
            "email": "comment_missing_field@example.com",
            "password": "TestPassword123!",
        },
    )
    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 사전 조건: 댓글을 작성할 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "댓글 필수 필드 누락 테스트 게시글",
            "content": "댓글 작성 시 필수 필드 누락 테스트 게시글입니다.",
            "user_id": user_id,
        },
    )
    assert post_response.status_code == 201

    post_id = post_response.get_json()["id"]

    # 이번 테스트에서 검증할 필수 필드 하나만 제거
    payload = {
        "content": "필수값 누락 테스트 댓글입니다.",
        "user_id": user_id,
    }
    payload.pop(missing_field)

    # 필수 필드가 누락된 댓글 생성 요청
    response = client.post(
        f"/api/posts/{post_id}/comments",
        json=payload,
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "잘못된 접근입니다."
