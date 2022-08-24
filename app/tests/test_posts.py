import pytest
import starlette.status

from app import schemas
from app.tests.conftest import get_random_string, client


@pytest.mark.order(5)
def test_create_post(request):
    access_token = request.config.cache.get("access_token", "default")
    payload = {
        "title": get_random_string(10),
        "content": get_random_string(20),
        "published": True
    }
    res = client.post(
        "/posts/",
        json=payload,
        headers={'Authorization': f"Bearer {access_token}"}
    )
    new_post = schemas.PostCreate(**res.json())
    response = res.json()
    assert res.status_code == starlette.status.HTTP_201_CREATED
    assert new_post.title == payload["title"]
    request.config.cache.set("post_id", response['id'])


@pytest.mark.order(6)
def test_create_post_unauthorized():
    payload = {
        "title": get_random_string(10),
        "content": get_random_string(20),
        "published": True
    }
    res = client.post(
        "/posts/",
        json=payload
    )
    assert res.status_code == starlette.status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(7)
def test_update_post(request):
    id = request.config.cache.get("post_id", "default")
    access_token = request.config.cache.get("access_token", "default")
    payload = {
        "title": get_random_string(10),
        "content": get_random_string(20),
        "published": False
    }
    res = client.put(
        f"/posts/{id}",
        json=payload,
        headers={'Authorization': f"Bearer {access_token}"}
    )
    updated_post = schemas.PostCreate(**res.json())
    assert res.status_code == starlette.status.HTTP_200_OK
    assert updated_post.title == payload["title"]


@pytest.mark.order(8)
def test_get_all_posts():
    res = client.get("/posts/")
    response = res.json()
    print(response)
    assert res.status_code == starlette.status.HTTP_200_OK


@pytest.mark.order(9)
def test_get_single_post(request):
    post_id = request.config.cache.get("post_id", "default")
    access_token = request.config.cache.get("access_token", "default")
    res = client.get(
        f"/posts/{post_id}",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    response = res.json()
    print(response)
    assert res.status_code == starlette.status.HTTP_200_OK
    assert response['id'] == post_id


@pytest.mark.order(10)
def test_get_single_post_unauthorized(request):
    post_id = request.config.cache.get("post_id", "default")
    res = client.get(
        f"/posts/{post_id}",
    )
    response = res.json()
    print(response)
    assert res.status_code == starlette.status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(11)
def test_get_single_post_not_exist(request):
    access_token = request.config.cache.get("access_token", "default")
    res = client.get(
        f"/posts/{100}",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    response = res.json()
    print(response)
    assert res.status_code == starlette.status.HTTP_404_NOT_FOUND


@pytest.mark.order(12)
def test_delete_post(request):
    post_id = request.config.cache.get("post_id", "default")
    access_token = request.config.cache.get("access_token", "default")
    res = client.delete(
        f"/posts/{post_id}",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert res.status_code == starlette.status.HTTP_204_NO_CONTENT


@pytest.mark.order(13)
def test_delete_post_no_authorization(request):
    post_id = request.config.cache.get("post_id", "default")
    res = client.delete(
        f"/posts/{post_id}"
    )
    assert res.status_code == starlette.status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(14)
def test_delete_post_non_exist(request):
    access_token = request.config.cache.get("access_token", "default")
    res = client.delete(
        f"/posts/{100}",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert res.status_code == starlette.status.HTTP_404_NOT_FOUND
