import pytest


@pytest.mark.asyncio
async def test_get_month_view(client, create_user, get_token):
    user_email = "calendar_user@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams", json={"name": "CalTeam", "code": "CALT"}, headers=headers
    )
    resp = await client.get(
        "/api/v1/calendars/month?year=2030&month=1", headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "days" in data or "month" in data


@pytest.mark.asyncio
async def test_get_day_view(client, create_user, get_token):
    user_email = "calendar_user2@example.com"
    user_password = "12345678"
    await create_user(client, user_email, user_password)
    headers = await get_token(client, user_email, user_password)
    await client.post(
        "/api/v1/teams", json={"name": "CalTeam2", "code": "CALT2"}, headers=headers
    )
    resp = await client.get(
        f"/api/v1/calendars/day?day_date=2030-01-01", headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "tasks" in data or "date" in data
