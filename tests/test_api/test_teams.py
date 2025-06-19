import pytest


@pytest.mark.asyncio
async def test_create_team(client, create_user, get_token):
    email = "admin1@example.com"
    password = "12345678"
    await create_user(client, email, password, role="admin")
    headers = await get_token(client, email, password)

    resp = await client.post(
        "/api/v1/teams", json={"name": "Test Team", "code": "TST"}, headers=headers
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Team"
    assert data["code"] == "TST"
    assert data["admin_id"]


@pytest.mark.asyncio
async def test_create_team_not_admin(client, create_user, get_token):
    email = "user1@example.com"
    password = "12345678"
    await create_user(client, email, password, role="user")
    headers = await get_token(client, email, password)
    resp = await client.post(
        "/api/v1/teams", json={"name": "No Rights", "code": "NRG"}, headers=headers
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_admin_adds_user_to_team(client, create_user, get_token):
    admin_email = "admin2@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)

    team_resp = await client.post(
        "/api/v1/teams", json={"name": "Team2", "code": "TST2"}, headers=admin_headers
    )
    assert team_resp.status_code == 201
    team_id = team_resp.json()["id"]

    user_email = "user2@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]

    add_resp = await client.post(
        f"/api/v1/teams/{team_id}/user/{user_id}", headers=admin_headers
    )
    assert add_resp.status_code == 201


@pytest.mark.asyncio
async def test_non_admin_cannot_add_user_to_team(client, create_user, get_token):
    admin_email = "admin3@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams", json={"name": "Team3", "code": "TST3"}, headers=admin_headers
    )
    team_id = team_resp.json()["id"]

    user_email = "user3@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]

    not_admin_email = "user4@example.com"
    not_admin_password = "12345678"
    await create_user(client, not_admin_email, not_admin_password)
    not_admin_headers = await get_token(client, not_admin_email, not_admin_password)

    add_resp = await client.post(
        f"/api/v1/teams/{team_id}/user/{user_id}", headers=not_admin_headers
    )
    assert add_resp.status_code == 403


@pytest.mark.asyncio
async def test_cannot_add_user_already_in_team(client, create_user, get_token):
    admin_email = "admin5@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams", json={"name": "Team5", "code": "TST5"}, headers=admin_headers
    )
    team_id = team_resp.json()["id"]

    user_email = "user5@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]
    await client.post(f"/api/v1/teams/{team_id}/user/{user_id}", headers=admin_headers)

    add_resp = await client.post(
        f"/api/v1/teams/{team_id}/user/{user_id}", headers=admin_headers
    )
    assert add_resp.status_code == 400


@pytest.mark.asyncio
async def test_admin_removes_user_from_team(client, create_user, get_token):
    admin_email = "admin_del@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams", json={"name": "TeamDel", "code": "TDEL"}, headers=admin_headers
    )
    team_id = team_resp.json()["id"]

    user_email = "user_del@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]
    await client.post(f"/api/v1/teams/{team_id}/user/{user_id}", headers=admin_headers)

    del_resp = await client.delete(
        f"/api/v1/teams/{team_id}/user/{user_id}", headers=admin_headers
    )
    assert del_resp.status_code == 204


@pytest.mark.asyncio
async def test_non_admin_cannot_remove_user_from_team(client, create_user, get_token):
    admin_email = "admin_del2@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "TeamDel2", "code": "TDEL2"},
        headers=admin_headers,
    )
    team_id = team_resp.json()["id"]

    user_email = "user_del2@example.com"
    user_password = "12345678"
    user = await create_user(client, user_email, user_password)
    user_id = user["id"]
    await client.post(f"/api/v1/teams/{team_id}/user/{user_id}", headers=admin_headers)

    not_admin_email = "user_notadmin@example.com"
    not_admin_password = "12345678"
    await create_user(client, not_admin_email, not_admin_password)
    not_admin_headers = await get_token(client, not_admin_email, not_admin_password)

    del_resp = await client.delete(
        f"/api/v1/teams/{team_id}/user/{user_id}", headers=not_admin_headers
    )
    assert del_resp.status_code == 403


@pytest.mark.asyncio
async def test_cannot_remove_team_admin(client, create_user, get_token):
    admin_email = "admin_del3@example.com"
    admin_password = "12345678"
    await create_user(client, admin_email, admin_password)
    admin_headers = await get_token(client, admin_email, admin_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "TeamDel3", "code": "TDEL3"},
        headers=admin_headers,
    )
    team_id = team_resp.json()["id"]

    del_resp = await client.delete(
        f"/api/v1/teams/{team_id}/user/{team_resp.json()['admin_id']}",
        headers=admin_headers,
    )
    assert del_resp.status_code == 400
