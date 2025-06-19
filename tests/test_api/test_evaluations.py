import pytest


@pytest.mark.asyncio
async def test_create_evaluation(client, create_user, get_token):
    user_email = "eval_user@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams", json={"name": "EvalTeam", "code": "EVALT"}, headers=headers
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Eval Task", "description": "desc"},
        headers=headers,
    )
    task_id = task_resp.json()["id"]
    eval_data = {"score": 5, "comment": "Отлично"}
    resp = await client.post(
        f"/api/v1/evaluations/{task_id}", json=eval_data, headers=headers
    )
    assert resp.status_code in (201, 200)
    data = resp.json()
    assert data["score"] == 5
    assert data["comment"] == "Отлично"


@pytest.mark.asyncio
async def test_get_evaluations(client, create_user, get_token):
    user_email = "eval_user2@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams", json={"name": "EvalTeam2", "code": "EVALT2"}, headers=headers
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Eval Task2", "description": "desc"},
        headers=headers,
    )
    task_id = task_resp.json()["id"]
    eval_data = {"score": 4, "comment": "Хорошо"}
    await client.post(f"/api/v1/evaluations/{task_id}", json=eval_data, headers=headers)
    resp = await client.get("/api/v1/evaluations", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(e["score"] == 4 for e in data)
