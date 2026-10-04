# tests/helpers.py


def create_user(client, username, email):
    response = client.post(
        "/api/register",
        json={
            "username": username,
            "email": email,
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 201

    return response.get_json()["id"]


def create_post(client, user_id, title, content):
    response = client.post(
        "/api/posts",
        json={
            "title": title,
            "content": content,
            "user_id": user_id,
        },
    )
    assert response.status_code == 201

    return response.get_json()["id"]