import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/users/", json={"email": "testuser@example.com", "password": "12345678"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user(client):
    create_resp = await client.post(
        "/api/v1/users/", json={"email": "getuser@example.com", "password": "12345678"}
    )
    user_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "getuser@example.com"


@pytest.mark.asyncio
async def test_update_user(client):
    create_resp = await client.post(
        "/api/v1/users/",
        json={"email": "updateuser@example.com", "password": "12345678"},
    )
    user_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/users/{user_id}", json={"email": "updated@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(client):
    create_resp = await client.post(
        "/api/v1/users/",
        json={"email": "deleteuser@example.com", "password": "12345678"},
    )
    user_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404
