import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_create_meeting(client, create_user, get_token):
    manager_email = "manager_meeting@example.com"
    manager_password = "12345678"
    await create_user(client, manager_email, manager_password)
    manager_headers = await get_token(client, manager_email, manager_password)
    team_resp = await client.post(
        "/api/v1/teams",
        json={"name": "MeetTeam", "code": "MEETT"},
        headers=manager_headers,
    )
    assert team_resp.status_code == 201
    meeting_data = {
        "title": "Test Meeting",
        "datetime": "2030-01-01T10:00:00",
        "participants": [],
        "description": "desc",
    }
    resp = await client.post(
        "/api/v1/meetings", json=meeting_data, headers=manager_headers
    )
    assert resp.status_code in (201, 200)
    meeting_id = resp.json().get("id")
    assert meeting_id


@pytest.mark.asyncio
async def test_get_meeting(client, create_user, get_token):
    manager_email = "manager_getmeeting@example.com"
    manager_password = "12345678"
    await create_user(client, manager_email, manager_password)
    manager_headers = await get_token(client, manager_email, manager_password)
    await client.post(
        "/api/v1/teams",
        json={"name": "GetMeetTeam", "code": "GETMEET"},
        headers=manager_headers,
    )
    meeting_data = {
        "title": "Get Meeting",
        "datetime": "2030-01-02T10:00:00",
        "participants": [],
        "description": "desc",
    }
    create_resp = await client.post(
        "/api/v1/meetings", json=meeting_data, headers=manager_headers
    )
    meeting_id = create_resp.json()["id"]
    resp = await client.get(f"/api/v1/meetings/{meeting_id}", headers=manager_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == meeting_id
    assert data["title"] == "Get Meeting"


@pytest.mark.asyncio
async def test_manager_only_can_create_meeting(client, create_user, get_token):
    user_email = "user_meeting@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    user_headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams",
        json={"name": "UserMeetTeam", "code": "USERMEET"},
        headers=user_headers,
    )
    meeting_data = {
        "title": "User Meeting",
        "datetime": "2030-01-03T10:00:00",
        "participants": [],
        "description": "desc",
    }
    resp = await client.post(
        "/api/v1/meetings", json=meeting_data, headers=user_headers
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_meeting(client, create_user, get_token):
    manager_email = "manager_updmeeting@example.com"
    manager_password = "12345678"
    await create_user(client, manager_email, manager_password)
    manager_headers = await get_token(client, manager_email, manager_password)
    await client.post(
        "/api/v1/teams",
        json={"name": "UpdMeetTeam", "code": "UPDMEET"},
        headers=manager_headers,
    )
    meeting_data = {
        "title": "Upd Meeting",
        "datetime": "2030-01-04T10:00:00",
        "participants": [],
        "description": "desc",
    }
    create_resp = await client.post(
        "/api/v1/meetings", json=meeting_data, headers=manager_headers
    )
    meeting_id = create_resp.json()["id"]
    upd_data = {
        "title": "Updated Meeting",
        "participants": [],
        "datetime": "2030-01-04T12:00:00",
    }
    upd_resp = await client.patch(
        f"/api/v1/meetings/{meeting_id}", json=upd_data, headers=manager_headers
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["title"] == "Updated Meeting"


@pytest.mark.asyncio
async def test_cancel_meeting(client, create_user, get_token):
    manager_email = "manager_cancelmeeting@example.com"
    manager_password = "12345678"
    await create_user(client, manager_email, manager_password)
    manager_headers = await get_token(client, manager_email, manager_password)
    await client.post(
        "/api/v1/teams",
        json={"name": "CancelMeetTeam", "code": "CANCELMEET"},
        headers=manager_headers,
    )
    meeting_data = {
        "title": "Cancel Meeting",
        "datetime": "2030-01-05T10:00:00",
        "participants": [],
        "description": "desc",
    }
    create_resp = await client.post(
        "/api/v1/meetings", json=meeting_data, headers=manager_headers
    )
    meeting_id = create_resp.json()["id"]
    cancel_resp = await client.delete(
        f"/api/v1/meetings/{meeting_id}", headers=manager_headers
    )
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["id"] == meeting_id
