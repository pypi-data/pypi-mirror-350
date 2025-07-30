import enum
import requests
import urllib3

from typing import Optional

urllib3.disable_warnings()


class HttpAction(enum.Enum):
    """
    Enumeration class representing HTTP actions.

    This class provides constants for various HTTP methods and is
    intended to standardize the use of these methods across an
    application where HTTP requests are handled.
    """
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"


class HttpRest:
    """
    Represents an HTTP REST service handling HTTP requests and responses efficiently.

    This class provides methods to perform HTTP requests (GET, POST, PATCH) using configurable
    timeouts, customized headers, and optional authentication tokens. It consolidates
    logging, error handling, and response formatting for easier debugging and integration
    into other applications.

    :ivar http_details: Contains log details related to the most recent HTTP request.
    :type http_details: list

    :ivar http_timeout: Specifies the timeout value in seconds for HTTP requests.
    :type http_timeout: int
    """
    DEFAULT_HTTP_TIMEOUT = 30

    def __init__(self, http_timeout: int = DEFAULT_HTTP_TIMEOUT):
        """
        Initializes a new instance of the HttpRest class with a default timeout.
        """
        self.http_details = []
        self.http_timeout = http_timeout

    def http_request(self, action: HttpAction,url: str, headers: dict = None, token: str = None, body: dict = None, http_verify: bool = False):
        """
        Makes an HTTP request with the specified parameters and processes the response.

        This method is used to perform an HTTP request based on the provided action
        and URL, along with optional headers, token, request body, and HTTP verification
        settings. The request details are logged, the specified action is executed,
        and the response is handled accordingly. The method returns the processed
        response for the executed request.

        :param action: An instance of HttpAction specifying the HTTP method to be used
                      (e.g., GET, POST, PUT, DELETE).
        :param url: The target URL for the HTTP request as a string.
        :param headers: Optional dictionary containing HTTP headers to include in the
                        request.
        :param token: Optional string representing the authentication token for the
                      request.
        :param body: Optional dictionary containing the body payload of the HTTP
                     request for applicable methods (e.g., POST, PUT).
        :param http_verify: Boolean is indicating whether the SSL certificate verification
                            should be performed (default is False).
        :return: The response object is processed by `_handle_response`, based on the
                 result of the HTTP request.
        """
        headers = self._prepare_headers(headers, token)
        self._log_request_details(token, action, url)
        response = self._perform_request(url, action, headers, body, http_verify)
        return self._handle_response(response)

    def _perform_request(self, url: str, action: HttpAction, headers: dict, body: dict, http_verify: bool):
        """
        Performs an HTTP request using the specified HTTP action, URL, headers, and body.
        This method uses the requests library to make GET, POST, or PATCH requests
        based on the provided action. The request is configured with a timeout
        defined by the `self.http_timeout` attribute and allows for optional SSL
        certificate verification using the `http_verify` parameter.

        :param url: The endpoint URL to which the HTTP request will be sent.
        :param action: The desired HTTP action (GET, POST, PATCH) to perform.
        :param headers: A dictionary of HTTP headers to include in the request.
        :param body: The JSON payload to include in the request body.
        :param http_verify: A boolean indicating whether to verify SSL certificates.
        :return: The response object from the requests' library.
        """
        methods = {
            HttpAction.GET: requests.get,
            HttpAction.POST: requests.post,
            HttpAction.PATCH: requests.patch,
        }
        return methods[action](url, headers=headers, json=body, timeout=self.http_timeout, verify=http_verify)

    @staticmethod
    def _prepare_headers(headers: Optional[dict], token: Optional[str]) -> dict:
        """
        Prepares and returns headers for an HTTP request based on the provided headers
        or generates common headers if none are provided.

        The method checks if custom headers are passed. If they are available, it uses them
        as they are. If not, it will generate and return default headers using the
        `HttpRest.get_common_rest_headers()` method, ensuring a proper token is included.

        :param headers: Optional dictionary containing HTTP headers. When provided, these headers
            are returned as-is without modification.
        :param token: Optional string representing an authorization token. This token is used
            to generate headers if the `headers` parameter is not supplied.
        :return: A dictionary containing the headers for the HTTP request.
        """
        return headers if headers else HttpRest.get_common_rest_headers(token)

    @staticmethod
    def get_common_rest_headers(token: Optional[str]) -> dict:
        """Returns common HTTP headers with optional authorization.
        :rtype: object
        """
        return {
            "Authorization": f"Bearer {token}" if token else "",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @staticmethod
    def _handle_response(response):
        """
        Extracts and formats the response from the server.
        """
        data = {'status_code': response.status_code, 'empty_response': True}
        if response.text:
            data = response.text
            if response.status_code >= 400:  # Handle error responses
                data = {'status_code': response.status_code, 'response': response.text}
        return data, response.status_code

    def _log_request_details(self, token: str, action: HttpAction, url: str):
        """
        Appends request details to the log for debugging or tracking purposes.
        """
        token_detail = f"API Token provided with length: {len(token)}" if token else "No API token provided"

        self.http_details = []
        self.http_details.append({"token": token_detail, "action": f"Sending {action.value} request to {url}"})
