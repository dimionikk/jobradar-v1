import pytest
from httpx import AsyncClient


async def test_register(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@gmail.com"
    assert "password" not in data


async def test_register_duplicate_email(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 400


async def test_login(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


async def test_logout(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    login = await client.post("/api/v1/auth/login", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    token = login.json()["access_token"]
    response = await client.post("/api/v1/auth/logout", headers={
        "authorization": f"Bearer {token}"
    })
    assert response.status_code == 200


async def test_get_profile(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    login = await client.post("/api/v1/auth/login", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    token = login.json()["access_token"]
    response = await client.get("/api/v1/profile/", headers={
        "authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@gmail.com"


async def test_update_profile(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    login = await client.post("/api/v1/auth/login", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    token = login.json()["access_token"]
    response = await client.patch("/api/v1/profile/", json={
        "city": "Київ",
        "experience": "junior"
    }, headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["city"] == "Київ"
    assert response.json()["experience"] == "junior"


async def test_delete_account(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    login = await client.post("/api/v1/auth/login", json={
        "email": "test@gmail.com",
        "password": "password123"
    })
    token = login.json()["access_token"]
    response = await client.delete("/api/v1/profile/", headers={
        "authorization": f"Bearer {token}"
    })
    assert response.status_code == 204


async def test_get_profile_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/profile/")
    assert response.status_code == 422