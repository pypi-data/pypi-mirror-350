import json

from requests import request


class Http:
    """
    A class for making HTTP requests.
    """
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def post(self, url, body, headers, timeout=10):
        """
        Send a POST request to the given URL with
        the provided body and headers.

        Args:
            url (str): The URL to send the request to.
            body (dict): The request body.
            headers (dict): The request headers.
            timeouts (dict, optional): The request timeouts. Defaults to None.

        Returns:
            dict: The response from the server.
        """
        headers = self.headers | headers
        data = json.dumps(body)
        result = request(
            method="POST", url=url,
            headers=headers, data=data, timeout=timeout
        )
        result.raise_for_status()
        return result.json()
