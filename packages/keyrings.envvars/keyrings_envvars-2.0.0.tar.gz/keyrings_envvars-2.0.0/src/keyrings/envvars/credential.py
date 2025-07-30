"""Credentials used by the keyrings.envvars backend."""

import os
from dataclasses import dataclass

from keyring.credentials import Credential


@dataclass
class EnvvarCredential(Credential):
    """
    Read credentials from the environment.

    This is similar to keyring.credentials.EnvironCredential except that it doesn't throw if a variable is unset or
    empty since a service could legitimately use only a username or only a password (for example, an API token)
    """

    user_env_var: str
    pass_env_var: str

    def __eq__(self, other: object) -> bool:
        """
        Compare this credential to another.

        Parameters
        ----------
        other : object
            Other credential to compare to.

        Returns
        -------
        bool
            True if `other` is equal to this credential. False if not equal.
        """
        return vars(self) == vars(other)

    def __hash__(self) -> int:
        """
        Get hash code for dict lookup.

        Returns
        -------
        int
            Hash of user env_var and pass env_var.
        """
        return hash((self.user_env_var, self.pass_env_var))

    @property
    def username(self) -> str:
        """
        Get the username for this credential from the environment.

        Returns
        -------
        str
            Credential username.
        """
        return os.getenv(self.user_env_var, '')

    @property
    def password(self) -> str:
        """
        Get the password for this credential from the environment.

        Returns
        -------
        str
            Credential password.
        """
        return os.getenv(self.pass_env_var, '')
