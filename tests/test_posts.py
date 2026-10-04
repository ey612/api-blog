
from tests.helpers import create_post, create_user


# [TC-POST-001] 정상 게시글 생성 시 게시글 정보 및 201 응답 검증
def test_create_post_success(client):
    # 사전 조건: 게시글 작성자 생성
    user_id = create_user(
        client,
        username="post_test_user",
        email="post_test@example.com",
    )

    # 게시글 생성 요청
    post_response = client.post(
        "/api/posts",
        json={
            "title": "첫 번째 게시글",
            "content": "게시글 생성 테스트입니다.",
            "user_id": user_id,
        },
    )

    # 생성 응답의 상태 코드 및 게시글 정보 검증
    assert post_response.status_code == 201

    post = post_response.get_json()
    assert isinstance(post["id"], int)
    assert post["title"] == "첫 번째 게시글"
    assert post["content"] == "게시글 생성 테스트입니다."


# [TC-POST-002] 게시글 목록 조회 시 생성한 게시글 및 200 응답 검증
def test_get_posts_success(client):
    # 사전 조건: 게시글 작성자 및 조회할 게시글 생성
    user_id = create_user(
        client,
        username="post_list_test_user",
        email="post_list_test@example.com",
    )

    post_id = create_post(
        client,
        user_id=user_id,
        title="첫 번째 게시글",
        content="게시글 목록 조회 테스트입니다.",
    )

    # 게시글 목록 조회 요청
    posts_response = client.get("/api/posts")

    assert posts_response.status_code == 200

    posts = posts_response.get_json()
    assert isinstance(posts, list)

    # 생성한 게시글이 목록에 포함되는지 검증
    post = next(
        (item for item in posts if item["id"] == post_id),
        None,
    )

    assert post is not None
    assert post["title"] == "첫 번째 게시글"
    assert post["user_id"] == user_id
    assert "created_at" in post


# [TC-POST-003] 게시글 상세 조회 시 게시글 정보 및 200 응답 검증
def test_get_post_success(client):
    # 사전 조건: 게시글 작성자 및 조회할 게시글 생성
    user_id = create_user(
        client,
        username="post_detail_test_user",
        email="post_detail_test@example.com",
    )

    post_id = create_post(
        client,
        user_id=user_id,
        title="첫 번째 게시글",
        content="게시글 상세 조회 테스트입니다.",
    )

    # 게시글 상세 조회 요청
    response = client.get(f"/api/posts/{post_id}")

    assert response.status_code == 200

    post = response.get_json()
    assert post["id"] == post_id
    assert post["title"] == "첫 번째 게시글"
    assert post["content"] == "게시글 상세 조회 테스트입니다."
    assert post["user_id"] == user_id
    assert "created_at" in post


# [TC-POST-004] 게시글 수정 시 응답 및 저장 결과 검증
def test_put_post_success(client):
    # 사전 조건: 게시글 작성자 및 수정할 게시글 생성
    user_id = create_user(
        client,
        username="post_update_test_user",
        email="post_update_test@example.com",
    )

    post_id = create_post(
        client,
        user_id=user_id,
        title="첫 번째 게시글",
        content="게시글 수정 테스트입니다.",
    )

    # 게시글 수정 요청
    update_response = client.put(
        f"/api/posts/{post_id}",
        json={
            "title": "수정된 게시글",
            "content": "수정된 게시글 내용입니다.",
        },
    )

    # 수정 응답의 상태 코드 및 게시글 정보 검증
    assert update_response.status_code == 200

    post = update_response.get_json()
    assert post["id"] == post_id
    assert post["title"] == "수정된 게시글"
    assert post["content"] == "수정된 게시글 내용입니다."

    # 수정 내용의 실제 저장 여부를 상세 조회로 검증
    get_response = client.get(f"/api/posts/{post_id}")

    assert get_response.status_code == 200

    saved_post = get_response.get_json()
    assert saved_post["title"] == "수정된 게시글"
    assert saved_post["content"] == "수정된 게시글 내용입니다."


# [TC-POST-005] 게시글 삭제 시 응답 및 삭제 결과 검증
def test_delete_post_success(client):
    # 사전 조건: 게시글 작성자 및 삭제할 게시글 생성
    user_id = create_user(
        client,
        username="post_delete_test_user",
        email="post_delete_test@example.com",
    )

    post_id = create_post(
        client,
        user_id=user_id,
        title="삭제 테스트 게시글",
        content="게시글 삭제 테스트입니다.",
    )

    # 게시글 삭제 요청
    delete_response = client.delete(f"/api/posts/{post_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "게시글 삭제 완료."

    # 삭제 후 상세 조회 시 404 응답 검증
    get_response = client.get(f"/api/posts/{post_id}")

    assert get_response.status_code == 404
    assert get_response.get_json()["error"] == "게시글을 찾을 수 없습니다."


# [TC-POST-006] 존재하지 않는 게시글 상세 조회 시 404 응답 검증
def test_get_post_not_found(client):
    response = client.get("/api/posts/9999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "게시글을 찾을 수 없습니다."


# [TC-POST-007] 존재하지 않는 게시글 수정 시 404 응답 검증
def test_put_post_not_found(client):
    response = client.put(
        "/api/posts/9999",
        json={
            "title": "수정된 게시글",
            "content": "수정된 게시글 내용입니다.",
        },
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "게시글을 찾을 수 없습니다."


# [TC-POST-008] 존재하지 않는 게시글 삭제 시 404 응답 검증
def test_delete_post_not_found(client):
    response = client.delete("/api/posts/9999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "게시글을 찾을 수 없습니다."
