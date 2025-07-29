import dataclasses
import datetime
import typing

import wialon.api
from django.conf import settings


@dataclasses.dataclass
class WialonAPICall:
    action: str
    timestamp: datetime.datetime
    args: tuple
    kwargs: dict
    result: typing.Any = None
    error: Exception | None = None


class Wialon(wialon.api.Wialon):
    def __init__(self, token: str, timeout: int = 300, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = token
        self.call_history: list[WialonAPICall] = []
        self.last_call_datetime = None
        self.timeout = timeout

    @property
    def total_calls(self) -> int:
        return len(self.call_history)

    def token_login(self, *args, **kwargs) -> typing.Any:
        kwargs["appName"] = "python-terminusgps"
        return self.call("token_login", *args, **kwargs)

    def call(self, action_name: str, *argc, **kwargs) -> typing.Any:
        now = datetime.datetime.now()

        try:
            result = super().call(action_name, *argc, **kwargs)
            call_record = WialonAPICall(
                action=action_name,
                timestamp=now,
                args=argc,
                kwargs=kwargs,
                result=result,
            )
            return result
        except wialon.api.WialonError as e:
            call_record = WialonAPICall(
                action=action_name, timestamp=now, args=argc, kwargs=kwargs, error=e
            )
            return None
        finally:
            self.last_call_datetime = now
            self.call_history.append(call_record)


class WialonSession:
    def __init__(
        self,
        token: str | None = None,
        sid: str | None = None,
        scheme: str = "https",
        host: str = "hst-api.wialon.com",
        port: int = 443,
        timeout: int = 300,
    ) -> None:
        """
        Starts or continues a Wialon API session.

        :param token: An optional Wialon API token. Default is :confval:`WIALON_TOKEN`.
        :type token: :py:obj:`str` | :py:obj:`None`
        :param sid: An optional Wialon API session id. If provided, the session is continued.
        :type sid: :py:obj:`str` | :py:obj:`None`
        :param scheme: HTTP request scheme to use. Default is ``"https"``.
        :type scheme: :py:obj:`str`
        :param host: Wialon API host url. Default is ``"hst-api.wialon.com"``.
        :type host: :py:obj:`str`
        :param port: Wialon API host port. Default is ``443``.
        :type port: :py:obj:`int`
        :param log_level: Level of emitted logs. Default is ``10``.
        :type log_level: :py:obj:`int`
        :param timeout: How long in seconds a session can be active for. Default is ``500`` (5 min).
        :type timeout: :py:obj:`int`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self._token = token or settings.WIALON_TOKEN
        self._username = None
        self._gis_sid = None
        self._hw_gp_ip = None
        self._wsdk_version = None
        self._uid = None
        self._wialon_api = Wialon(
            scheme=scheme,
            host=host,
            port=port,
            sid=sid,
            timeout=timeout,
            token=self.token,
        )

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__}(sid={self.id})"

    def __enter__(self) -> "WialonSession":
        """
        Logs into the Wialon API using :py:meth:`login`.

        :raises AssertionError: If the Wialon API token was not set.
        :returns: A valid Wialon API session.
        :rtype: :py:obj:`~terminusgps.wialon.session.WialonSession`

        """
        assert self.token, "Wialon API token was not set"
        self.login(self.token)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """
        Logs out of the session by calling :py:meth:`logout`.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.logout()

    @property
    def wialon_api(self) -> Wialon:
        return self._wialon_api

    @property
    def gis_geocode(self) -> str | None:
        """
        Gis geocode URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_geocode

    @property
    def gis_render(self) -> str | None:
        """
        Gis rendering URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_render

    @property
    def gis_routing(self) -> str | None:
        """
        Gis routing URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_routing

    @property
    def gis_search(self) -> str | None:
        """
        Gis search URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_search

    @property
    def gis_sid(self) -> str | None:
        """
        Gis session id.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_sid

    @property
    def host(self) -> str | None:
        """
        IP of the client hosting the Wialon session.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._host

    @property
    def hw_gw_ip(self) -> str | None:
        """
        Hardware gateway IP.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._hw_gw_ip

    @property
    def hw_gw_dns(self) -> str | None:
        """
        Hardware gateway domain name, should evaluate to :py:attr:`hw_gw_ip` if present.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._hw_gw_dns

    @property
    def wsdk_version(self) -> str | None:
        """
        The Wialon Source Developer Kit (WSDK) version number of the session.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._wsdk_version

    @property
    def uid(self) -> str | None:
        """
        A Wialon user ID this session is operating as.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`
        """
        return self._uid

    @property
    def username(self) -> str | None:
        """
        A Wialon username the session is operating as.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._username

    @property
    def id(self) -> str | None:
        """
        Shortcut property for :py:attr:`WialonSession.wialon_api.sid`.

        Returns :py:obj:`None` if the session wasn't logged in.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self.wialon_api.sid

    @property
    def token(self) -> str:
        """
        A Wialon API token set during :py:meth:`WialonSession.__init__`.

        Default token value is :confval:`WIALON_TOKEN`.

        :type: :py:obj:`str`
        :value: :confval:`WIALON_TOKEN`

        """
        return str(self._token)

    def login(self, token: str, flags: int = sum([0x1, 0x2, 0x20])) -> str:
        """
        Logs into the Wialon API and starts a new session.

        :param token: An active Wialon API token.
        :type token: :py:obj:`str`
        :param flags: A login response flag integer.
        :type flags: :py:obj:`int`
        :raises WialonError: If the login fails.
        :raises AssertionError: If the login token was not set.
        :returns: The new session id.
        :rtype: :py:obj:`str`

        """
        try:
            response = self.wialon_api.token_login(**{"token": token, "fl": flags})
            self._set_login_response(response)
            return response.get("eid")
        except (wialon.api.WialonError, ValueError):
            raise

    def logout(self) -> None:
        """
        Logs out of the Wialon API session.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        response: dict = self.wialon_api.core_logout({})
        self.wialon_api.sid = None

        if response.get("error") != 0:
            print(f"Failed to logout of session: '{response.get('message')}'")

    def _set_login_response(self, login_response: dict | None) -> None:
        """
        Sets the Wialon API session's attributes based on a login response.

        :param login_response: A response returned from :py:meth:`login` or :py:meth:`duplicate`.
        :type login_response: :py:obj:`dict`
        :raises ValueError: If ``login_response`` wasn't provided.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if login_response is None:
            raise ValueError("Failed to login to Wialon.")

        self.wialon_api.sid = login_response.get("eid")
        self._gis_geocode = login_response.get("gis_geocode")
        self._gis_render = login_response.get("gis_render")
        self._gis_routing = login_response.get("gis_routing")
        self._gis_search = login_response.get("gis_search")
        self._gis_sid = login_response.get("gis_sid")
        self._host = login_response.get("host")
        self._hw_gw_dns = login_response.get("hw_gw_dns")
        self._hw_gw_ip = login_response.get("hw_gw_ip")
        self._uid = login_response.get("user", {}).get("id")
        self._nm = login_response.get("user", {}).get("nm")
        self._username = login_response.get("au")
        self._video_service_url = login_response.get("video_service_url")
        self._wsdk_version = login_response.get("wsdk_version")


class WialonSessionManager:
    """Provides an interface for generating automatically activated Wialon sessions."""

    def __init__(
        self,
        token: str | None = None,
        lifetime: int = 500,
        session: WialonSession | None = None,
        session_id: str | None = None,
    ) -> None:
        """
        Sets :py:attr:`token` and :py:attr:`lifetime`.

        :param token: A Wialon API token. Default is :confval:`WIALON_TOKEN`.
        :type token: :py:obj:`str` | :py:obj:`None`
        :param lifetime: How long in seconds a Wialon session can be valid for. Default is ``500``.
        :type lifetime: :py:obj:`int`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.token = token
        self.lifetime = lifetime

        target_sid = session.id if session and session.id else session_id
        self.session = WialonSession(sid=target_sid)
        if not target_sid or not self.validate_session():
            self.session.login(token=self.token)

    def check_active(self) -> bool:
        """
        Checks if :py:attr:`session` is active.

        :returns: Whether or not :py:attr:`session` is an active Wialon session.
        :rtype: :py:obj:`bool`

        """
        if not self.session.id:
            return False
        if not self.session.wialon_api.last_call_datetime:
            return self.validate_session()

        now = datetime.datetime.now()
        last_call = self.session.wialon_api.last_call_datetime
        session_expiry = last_call + datetime.timedelta(seconds=self.lifetime)

        if now > session_expiry:
            return False
        return self.validate_session()

    def get_session(self, sid: str | None = None) -> WialonSession:
        """
        Returns a valid Wialon API session.

        If ``sid`` is provided, tries to continue the session and return it.

        :param sid: A Wialon API session id.
        :type sid: :py:obj:`str` | :py:obj:`None`
        :returns: A valid Wialon API session.
        :rtype: :py:obj:`~terminusgps.wialon.session.WialonSession`

        """
        if sid is not None:
            self.session = WialonSession(sid=sid)
            if not self.validate_session():
                self.session = WialonSession()
                self.session.login(token=self.token)
                return self.session
        if not self.check_active():
            self.session = WialonSession()
            self.session.login(token=self.token)
        return self.session

    def validate_session(self) -> bool:
        try:
            result = self.session.wialon_api.core_duplicate()
            return result is not None
        except wialon.api.WialonError:
            return False

    @property
    def sid(self) -> str | None:
        """
        Current Wialon session id.

        :type: :py:obj:`str` | :py:obj:`None`

        """
        return self.session.wialon_api.sid if self.session else None

    @sid.setter
    def sid(self, other: str) -> None:
        """
        Sets :py:attr:`sid` to ``other``.

        :param other: A Wialon session id.
        :type other: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if self.session:
            self.session.wialon_api.sid = other
        else:
            self.session = WialonSession(sid=other)

    @property
    def token(self) -> str:
        """
        A Wialon API token.

        :type: :py:obj:`str`

        """
        return str(self._token)

    @token.setter
    def token(self, other: str | None) -> None:
        """
        Sets :py:attr:`token` to ``other`` if provided.

        If ``other`` isn't provided, instead sets :py:attr:`token` to :confval:`WIALON_TOKEN`.

        :param other: A Wialon API token.
        :type other: :py:obj:`str` | :py:obj:`None`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._token = other if other is not None else settings.WIALON_TOKEN

    @property
    def session(self) -> WialonSession:
        """
        A Wialon API session.

        :type: :py:obj:`~terminusgps.wialon.session.WialonSession`

        """
        return self._session

    @session.setter
    def session(self, other: WialonSession) -> None:
        """
        Sets :py:attr:`session` to ``other``.

        :param other: A Wialon session.
        :type other: :py:obj:`~terminusgps.wialon.session.WialonSession`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._session = other

    @property
    def lifetime(self) -> int:
        """
        How long in seconds a Wialon session can live for.

        :type: :py:obj:`int`
        :value: :py:obj:`500`

        """
        return self._lifetime

    @lifetime.setter
    def lifetime(self, other: int) -> None:
        """
        Sets :py:attr:`lifetime` to ``other``.

        :param other: An integer.
        :type other: :py:obj:`int`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._lifetime = other
