from typing import Any, Dict, Optional

import requests  # type: ignore


class HttpClient:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        default_headers: Optional[Dict[str, str]] = None,
    ):
        """
        :param base_url: Root URL of your service.
        :param api_key: Optional API key for authentication.
        :param timeout: Request timeout in seconds.
        :param default_headers: Default headers to be used in all requests.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.default_headers = default_headers or {"Content-Type": "application/json"}

        if api_key:
            self.default_headers["Authorization"] = f"Bearer {api_key}"

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict:
        url = f"{self.base_url}{path}"
        all_headers = self.default_headers.copy()
        if headers:
            all_headers.update(headers)
        response = requests.get(
            url, headers=all_headers, params=params, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def post(
        self,
        path: str,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict:
        url = f"{self.base_url}{path}"
        all_headers = self.default_headers.copy()
        if headers:
            all_headers.update(headers)
        response = requests.post(
            url, headers=all_headers, json=json, data=data, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def patch(
        self,
        path: str,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict:
        url = f"{self.base_url}{path}"
        all_headers = self.default_headers.copy()
        if headers:
            all_headers.update(headers)
        response = requests.patch(
            url, headers=all_headers, json=json, data=data, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def post_multipart(
        self,
        path: str,
        data: Dict[str, str],
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """
        Send a multipart/form-data POST request.

        :param path: API endpoint path.
        :param data: Dictionary of form fields (text fields).
        :param files: Dictionary of file data { "file_field_name": ("filename", file_object, "mime/type") }
        :param headers: Optional custom headers.
        """
        url = f"{self.base_url}{path}"
        all_headers = self.default_headers.copy()
        if headers:
            all_headers.update(headers)
        # Remove Content-Type header because requests will set it automatically
        if "Content-Type" in all_headers:
            del all_headers["Content-Type"]

        response = requests.post(
            url, headers=all_headers, data=data, files=files, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
