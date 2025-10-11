import admin
import json

def test_create_user_good():
    user = admin.create_user(
        "TEST USER",
        "test@example.com",
        "asdfasdfasdf",
        "",
    )
    assert user.get('success') == 'New Account Created'

def test_get_user_success():
    user = admin.User.from_credentials(
        "test@example.com",
        "asdfasdfasdf"
    )
    assert user.email == "test@example.com"

def test_delete_user():
    removed = admin.delete_user(
        "test@example.com",
        "TEST USER",
    )
    assert removed == "User Deleted"
