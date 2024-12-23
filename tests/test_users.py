# tests/test_users.py
from fastapi import status

from app.schemas import UserOut


def test_register_user_success(client):
    """
    Test that a new user can be successfully registered.
    """
    new_user_data = {
        "email": "newuser@example.com",
        "password": "somepassword"
    }
    res = client.post("/users/", json=new_user_data)
    assert res.status_code == status.HTTP_201_CREATED, f"Expected 201, got {res.status_code}"

    created_user = UserOut(**res.json())
    assert created_user.email == new_user_data["email"]



def test_register_user_duplicate_email(client, test_user):
    """
    Test that trying to register a user with an existing email
    returns HTTP_400_BAD_REQUEST.
    """
    # test_user is a fixture that already creates a user with "test@example.com"
    duplicate_user_data = {
        "email": test_user["email"],  # Same email as the fixture user
        "password": "somepassword"
    }
    res = client.post("/users/", json=duplicate_user_data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST, f"Expected 400, got {res.status_code}"
    assert res.json()["detail"] == "Email already registered"


def test_register_user_invalid_data(client):
    """
    Test that posting invalid data (e.g., missing fields) raises a 422.
    """
    # Missing 'password'
    invalid_data = {
        "email": "invalid@example.com"
    }
    res = client.post("/users/", json=invalid_data)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_me_authorized(authorized_client, test_user):
    """
    Test that an authorized user can retrieve their own data.
    """
    res = authorized_client.get("/users/me")
    assert res.status_code == status.HTTP_200_OK, f"Expected 200, got {res.status_code}"

    user_data = UserOut(**res.json())
    assert user_data.email == test_user["email"]


def test_get_me_unauthorized(client):
    """
    Test that attempting to retrieve current user data without
    an authorization token fails with HTTP_401_UNAUTHORIZED.
    """
    res = client.get("/users/me")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json()["detail"] == "Not authenticated"


def test_get_user_by_id_success(authorized_client, test_user):
    """
    Test that an authorized user can retrieve a user's details by ID.
    Using the fixture's user ID as a valid example.
    """
    user_id = test_user["id"]
    res = authorized_client.get(f"/users/{user_id}")
    assert res.status_code == status.HTTP_200_OK, f"Expected 200, got {res.status_code}"

    user_data = UserOut(**res.json())
    assert user_data.email == test_user["email"]


def test_get_user_by_id_not_found(authorized_client):
    """
    Test that retrieving a user with a non-existing ID returns 404.
    """
    res = authorized_client.get("/users/999999")  # Some ID that doesn't exist
    assert res.status_code == status.HTTP_404_NOT_FOUND, f"Expected 404, got {res.status_code}"
    assert res.json()["detail"] == "User not found"


def test_get_user_by_id_unauthorized(client, test_user):
    """
    Test that a request without a valid token cannot retrieve a user by ID.
    """
    user_id = test_user["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED, f"Expected 401, got {res.status_code}"
    assert res.json()["detail"] == "Not authenticated"
