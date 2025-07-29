from authorizenet import apicontractsv1

from terminusgps.authorizenet.auth import get_merchant_auth, get_validation_mode
from terminusgps.authorizenet.controllers import AuthorizenetControllerExecutor


class AuthorizenetBase(AuthorizenetControllerExecutor):
    """Base class for Authorizenet objects."""

    def __init__(self, id: int | str | None = None, *args, **kwargs) -> None:
        """
        Sets :py:attr:`id` if provided.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.id = id

    def __str__(self) -> str:
        """Returns the object in format: '#<ID>' if :py:attr:`id` is set."""
        return f"#{self.id}" if self.id else ""

    @property
    def id(self) -> str | None:
        """
        An Authorizenet generated id.

        :type: :py:obj:`str` | :py:obj:`None`

        """
        return self._id

    @id.setter
    def id(self, other: int | str | None) -> None:
        """
        Sets :py:attr:`id` to ``other``.

        :raises ValueError: If ``other`` was provided as a string containing non-digit characters.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if isinstance(other, str) and not other.isdigit():
            raise ValueError(f"'id' can only contain digit characters, got '{other}'.")
        self._id = str(other) if other is not None else None

    @property
    def merchantAuthentication(self) -> apicontractsv1.merchantAuthenticationType:
        """
        Current merchant authentication object to authenticate Authorizenet API calls.

        :returns: A merchant authentication object.
        :rtype: :py:obj:`~authorizenet.apicontractsv1.merchantAuthenticationType`

        """
        return get_merchant_auth()

    @property
    def validationMode(self) -> str:
        """
        Current Authorizenet API validation mode.

        :returns: An Authorizenet API validation mode string.
        :rtype: :py:obj:`str`

        """
        return get_validation_mode()
