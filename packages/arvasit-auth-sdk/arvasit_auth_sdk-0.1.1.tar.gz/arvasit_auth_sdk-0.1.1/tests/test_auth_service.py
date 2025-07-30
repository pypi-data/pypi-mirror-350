import pytest
from auth_sdk import AuthService, AuthServiceConfig


def test_auth_service_initialization():
    config = AuthServiceConfig(
        url="https://api.arvasit.com",
        public_key="test_public_key",
        secret_key="test_secret_key",
    )
    auth_service = AuthService(config)

    assert auth_service.config == config
    assert auth_service.base_url == config.url
    assert auth_service.session.headers["X-Public-Key"] == config.public_key
    assert auth_service.session.headers["X-Secret-Key"] == config.secret_key
