import manage
import json

def test_create_user_good():
    user = manage.create_user(
        "TEST USER",
        "test@example.com",
        "asdfasdfasdf",
        "",
    )
    assert user.get('success') == 'New Account Created'

def test_get_user_success():
    user = manage.User.from_credentials(
        "test@example.com",
        "asdfasdfasdf"
    )
    assert user.email == "test@example.com"

def test_get_user_fail_wrong_pwd():
    user = manage.User.from_credentials(
        "test@example.com",
        "asdfasdfasdfxxx"
    )
    assert user == None

def test_get_user_fail_not_found():
    user = manage.User.from_credentials(
        "test@example.net",
        "asdfasdfasdf"
    )
    assert user == None

def test_delete_user():
    removed = manage.delete_user(
        "test@example.com",
        "TEST USER",
    )
    assert removed == "User Deleted"
