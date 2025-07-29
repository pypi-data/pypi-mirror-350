import typing
import requests


# ==------------------------------------------------------------== #
# Classes                                                          #
# ==------------------------------------------------------------== #
class Session():
    """Creates requests session for making HTTP/HTTPS requests."""

    def __init__(self) -> None:
        self.session = requests.Session()

    def get(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a GET request."""

        return self.session.get(url, *args, **kwargs)

    def post(self, url: str, *args, **kwargs) -> requests.Response:
        """Sends a POST request."""

        return self.session.post(url, *args, **kwargs)

    def patch(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a PATCH request."""

        return self.session.patch(url, *args, **kwargs)

    def put(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a PUT request."""

        return self.session.put(url, *args, **kwargs)

    def delete(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a DELETE request."""

        return self.session.delete(url, *args, **kwargs)


# ==------------------------------------------------------------== #
# Functions                                                        #
# ==------------------------------------------------------------== #
def get(url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
    """Sends a GET request."""

    return requests.get(url, *args, **kwargs)


def post(url: str, *args, **kwargs) -> requests.Response:
    """Sends a POST request."""

    return requests.post(url, *args, **kwargs)


def patch(url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
    """Sends a PATCH request."""

    return requests.patch(url, *args, **kwargs)


def put(url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
    """Sends a PUT request."""

    return requests.put(url, *args, **kwargs)


def delete(url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
    """Sends a DELETE request."""

    return requests.delete(url, *args, **kwargs)
