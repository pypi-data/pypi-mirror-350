import pytest
from shared_architecture.utils.keycloak_helper import validate_token, get_user_roles


@pytest.fixture
def valid_token():
    # This is a mocked token for testing purposes.
    # Replace with a properly structured JWT if using real validation.
    return {
        "preferred_username": "test_user",
        "realm_access": {"roles": ["admin", "user"]}
    }


def test_validate_token_accepts_valid_token(valid_token):
    result = validate_token(valid_token)
    assert result["preferred_username"] == "test_user"


def test_get_user_roles_returns_roles(valid_token):
    roles = get_user_roles(valid_token)
    assert "admin" in roles
    assert "user" in roles
