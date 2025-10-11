import admin

def test_user():
    user = admin.User.from_credentials(
        "mike@mzoo.org",
        "mike771"
    )
    print(user)
    assert user.email == "mike@mzoo.org"
