import requests


class APIException(Exception):
    def __init__(self, response: requests.Response) -> None:
        self.response: requests.Response = response
        self.status_code: int = response.status_code

        msg = f"APIException: status code {self.status_code}"
        super().__init__(msg)


class MissingAccountException(Exception):
    pass


class MissingClientException(Exception):
    pass
