import pytest
import unittest
from unittest.mock import patch, Mock
import urllib3
import uuid

from pynpdc.auth_client import (
    AuthClient,
)
from pynpdc.exception import APIException
from pynpdc.models import (
    AccessLevel,
    Account,
    AuthContainer,
)
from .helpers import create_invalid_test_auth, get_test_config

"""
Prerequisites for this test suite:

- a user foo@example.org with password 1234123412341234 has to exist.
- an admin user admin@example.org with password 1234123412341234 has to exist.

When testing a nullable object for being not null, a special pattern is used to
make mypy pass when object properties are accessed.

bad:

self.assertIsInstance(dataset, Dataset)

good:

self.assertIsInstance(dataset, Dataset)
if type(dataset) is not Dataset:  # make mypy happy
    raise Exception()

"""


class FixtureProperties:
    entrypoint: str
    user: str
    password: str
    admin_user: str
    admin_password: str
    client: AuthClient


class FixtureType:
    cls: FixtureProperties


@pytest.fixture(scope="class")
def run_fixtures(request: FixtureType) -> None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    cfg = get_test_config()

    request.cls.entrypoint = cfg.komainu.entrypoint
    request.cls.user = cfg.komainu.test_user
    request.cls.password = cfg.komainu.test_password
    request.cls.admin_user = cfg.komainu.test_admin_user
    request.cls.admin_password = cfg.komainu.test_admin_password

    request.cls.client = AuthClient(request.cls.entrypoint, verify_ssl=False)


@pytest.mark.usefixtures("run_fixtures")
class TestAuth(unittest.TestCase, FixtureProperties):

    LINK_PREFIX: str = "https://example.org/"

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_login_succeeds(self) -> None:
        account = self.client.login(self.user, self.password)

        self.assertIsInstance(account, Account)
        self.assertEqual(account.email, self.user)
        self.assertIsInstance(account.token, str)
        self.assertNotEqual(account.token, "")
        self.assertIsInstance(account.id, uuid.UUID)
        self.assertNotEqual(account.id, "")
        self.assertIsInstance(account.access_level, AccessLevel)

    def test_login_fails(self) -> None:
        with pytest.raises(APIException) as e_info:
            self.client.login("not-a-user@example.org", "random-password")

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_logout(self) -> None:
        account = self.client.login(self.user, self.password)
        self.client.logout(account)

        with pytest.raises(APIException):
            self.client.logout(account)

    def test_logout_with_bad_token_fails(self) -> None:
        auth = create_invalid_test_auth()

        with pytest.raises(APIException) as e_info:
            self.client.logout(auth)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_get_account(self) -> None:
        login_account = self.client.login(self.user, self.password)
        account_id = login_account.id

        account = self.client.get_account(account_id)
        self.assertIsInstance(account, Account)
        if type(account) is not Account:  # make mypy happy
            raise Exception()

        self.assertEqual(account.id, account_id)
        self.assertEqual(account.email, self.user)
        self.assertIsInstance(account.access_level, AccessLevel)

    def test_getting_non_existent_account_fails(self) -> None:
        account_id = uuid.uuid4()
        account = self.client.get_account(account_id)
        self.assertIsNone(account)

    def test_authorize(self) -> None:
        login_account = self.client.login(self.user, self.password)

        auth = self.client.authorize(login_account)

        self.assertIsInstance(auth, Account)
        self.assertEqual(auth.id, login_account.id)
        self.assertEqual(auth.email, self.user)
        self.assertIsInstance(auth.access_level, AccessLevel)

    def test_authorizing_with_bad_token_fails(self) -> None:
        auth = create_invalid_test_auth()

        with pytest.raises(APIException) as e_info:
            self.client.authorize(auth)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_keepalive(self) -> None:
        login_account = self.client.login(self.user, self.password)

        token = self.client.keepalive(login_account)

        self.assertIsInstance(token, str)
        self.assertNotEqual(token, login_account.token)

    def test_calling_keepalive_with_bad_token_fails(self) -> None:
        auth = create_invalid_test_auth()

        with pytest.raises(APIException) as e_info:
            self.client.keepalive(auth)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_changing_password_fails_with_invalid_new_current_password(self) -> None:
        # We do not want to mess with existing accounts, so therefore we only
        # test an error case, that will not change the password.

        auth = self.client.login(self.user, self.password)

        with pytest.raises(APIException) as e_info:
            self.client.change_password(auth, self.password, "too-short")

        e = e_info.value
        self.assertEqual(e.status_code, 422)
        issue_field = e.response.json()["details"]["issues"][0]["field"]
        self.assertEqual(issue_field, "newPassword")

    def test_account_administration(self) -> None:
        """
        This function tests both create_account and update_account.

        Normally we keep the tests separated, but since it is not possible to
        delete accounts through the API we want to create accounts as little as
        possible in the unit tests.
        """

        auth = self.client.login(self.admin_user, self.admin_password)
        new_account_email = f"test-{uuid.uuid4()}@example.org"

        account = self.client.create_account(auth, new_account_email, self.LINK_PREFIX)

        self.assertEqual(account.email, new_account_email)
        self.assertEqual(account.access_level, AccessLevel.EXTERNAL)
        self.assertFalse(account.directory_user)

        # load the account

        loaded_account = self.client.get_account(account.id)

        self.assertIsInstance(loaded_account, Account)

        # update the account

        updated_account = self.client.update_account(auth, account.id, active=True)

        self.assertEqual(updated_account.email, new_account_email)
        self.assertEqual(updated_account.access_level, AccessLevel.EXTERNAL)

    def test_creating_an_account_without_admin_level_fails(self) -> None:
        auth = self.client.login(self.user, self.password)
        new_account_email = f"test-{uuid.uuid4()}@example.org"

        with pytest.raises(APIException) as e_info:
            self.client.create_account(auth, new_account_email, self.LINK_PREFIX)

        e = e_info.value
        self.assertEqual(e.status_code, 403)

    def test_updating_an_account_without_admin_level_fails(self) -> None:
        auth = self.client.login(self.user, self.password)
        account_id = auth.id

        with pytest.raises(APIException) as e_info:
            self.client.update_account(auth, account_id, active=False)

        e = e_info.value
        self.assertEqual(e.status_code, 403)


@pytest.mark.usefixtures("run_fixtures")
class TestAuthClientWithAPIExceptions(unittest.TestCase, FixtureProperties):

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        resp = Mock()
        resp.status_code = 500

        patcher = patch("requests.api.request", return_value=resp)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_get_account_catching_failure(self) -> None:

        with pytest.raises(APIException) as e_info:
            account_id = uuid.uuid4()
            self.client.get_account(account_id)

        e = e_info.value
        self.assertEqual(e.status_code, 500)

    def test_update_account_catching_failure(self) -> None:
        auth = AuthContainer("")

        with pytest.raises(APIException) as e_info:
            account_id = uuid.uuid4()
            self.client.update_account(auth, account_id, active=False)

        e = e_info.value
        self.assertEqual(e.status_code, 500)
