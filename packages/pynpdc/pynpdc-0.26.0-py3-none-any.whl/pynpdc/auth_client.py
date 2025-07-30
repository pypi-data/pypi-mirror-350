import base64
import requests
from typing import Optional
import uuid

from .exception import APIException
from .models import Account, AccountWithToken, AuthContainer, KeepaliveAPIResponse

AUTH_STAGING_ENTRYPOINT = "https://beta.data.npolar.no/-/auth/"
AUTH_LIFE_ENTRYPOINT = "https://auth.data.npolar.no/"


class AuthClient:
    """
    A client to communicate with the NPDC auth module.

    Attributes:
        entrypoint (str): The entrypoint of the Rest API with a trailing slash
        verify_ssl (bool): Set to false, when the Rest API has a self signed
            certificate
    """

    def __init__(self, entrypoint: str, *, verify_ssl: bool = True) -> None:
        """
        Create a new AuthClient.

        Args:
            entrypoint (str): The entrypoint of the Rest API with a trailing
                slash
            verify_ssl (bool): Set to false, when the Rest API has a self signed
                certificate
        """
        self.entrypoint: str = entrypoint
        self.verify_ssl: bool = verify_ssl

    # !IMPL GET /authenticate/
    def login(self, email: str, password: str) -> AccountWithToken:
        """
        Login a user and retrieve account.

        Args:
            email (str): The user email
            password (str): The user password

        Returns:
            AccountWithToken: The logged in account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        creds = base64.b64encode(bytes(f"{email}:{password}", "utf8"))
        endpoint = f"{self.entrypoint}authenticate/"
        headers = {"Authorization": "Basic " + creds.decode("utf8")}

        response = requests.get(endpoint, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            raise APIException(response)

        return AccountWithToken(response.json(), client=self)

    # !IMPL DELETE /authenticate/
    def logout(self, auth: AuthContainer) -> None:
        """
        Logout a user.

        Args:
            auth (AuthContainer): An object containing the auth token

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        endpoint = f"{self.entrypoint}authenticate/"
        response = requests.delete(
            endpoint, headers=auth.headers, verify=self.verify_ssl
        )
        if response.status_code != 200:
            raise APIException(response)

    # !IMPL GET /authorize/
    def authorize(self, auth: AuthContainer) -> Account:
        """
        Retrieve a logged in account by token

        Args:
            auth (AuthContainer): An object containing the auth token

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """

        endpoint = f"{self.entrypoint}authorize/"
        response = requests.get(endpoint, headers=auth.headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    # !IMPL POST /account/
    def create_account(
        self, auth: AuthContainer, email: str, link_prefix: str
    ) -> Account:
        """
        Create a new external account

        Only admins have access to this method

        Args:
            auth (AuthContainer): the account used to create the new
                account. Has to have accessLevel admin.
            email (str): the email for the account. The email domain must not be
                an internal one (npolar.no in the production system)
            link_prefix (str): the link prefix. Used to build a URL in the
                email.

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 201
        """

        endpoint = f"{self.entrypoint}account/"
        payload = {"email": email, "linkPrefix": link_prefix}
        response = requests.post(
            endpoint, headers=auth.headers, json=payload, verify=self.verify_ssl
        )

        if response.status_code != 201:
            raise APIException(response)

        return Account(response.json())

    # !IMPL GET /account/{id}
    def get_account(self, account_id: uuid.UUID) -> Optional[Account]:
        """
        Retrieve an account by ID

                When the account is not found, None is returned.

        Args:
            account_id (uuid.UUID): the UUID of the account

        Returns:
            Account | None

        Raises:
            APIException: if the HTTP status code of the response is 500
        """

        endpoint = f"{self.entrypoint}account/{account_id}"
        response = requests.get(endpoint, verify=self.verify_ssl)

        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    # !IMPL PUT /account/{id}
    def update_account(
        self, auth: AuthContainer, account_id: uuid.UUID, *, active: bool
    ) -> Account:
        """
        Update an external account

        Only admins have access to this method

        Args:
            auth (AuthContainer): the account used to update the account. Has
                to have accessLevel admin.
            account_id (uuid.UUID): the UUID of the account
            active (bool): the active set to be updated in the account

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """

        endpoint = f"{self.entrypoint}account/{account_id}"
        payload = {"active": active}
        response = requests.put(
            endpoint, headers=auth.headers, json=payload, verify=self.verify_ssl
        )

        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    # !IMPL PUT /account/
    def change_password(
        self, auth: AuthContainer, current_password: str, new_password: str
    ) -> None:
        endpoint = f"{self.entrypoint}account/"
        payload = {
            "currentPassword": current_password,
            "newPassword": new_password,
        }

        response = requests.put(
            endpoint, headers=auth.headers, json=payload, verify=self.verify_ssl
        )
        if response.status_code > 204:
            raise APIException(response)

    # !IMPL POST /keepalive/
    def keepalive(self, auth: AuthContainer) -> str:
        """
        Extend the login session and retrieve a new token

        Args:
            auth (AuthContainer): the account that should be extended. Has
                to have a valid token

        Returns:
            str

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        endpoint = f"{self.entrypoint}keepalive/"

        response = requests.post(endpoint, headers=auth.headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise APIException(response)

        response_data: KeepaliveAPIResponse = response.json()
        return response_data["token"]
