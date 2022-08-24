from decouple import config
import pytest
import starlette.status
from jose import jwt
from app import schemas
from app.tests.conftest import random_email,\
    get_random_string, get_test_user_token, client


@pytest.mark.order(1)
def test_create_user(request):
    email = random_email(7)
    password = get_random_string(10)
    request.config.cache.set("email", email)
    request.config.cache.set("password", password)
    payload = {
        "email": f"{email}",
        "password": f"{password}"
    }
    res = client.post("/users/", json=payload)
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == starlette.status.HTTP_201_CREATED
    assert new_user.email == payload['email']
    request.config.cache.set("user_id", new_user.id)


@pytest.mark.order(2)
def test_login_user(request):
    user_id = request.config.cache.get("user_id", "default")
    username = request.config.cache.get("email", 'default')
    password = request.config.cache.get("password", 'default')
    res = client.post(
        "/login",
        data={
            "username": f"{username}",
            "password": f"{password}"
        })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        config("SECRET_KEY"),
        algorithms=[config("ALGORITHM")])
    res_user_id = payload.get("user_id")
    request.config.cache.set("access_token", login_res.access_token)
    assert res_user_id == user_id
    assert login_res.token_type == "bearer"
    assert res.status_code == starlette.status.HTTP_200_OK


@pytest.mark.order(3)
def test_invalid_login():
    res = client.post(
        "/login",
        data={
            "username": "username@gmail.com",
            "password": "pass1234"
        })
    response = res.json()
    print(response)
    assert res.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response['detail'] == "Invalid credentials"


@pytest.mark.order(4)
def test_get_user(request):
    user_id = request.config.cache.get("user_id", "default")
    access_token = get_test_user_token()

    res = client.get(
        f"/users/{user_id}",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    user = schemas.UserOut(**res.json())
    assert user.id == user_id
    assert res.status_code == starlette.status.HTTP_200_OK
