import os
import unittest

from django.conf import settings

from terminusgps.wialon.session import WialonSession

TEST_WIALON_TOKEN = os.getenv("WIALON_TOKEN") or settings.WIALON_TOKEN


class WialonSessionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.token = TEST_WIALON_TOKEN
        self.session = WialonSession()

    def tearDown(self) -> None:
        if self.session.active:
            self.session.logout()

    def test_session_init(self) -> None:
        self.assertIsNone(self.session.id)
        self.assertIsNone(self.session.username)
        self.assertIsNone(self.session.uid)

    def test_session_login(self) -> None:
        sid: str = self.session.login(self.token)
        self.assertEqual(self.session.id, sid)

    def test_session_logout(self) -> None:
        self.session.login(self.token)
        self.session.logout()
        self.assertIsNone(self.session.id, None)

    def test_session_bad_call(self) -> None:
        self.session.login(self.token)
        response = self.session.wialon_api.core_bad_call({})
        self.assertIsNone(response)

    def test_session_valid_call_count(self) -> None:
        self.session.login(self.token)  # Login/logout does not count
        self.session.wialon_api.avl_evts()
        self.assertEqual(self.session.wialon_api.total_calls, 1)
