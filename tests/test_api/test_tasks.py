import pytest


@pytest.mark.asyncio
async def test_create_task(client, create_user, get_token):
    admin_email = "admin_task@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "TaskTeam", "code": "TASKT"},
        headers=admin_headers,
    )
    assert team_resp.status_code == 201

    resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "desc"},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "desc"


@pytest.mark.asyncio
async def test_create_task_without_team(client, create_user, get_token):
    user_email = "user_notaskteam@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)

    resp = await client.post(
        "/api/v1/tasks",
        json={"title": "No Team Task", "description": "desc"},
        headers=headers,
    )
    assert resp.status_code == 403 or resp.status_code == 400


@pytest.mark.asyncio
async def test_update_task(client, create_user, get_token):
    admin_email = "admin_upd@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams", json={"name": "UpdTeam", "code": "UPDT"}, headers=admin_headers
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Old Task", "description": "old"},
        headers=admin_headers,
    )
    task_id = task_resp.json()["id"]

    upd_resp = await client.patch(
        f"/api/v1/tasks/{task_id}", json={"title": "New Task"}, headers=admin_headers
    )
    assert upd_resp.status_code == 200
    data = upd_resp.json()
    assert data["title"] == "New Task"


@pytest.mark.asyncio
async def test_update_task_not_owner(client, create_user, get_token):
    owner_email = "owner@example.com"
    owner_password = "12345678"
    await create_user(client, owner_email, owner_password)
    owner_headers = await get_token(client, owner_email, owner_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "OwnerTeam", "code": "OWNR"},
        headers=owner_headers,
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Owner Task", "description": "desc"},
        headers=owner_headers,
    )
    task_id = task_resp.json()["id"]

    user_email = "notowner@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]
    await client.post(
        f"/api/v1/teams/{team_resp.json()['id']}/user/{user_id}", headers=owner_headers
    )
    user_headers = await get_token(client, user_email, user_password)

    upd_resp = await client.patch(
        f"/api/v1/tasks/{task_id}", json={"title": "Hack Task"}, headers=user_headers
    )
    assert upd_resp.status_code == 403


@pytest.mark.asyncio
async def test_delete_task(client, create_user, get_token):
    admin_email = "admin_del_task@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "DelTaskTeam", "code": "DTASK"},
        headers=admin_headers,
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Task to delete", "description": "desc"},
        headers=admin_headers,
    )
    task_id = task_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/tasks/{task_id}", headers=admin_headers)
    assert del_resp.status_code == 200 or del_resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_task_not_owner(client, create_user, get_token):
    owner_email = "owner_del@example.com"
    owner_password = "12345678"
    await create_user(client, owner_email, owner_password)
    owner_headers = await get_token(client, owner_email, owner_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "DelOwnerTeam", "code": "DLOWN"},
        headers=owner_headers,
    )
    task_resp = await client.post(
        "/api/v1/tasks",
        json={"title": "Owner's Task", "description": "desc"},
        headers=owner_headers,
    )
    task_id = task_resp.json()["id"]

    user_email = "notowner_del@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]
    await client.post(
        f"/api/v1/teams/{team_resp.json()['id']}/user/{user_id}", headers=owner_headers
    )
    user_headers = await get_token(client, user_email, user_password)

    del_resp = await client.delete(f"/api/v1/tasks/{task_id}", headers=user_headers)
    assert del_resp.status_code == 403
