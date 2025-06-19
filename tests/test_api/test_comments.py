import pytest


@pytest.mark.asyncio
async def test_create_task_comment(client, create_user, get_token):
    user_email = "comment_user@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams", json={"name": "CommentTeam", "code": "COMT"}, headers=headers
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Comment Task", "description": "desc"},
        headers=headers,
    )
    task_id = task_resp.json()["id"]
    comment_data = {"text": "Мой комментарий"}
    resp = await client.post(
        f"/api/v1/task_comments/{task_id}", json=comment_data, headers=headers
    )
    assert resp.status_code in (201, 200)
    data = resp.json()
    assert data["text"] == "Мой комментарий"


@pytest.mark.asyncio
async def test_get_task_comments(client, create_user, get_token):
    user_email = "comment_user2@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams", json={"name": "CommentTeam2", "code": "COMT2"}, headers=headers
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Comment Task2", "description": "desc"},
        headers=headers,
    )
    task_id = task_resp.json()["id"]
    comment_data = {"text": "Второй комментарий"}
    await client.post(
        f"/api/v1/task_comments/{task_id}", json=comment_data, headers=headers
    )
    resp = await client.get(f"/api/v1/task_comments/{task_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(c["text"] == "Второй комментарий" for c in data)
