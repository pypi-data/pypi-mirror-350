
from auth_user.auth.basic_auth import BasicAuthManager


def test_hashing():
    test_password = "<PASSWORD>"
    hash_pass= BasicAuthManager.hash_password(password=test_password)

    assert BasicAuthManager.verify_password(plain_password=test_password, hashed_password=hash_pass)