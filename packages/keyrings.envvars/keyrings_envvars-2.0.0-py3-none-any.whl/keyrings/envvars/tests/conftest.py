"""Shared fixtures."""

import pytest


@pytest.fixture
def _mock_keyring_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mock environment variables for keyring service, username and password.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Pytest monkeypatch.
    """
    monkeypatch.setenv('KEYRING_SERVICE_NAME_0', 'https://index.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_0', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_0', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_1', 'https://index1.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_1', 'testusername1')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_1', 'testpassword1')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_2', 'https://index2.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_2', 'testusername2')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_3', 'https://index3.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_4', '')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_5', 'https://index5.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_5', '')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_5', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_6', 'https://index6.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_6', '')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_7', 'https://index-duplicate.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_7', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_7', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_8', 'https://index-duplicate.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_8', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_8', 'testpassword2')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_9', 'https://index-multiple.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_9', 'testusername1')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_9', 'testpassword1')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_10', 'https://index-multiple.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_10', 'testusername2')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_10', 'testpassword2')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_11', 'https://index-empty-user.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_11', '')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_11', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_12', 'https://index-empty-pass.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_12', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_12', '')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_13', 'https://index-unset-user.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_13', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_14', 'https://index-unset-pass.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_14', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_15', 'https://index-empty-user-pass.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_15', '')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_15', '')
