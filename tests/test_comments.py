import pytest

# [TC-COM-001] 정상 댓글 작성
def test_create_comment_success(client):
    # 1. 사용자 생성
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

    # 2. 게시글 생성
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

    # 3. 댓글 작성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "첫 번째 댓글입니다.",
            "user_id": user_id,
        },
    )

    # 4. 결과 검증
    assert comment_response.status_code == 201
    assert isinstance(comment_response.get_json()["id"], int)
    assert comment_response.get_json()["post_id"] == post_id
    assert comment_response.get_json()["content"] == "첫 번째 댓글입니다."
    assert comment_response.get_json()["user_id"] == user_id
    assert "created_at" in comment_response.get_json()


#[TC-COM-002] 댓글 목록 조회
def test_get_comments_success(client):
    # 1. 사용자 생성
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

    # 2. 게시글 생성
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

    # 3. 댓글 작성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "댓글 목록 조회 테스트 댓글입니다.",
            "user_id": user_id,
        },
    )

    assert comment_response.status_code == 201
    comment_id = comment_response.get_json()["id"]

    # 4. 댓글 목록 조회
    comments_response = client.get(f"/api/posts/{post_id}/comments")

    # 5. 결과 검증
    assert comments_response.status_code == 200

    comments = comments_response.get_json()

    assert isinstance(comments, list)
    assert len(comments) == 1

    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "댓글 목록 조회 테스트 댓글입니다."
    assert comments[0]["user_id"] == user_id
    assert "created_at" in comments[0]


#[TC-COM-003] 댓글 수정
def test_update_comment_success(client):
    # 1. 사용자 생성
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

    # 2. 게시글 생성
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

    # 3. 댓글 작성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "수정 전 댓글입니다.",
            "user_id": user_id,
        },
    )   

    assert comment_response.status_code == 201
    comment_id = comment_response.get_json()["id"]

    # 4. 댓글 수정
    update_response = client.put(
        f"/api/comments/{comment_id}",
        json={
            "content": "수정 후 댓글입니다.",
        },
    )   

    # 5. 수정 응답 검증
    assert update_response.status_code == 200

    updated_comment = update_response.get_json()

    assert updated_comment["id"] == comment_id
    assert updated_comment["content"] == "수정 후 댓글입니다."
    assert updated_comment["user_id"] == user_id
    assert updated_comment["post_id"] == post_id
    assert "created_at" in updated_comment

    # 6. 수정 내용이 실제로 저장되었는지 재조회
    get_response = client.get(f"/api/posts/{post_id}/comments")

    assert get_response.status_code == 200

    comments = get_response.get_json()
    assert len(comments) == 1
    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "수정 후 댓글입니다."


#[TC-COM-004] 댓글 삭제
def test_delete_comment_success(client):
    # 1. 사용자 생성
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

    # 2. 게시글 생성
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

    # 3. 댓글 작성
    comment_response = client.post(
        f"/api/posts/{post_id}/comments",
        json={
            "content": "삭제 전 댓글입니다.",
            "user_id": user_id,
        },
    )   

    assert comment_response.status_code == 201
    comment_id = comment_response.get_json()["id"]

    # 4. 댓글 삭제
    delete_response = client.delete(f"/api/comments/{comment_id}")

    # 5. 삭제 응답 검증
    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "댓글 삭제 완료."

    # 6. 삭제된 댓글이 목록에 존재하지 않는지 확인
    get_response = client.get(f"/api/posts/{post_id}/comments")

    assert get_response.status_code == 200

    comments = get_response.get_json()

    assert isinstance(comments, list)
    assert len(comments) == 0


#[TC-COM-005] 존재하지 않는 게시글에 댓글 작성 시도
def test_create_comment_nonexistent_post(client):
    # 1. 사용자 생성
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

    # 2. 존재하지 않는 게시글 ID 사용
    nonexistent_post_id = 999999

    # 3. 댓글 작성 시도
    comment_response = client.post(
        f"/api/posts/{nonexistent_post_id}/comments",
        json={
            "content": "존재하지 않는 게시글에 대한 댓글입니다.",
            "user_id": user_id,
        },
    )

    # 4. 댓글 작성 실패 응답 검증
    assert comment_response.status_code == 404
    assert comment_response.get_json()["error"] == "게시글을 찾을 수 없습니다."


#[TC-COM-006] 존재하지 않는 게시글의 댓글 목록 조회
def test_get_comments_nonexistent_post(client):
    # 1. 존재하지 않는 게시글 ID 사용
    nonexistent_post_id = 999999

    # 2. 댓글 목록 조회 시도
    comments_response = client.get(f"/api/posts/{nonexistent_post_id}/comments")

    # 3. 댓글 목록 조회 실패 응답 검증
    assert comments_response.status_code == 404
    assert comments_response.get_json()["error"] == "게시글을 찾을 수 없습니다."

#[TC-COM-007] 존재하지 않는 댓글 수정 시도
def test_update_comment_nonexistent(client):
    # 1. 존재하지 않는 댓글 ID 사용
    nonexistent_comment_id = 999999

    # 2. 댓글 수정 시도
    update_response = client.put(
        f"/api/comments/{nonexistent_comment_id}",
        json={
            "content": "존재하지 않는 댓글을 수정하려고 합니다.",
        },
    )

    # 3. 댓글 수정 실패 응답 검증
    assert update_response.status_code == 404
    assert update_response.get_json()["error"] == "댓글을 찾을 수 없습니다."


#[TC-COM-008] 존재하지 않는 댓글 삭제 시도
def test_delete_comment_nonexistent(client):
    # 1. 존재하지 않는 댓글 ID 사용
    nonexistent_comment_id = 999999

    # 2. 댓글 삭제 시도
    delete_response = client.delete(f"/api/comments/{nonexistent_comment_id}")

    # 3. 댓글 삭제 실패 응답 검증
    assert delete_response.status_code == 404
    assert delete_response.get_json()["error"] == "댓글을 찾을 수 없습니다."


#[TC-COM-009][TC-COM-010] 댓글 작성 시 필수 필드 누락

@pytest.mark.parametrize("missing_field", ["content", "user_id"])
def test_create_comment_missing_fields(client, missing_field):
    # 1. 사용자 생성
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

    # 2. 게시글 생성
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

    # 3. 정상 요청 데이터 생성
    payload = {
        "content": "필수값 누락 테스트 댓글입니다.",
        "user_id": user_id,
    }

    # 4. 필수 필드 제거
    payload.pop(missing_field)

    # 5. 댓글 작성 시도
    response = client.post(
        f"/api/posts/{post_id}/comments",
        json=payload,
    )

    # 6. 댓글 작성 실패 응답 검증
    assert response.status_code == 400
    assert response.get_json()["error"] == "잘못된 접근입니다."