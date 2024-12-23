#this is  tests/test_posts.py
import pytest
from app import schemas, models


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "First Post",
            "content": "First Content",
            "user_id": test_user["id"]
        },
        {
            "title": "Second Post",
            "content": "Second Content",
            "user_id": test_user["id"]
        },
        {
            "title": "Third Post",
            "content": "Third Content",
            "user_id": test_user2["id"]
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()


# Test Create Post
def test_create_post(authorized_client):
    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "published": True
    }
    response = authorized_client.post("/posts/", json=post_data)

    assert response.status_code == 201
    created_post = schemas.Post(**response.json())
    assert created_post.title == post_data["title"]
    assert created_post.content == post_data["content"]


def test_unauthorized_create_post(client):
    response = client.post("/posts/", json={"title": "Test", "content": "Test"})
    assert response.status_code == 401


# Test Get Posts
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == len(test_posts)

def test_get_posts_with_search(authorized_client, test_posts):
    response = authorized_client.get("/posts/?search=First")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["title"] == "First Post"


# Test Get Post by ID
def test_get_post_by_id(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert post.id == test_posts[0].id


def test_get_post_not_found(authorized_client):
    response = authorized_client.get("/posts/99999")
    assert response.status_code == 404


# Test Update Post
def test_update_post(authorized_client, test_posts):
    updated_data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": True
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=updated_data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == updated_data["title"]


def test_update_other_user_post(authorized_client, test_posts):
    updated_data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": True
    }
    response = authorized_client.put(f"/posts/{test_posts[2].id}", json=updated_data)
    assert response.status_code == 403


# Test Delete Post
def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_non_exist(authorized_client):
    response = authorized_client.delete("/posts/99999")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert response.status_code == 403


def test_authentication(authorized_client):
    response = authorized_client.get("/users/me")
    print(f"/users/me response: {response.status_code}, {response.json()}")  # Debugging
    assert response.status_code == 200
