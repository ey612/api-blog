

# [TC-POST-001] 정상 게시글 생성
def test_create_post_success(client):
    # 1. 사전 조건: 사용자 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "post_test_user",
            "email": "post_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    user_id = register_response.get_json()["id"]

    # 2. 게시글 생성 요청
    post_response = client.post(
        "/api/posts",
        json={
            "title": "첫 번째 게시글",
            "content": "게시글 생성 테스트입니다.",
            "user_id": user_id,
        },
    )

    # 3. 결과 검증
    assert post_response.status_code == 201
    post_id = post_response.get_json()["id"]
    assert isinstance(post_id, int)
    assert post_response.get_json()["title"] == "첫 번째 게시글"
    assert post_response.get_json()["content"] == "게시글 생성 테스트입니다."



#[TC-POST-002] 게시글 목록 조회
def test_get_posts_success(client):
    # 1. 사전 조건: 사용자 생성 및 게시글 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "post1_list_test_user",
            "email": "post1_list_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.get_json()["id"]

    # 2. 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "첫 번째 게시글",
            "content": "게시글 목록 조회 테스트입니다.",
            "user_id": user_id,
        },
    )

    assert post_response.status_code == 201

    # 3. 게시글 목록 조회 요청
    posts_response = client.get("/api/posts")

    # 4. 결과 검증
    assert posts_response.status_code == 200

    posts = posts_response.get_json()
    post_id = post_response.get_json()["id"]
    assert isinstance(posts, list)

    post = next(
        (item for item in posts if item["id"] == post_id),
        None,
    )

    assert post is not None
    assert post["title"] == "첫 번째 게시글"
    assert post["user_id"] == user_id
    assert "created_at" in post



#[TC-POST-003] 게시글 상세 조회
def test_get_post_success(client):
    # 1. 사전 조건: 사용자 생성 및 게시글 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "post_detail_test_user",
            "email": "post_detail_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.get_json()["id"]

    # 2. 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "첫 번째 게시글",
            "content": "게시글 상세 조회 테스트입니다.",
            "user_id": user_id,
        },
    )

    assert post_response.status_code == 201
    post_id = post_response.get_json()["id"]

    # 3. 게시글 상세 조회 요청
    response = client.get(f"/api/posts/{post_id}")

    # 4. 결과 검증
    assert response.status_code == 200

    post = response.get_json()
    assert post["id"] == post_id
    assert post["title"] == "첫 번째 게시글"
    assert post["content"] == "게시글 상세 조회 테스트입니다."
    assert post["user_id"] == user_id
    assert "created_at" in post


#[TC-POST-004] 게시글 수정
def test_put_post_success(client):
    # 1. 사전 조건: 사용자 생성 및 게시글 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "post_update_test_user",
            "email": "post_update_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.get_json()["id"]

    # 2. 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "첫 번째 게시글",
            "content": "게시글 수정 테스트입니다.",
            "user_id": user_id,
        },
    )

    assert post_response.status_code == 201
    post_id = post_response.get_json()["id"]

    # 3. 게시글 수정
    update_response = client.put(
        f"/api/posts/{post_id}",
        json={
            "title": "수정된 게시글",
            "content": "수정된 게시글 내용입니다.",
        },
    )

    # 4. 결과 검증
    assert update_response.status_code == 200

    post = update_response.get_json()
    assert post["id"] == post_id
    assert post["title"] == "수정된 게시글"
    assert post["content"] == "수정된 게시글 내용입니다."

    # 5. 수정 내용이 실제로 저장되었는지 재조회
    get_response = client.get(f"/api/posts/{post_id}")

    assert get_response.status_code == 200

    saved_post = get_response.get_json()
    assert saved_post["title"] == "수정된 게시글"
    assert saved_post["content"] == "수정된 게시글 내용입니다."


#[TC-POST-005] 정상 게시글 삭제
def test_delete_post_success(client):
    # 1. 사전 조건: 사용자 생성 및 게시글 생성
    register_response = client.post(
        "/api/register",
        json={
            "username": "post_delete_test_user",
            "email": "post_delete_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.get_json()["id"]

    # 2. 게시글 생성
    post_response = client.post(
        "/api/posts",
        json={
            "title": "삭제 테스트 게시글",
            "content": "게시글 삭제 테스트입니다.",
            "user_id": user_id,
        },
    )

    assert post_response.status_code == 201
    post_id = post_response.get_json()["id"]

    # 3. 게시글 삭제
    delete_response = client.delete(f"/api/posts/{post_id}")

    # 4. 삭제 응답 검증
    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "게시글 삭제 완료."

    # 5. 삭제 후 상세 조회
    get_response = client.get(f"/api/posts/{post_id}")

    assert get_response.status_code == 404
    assert get_response.get_json()["error"] == "게시글을 찾을 수 없습니다."


#[TC-POST-006] 존재하지 않는 게시글 조회
def test_get_post_not_found(client):
    # 1. 존재하지 않는 게시글 조회 요청
    response = client.get("/api/posts/9999")

    # 2. 결과 검증
    assert response.status_code == 404
    assert response.get_json()["error"] == "게시글을 찾을 수 없습니다."


#[TC-POST-007] 존재하지 않는 게시글 수정
def test_put_post_not_found(client):
    # 1. 존재하지 않는 게시글 수정 요청
    response = client.put(
        "/api/posts/9999",
        json={
            "title": "수정된 게시글",
            "content": "수정된 게시글 내용입니다.",
        },
    )

    # 2. 결과 검증
    assert response.status_code == 404
    assert response.get_json()["error"] == "게시글을 찾을 수 없습니다."


#[TC-POST-008] 존재하지 않는 게시글 삭제
def test_delete_post_not_found(client):
    # 1. 존재하지 않는 게시글 삭제 요청
    response = client.delete("/api/posts/9999")

    # 2. 결과 검증
    assert response.status_code == 404
    assert response.get_json()["error"] == "게시글을 찾을 수 없습니다."