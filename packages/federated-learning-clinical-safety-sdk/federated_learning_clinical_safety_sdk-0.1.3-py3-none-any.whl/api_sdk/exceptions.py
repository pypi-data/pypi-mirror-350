# src/my_api_sdk/exceptions.py
import requests

class APIError(Exception):
    """Raised when the API returns a non-2xx response."""

    def __init__(self, status_code: int, message: str):
        super().__init__(f"APIError {status_code}: {message}")
        self.status_code = status_code
        self.message = message

    @classmethod
    def from_response(cls, resp: requests.Response):
        try:
            detail = resp.json().get('detail', resp.text)
        except ValueError:
            detail = resp.text
        return cls(resp.status_code, detail)
