"""Tests for keyrings.envvars."""

from __future__ import annotations

import os

import pytest
from keyring.errors import PasswordDeleteError, PasswordSetError

from ..credential import EnvvarCredential
from ..keyring import EnvvarsKeyring


class TestKeyringBackend:
    """Test Keyring Backend."""

    def test_get_trailing_number(self) -> None:
        """Test getting trailing number from an environment variable."""
        assert EnvvarsKeyring._get_trailing_number('KEYRING_SERVICE_NAME_A') is None
        assert EnvvarsKeyring._get_trailing_number('KEYRING_SERVICE_NAME_0') == '0'
        assert EnvvarsKeyring._get_trailing_number('OTHER_KEYRING_SERVICE_NAME_0') is None
        assert EnvvarsKeyring._get_trailing_number('KEYRING_SERVICE_NAME_١') is None, (  # noqa: RUF001 # ARABIC-INDIC DIGIT ONE is expected here
            'Arabic Unicode digits are not allowed'
        )

    @pytest.mark.usefixtures('_mock_keyring_environment')
    @pytest.mark.parametrize(
        ('service', 'expected'),
        [
            (None, None),
            ('', None),
            (
                'https://index.example.com',
                {
                    'testusername': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_0',
                        'KEYRING_SERVICE_PASSWORD_0',
                    ),
                },
            ),
            (
                'https://index1.example.com',
                {
                    'testusername1': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_1',
                        'KEYRING_SERVICE_PASSWORD_1',
                    ),
                },
            ),
            (
                'https://index2.example.com',
                {
                    'testusername2': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_2',
                        'KEYRING_SERVICE_PASSWORD_2',
                    ),
                },
            ),
            (
                'https://index3.example.com',
                {
                    '': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_3',
                        'KEYRING_SERVICE_PASSWORD_3',
                    ),
                },
            ),
            pytest.param(
                'https://index.example.com',
                {
                    'testusername': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_1',
                        'KEYRING_SERVICE_PASSWORD_1',
                    ),
                },
                marks=pytest.mark.xfail,
            ),
            pytest.param(
                'https://index-duplicate.example.com',
                {
                    'testusername': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_7',
                        'KEYRING_SERVICE_PASSWORD_7',
                    ),
                },
                marks=pytest.mark.xfail,
            ),
            (
                'https://index-duplicate.example.com',
                {
                    'testusername': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_8',
                        'KEYRING_SERVICE_PASSWORD_8',
                    ),
                },
            ),
            (
                'https://index-multiple.example.com',
                {
                    'testusername1': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_9',
                        'KEYRING_SERVICE_PASSWORD_9',
                    ),
                    'testusername2': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_10',
                        'KEYRING_SERVICE_PASSWORD_10',
                    ),
                },
            ),
            (
                'https://index-empty-user.example.com',
                {
                    '': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_11',
                        'KEYRING_SERVICE_PASSWORD_11',
                    ),
                },
            ),
            (
                'https://index-empty-pass.example.com',
                {
                    'testusername': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_12',
                        'KEYRING_SERVICE_PASSWORD_12',
                    ),
                },
            ),
            (
                'https://index-unset-user.example.com',
                {
                    '': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_13',
                        'KEYRING_SERVICE_PASSWORD_13',
                    ),
                },
            ),
            (
                'https://index-unset-pass.example.com',
                {
                    'testusername': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_14',
                        'KEYRING_SERVICE_PASSWORD_14',
                    ),
                },
            ),
            (
                'https://index-empty-user-pass.example.com',
                {
                    '': EnvvarCredential(
                        'KEYRING_SERVICE_USERNAME_15',
                        'KEYRING_SERVICE_PASSWORD_15',
                    ),
                },
            ),
        ],
    )
    def test_get_mapping(self, service: str, expected: EnvvarCredential) -> None:
        """
        Test getting None from an empty service and username.

        Parameters
        ----------
        service : str
            Service.
        expected : EnvvarCredential
            Expected return value from _get_mapping().
        """
        mapping = EnvvarsKeyring._get_mapping()
        # Number of valid services defined in conftest.py
        # A valid service is any with a defined service name
        valid_service_definitions_count = 13

        result = mapping.get(service)

        assert len(mapping) == valid_service_definitions_count
        assert result == expected

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_keyring_backend_get_password(self) -> None:
        """Test getting a password from a defined service and username."""
        k = EnvvarsKeyring()

        service = 'https://index.example.com'
        user = 'testusername'

        retrieved = k.get_password(service, user)
        assert retrieved == os.getenv('KEYRING_SERVICE_PASSWORD_0')

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_keyring_backend_get_invalid_service(self) -> None:
        """Test getting a password from an invalid service and username."""
        k = EnvvarsKeyring()

        service = 'https://index-unknown.example.com'
        user = 'testusername'

        retrieved = k.get_password(service, user)
        assert retrieved is None

    @pytest.mark.usefixtures('_mock_keyring_environment')
    @pytest.mark.parametrize(
        ('service', 'username', 'expected'),
        [
            (None, None, None),
            ('', None, None),
            (None, '', None),
            ('', '', None),
            ('https://index.example.com', '', None),
            ('https://index-multiple.example.com', None, None),
            ('', 'testusername', None),
            (
                'https://index.example.com',
                'testusername',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_0',
                    'KEYRING_SERVICE_PASSWORD_0',
                ),
            ),
            (
                'https://index.example.com',
                None,
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_0',
                    'KEYRING_SERVICE_PASSWORD_0',
                ),
            ),
            ('https://index.example.com', 'testusername1', None),
            ('https://index1.example.com', 'testusername2', None),
            (
                'https://index2.example.com',
                'testusername2',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_2',
                    'KEYRING_SERVICE_PASSWORD_2',
                ),
            ),
            ('https://index3.example.com', 'testusername3', None),
            pytest.param(
                'https://index.example.com',
                'testusername',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_1',
                    'KEYRING_SERVICE_PASSWORD_1',
                ),
                marks=pytest.mark.xfail,
            ),
            pytest.param(
                'https://index-duplicate.example.com',
                'testusername',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_7',
                    'KEYRING_SERVICE_PASSWORD_7',
                ),
                marks=pytest.mark.xfail,
            ),
            pytest.param(
                'https://index-duplicate.example.com',
                'testusername',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_8',
                    'KEYRING_SERVICE_PASSWORD_8',
                ),
            ),
            (
                'https://index-multiple.example.com',
                'testusername1',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_9',
                    'KEYRING_SERVICE_PASSWORD_9',
                ),
            ),
            (
                'https://index-multiple.example.com',
                'testusername2',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_10',
                    'KEYRING_SERVICE_PASSWORD_10',
                ),
            ),
            (
                'https://index-empty-user.example.com',
                '',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_11',
                    'KEYRING_SERVICE_PASSWORD_11',
                ),
            ),
            (
                'https://index-empty-pass.example.com',
                'testusername',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_12',
                    'KEYRING_SERVICE_PASSWORD_12',
                ),
            ),
            (
                'https://index-unset-user.example.com',
                '',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_13',
                    'KEYRING_SERVICE_PASSWORD_13',
                ),
            ),
            (
                'https://index-unset-pass.example.com',
                'testusername',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_14',
                    'KEYRING_SERVICE_PASSWORD_14',
                ),
            ),
            (
                'https://index-empty-user-pass.example.com',
                '',
                EnvvarCredential(
                    'KEYRING_SERVICE_USERNAME_15',
                    'KEYRING_SERVICE_PASSWORD_15',
                ),
            ),
        ],
    )
    def test_get_credential(self, service: str, username: str, expected: EnvvarCredential) -> None:
        """
        Test getting a credential.

        Parameters
        ----------
        service : str
            Service.
        username : str
            Username.
        expected : EnvvarCredential
            Expected return value from EnvvarsKeyring.get_credential().
        """
        k = EnvvarsKeyring()

        retrieved = k.get_credential(service, username)

        assert retrieved == expected

    def test_keyring_backend_set(self) -> None:
        """Setting a password should raise an error."""
        k = EnvvarsKeyring()

        service = 'https://index.example.com'
        user = 'testusername'
        pw = 'testpassword'
        with pytest.raises(PasswordSetError):
            k.set_password(service, user, pw)

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_keyring_backend_delete(self) -> None:
        """Deleting a password should raise an error."""
        k = EnvvarsKeyring()

        service = 'https://index.example.com'
        user = 'testusername'

        with pytest.raises(PasswordDeleteError):
            k.delete_password(service, user)

    def test_keyring_backend_priority(self) -> None:
        """Test keyring priority."""
        assert EnvvarsKeyring.priority == 1


class TestEnvvarCredential:
    """Test the EnvvarCredential class."""

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_basic(self) -> None:
        """Check that an EnvvarCredential with a set username and password behaves as expected."""
        cred = EnvvarCredential(
            'KEYRING_SERVICE_USERNAME_0',
            'KEYRING_SERVICE_PASSWORD_0',
        )

        assert cred.username == 'testusername'
        assert cred.password == 'testpassword'  # nosec: B105

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_empty_username(self) -> None:
        """Check that an EnvvarCredential with an empty username env var returns an empty string for the username."""
        cred = EnvvarCredential(
            'KEYRING_SERVICE_USERNAME_11',
            'KEYRING_SERVICE_PASSWORD_11',
        )

        assert cred.username == ''  # noqa: PLC1901
        assert cred.password == 'testpassword'  # nosec: B105

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_empty_password(self) -> None:
        """Check that an EnvvarCredential with an empty password env var returns an empty string for the password."""
        cred = EnvvarCredential(
            'KEYRING_SERVICE_USERNAME_12',
            'KEYRING_SERVICE_PASSWORD_12',
        )

        assert cred.username == 'testusername'
        assert cred.password == ''  # noqa: PLC1901  # nosec: B105

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_unset_username(self) -> None:
        """Check that an EnvvarCredential with an unset username env var returns an empty string for the username."""
        cred = EnvvarCredential(
            'KEYRING_SERVICE_USERNAME_13',
            'KEYRING_SERVICE_PASSWORD_13',
        )

        assert cred.username == ''  # noqa: PLC1901
        assert cred.password == 'testpassword'  # nosec: B105

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_unset_password(self) -> None:
        """Check that an EnvvarCredential with an unset password env var returns an empty string for the password."""
        cred = EnvvarCredential(
            'KEYRING_SERVICE_USERNAME_14',
            'KEYRING_SERVICE_PASSWORD_14',
        )

        assert cred.username == 'testusername'
        assert cred.password == ''  # noqa: PLC1901  # nosec: B105

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_empty_username_and_password(self) -> None:
        """
        Check empty username and password.

        Check that an EnvvarCredential with an empty username env var and an empty password env var returns an empty
        string for both the username and the password.
        """
        cred = EnvvarCredential(
            'KEYRING_SERVICE_USERNAME_15',
            'KEYRING_SERVICE_PASSWORD_15',
        )

        assert cred.username == ''  # noqa: PLC1901
        assert cred.password == ''  # noqa: PLC1901  # nosec: B105

    def test_hash_code(self) -> None:
        """Check that EnvvarCredentials referencing the same environment variables have the same hash codes."""
        cred_a = EnvvarCredential('USERNAME_VAR', 'PASSWORD_VAR')
        cred_b = EnvvarCredential('USERNAME_VAR', 'PASSWORD_VAR')

        assert hash(cred_a) == hash(cred_b)
