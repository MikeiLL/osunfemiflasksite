import admin

""" def test_create_user_good():
    user = admin.create_user(
        "TEST USER",
        "test@example.com",
        "asdfasdfasdf",
        "",
    )
    assert user.email == "test@example.com" """

def test_get_user_success():
    user = admin.User.from_credentials(
        "test@example.com",
        "asdfasdfasdf"
    )
    assert user.email == "test@example.com"
