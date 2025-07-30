from typing import Optional, List, Dict

import requests as req

from pygeai import logger


class ApiService:
    """
    Generic service for interacting with RESTful APIs.

    :param base_url: str - The base URL of the API.
    :param username: str - Optional username for authentication.
    :param password: str - Optional password for authentication.
    :param token: str - Optional token for authentication.
    """

    def __init__(self, base_url, username: str = None, password: str = None, token: str = None):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._token = token

    @property
    def base_url(self):
        return self._base_url

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def token(self):
        return self._token

    def get(self, endpoint: str, params: dict = None, headers: dict = None, verify: bool = True):
        """
        Sends a GET request to the specified API endpoint.

        :param endpoint: str - The API endpoint to send the request to.
        :param params: dict - Optional query parameters for the request.
        :param headers: dict - Optional headers for the request.
        :param verify: bool - Optional verification of the connection.
        :return: Response object from the GET request.
        """
        try:
            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (
                        self.username,
                        self.password
                    )
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                response = session.get(
                    url=url,
                    params=params,
                    headers=headers
                )
        except Exception as e:
            logger.error(f"Error sending GET request: {e}")
        else:
            logger.debug(f"GET request to URL: {response.url}")
            return response

    def post(self, endpoint: str, data: dict, headers: dict = None, verify: bool = True, form: bool = False):
        """
        Sends a POST request to the specified API endpoint.

        :param endpoint: str - The API endpoint to send the request to.
        :param data: dict - The payload to include in the POST request.
        :param headers: dict - Optional headers for the request.
        :param verify: bool - Whether to verify SSL certificates. Defaults to True.
        :param form: bool - Whether to send data in json format or in form. Defaults to False (JSON).
        :return: Response object from the POST request.
        """
        try:
            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (
                        self.username,
                        self.password
                    )
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                if form:
                    response = session.post(
                        url=url,
                        data=data,
                        headers=headers
                    )
                else:
                    response = session.post(
                        url=url,
                        json=data,
                        headers=headers
                    )
        except Exception as e:
            logger.error(f"Error sending POST request: {e}")
        else:
            logger.debug(f"POST request to URL: {response.url}")
            return response

    def stream_post(
            self,
            endpoint: str,
            data: dict,
            headers: dict = None,
            verify: bool = True,
            form: bool = False
    ):
        """
        Sends a streaming POST request to the specified API endpoint.

        :param endpoint: str - The API endpoint to send the request to.
        :param data: dict - The payload to include in the POST request.
        :param headers: dict - Optional headers for the request.
        :param verify: bool - Whether to verify SSL certificates. Defaults to True.
        :param form: bool - Whether to send data in form format instead of JSON. Defaults to False (JSON).
        :return: Generator yielding chunks of the streaming response.
        """
        try:
            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (self.username, self.password)
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                if form:
                    response = session.post(
                        url=url,
                        data=data,
                        headers=headers,
                        stream=True
                    )
                else:
                    response = session.post(
                        url=url,
                        json=data,
                        headers=headers,
                        stream=True
                    )

                response.raise_for_status()
                logger.debug(f"Streaming POST request to URL {response.url}")
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        yield line

        except Exception as e:
            logger.error(f"Error sending streaming POST request: {e}")
            raise

    def post_file_binary(
            self,
            endpoint: str,
            headers: dict = None,
            verify: bool = True,
            file=None
    ):
        try:
            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (
                        self.username,
                        self.password
                    )
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                response = session.post(
                    url=url,
                    headers=headers,
                    data=file
                )
        except Exception as e:
            logger.error(f"Error sending POST request with binary file: {e}")
        else:
            logger.debug(f"POST request with binary file to URL: {response.url}")
            return response

    def post_files_multipart(
            self,
            endpoint: str,
            data: Optional[dict] = None,
            headers: Optional[dict] = None,
            verify: bool = True,
            files: Optional[Dict[str, str]] = None,
    ):
        try:
            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (
                        self.username,
                        self.password
                    )
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                # headers["Content-Type"] = "multipart/form-data"

                response = session.post(
                    url=url,
                    headers=headers,
                    data=data,
                    files=files
                )
        except Exception as e:
            logger.error(f"Error sending POST request with files multipart: {e}")
        else:
            logger.debug(f"POST request with multipart files to URL: {response.url}")
            return response

    def put(self, endpoint: str, data: dict, headers: dict = None, verify: bool = True):
        """
        Sends a PUT request to the specified API endpoint.

        :param endpoint: str - The API endpoint to send the request to.
        :param data: dict - The payload to include in the PUT request.
        :param headers: dict - Optional headers for the request.
        :param verify: bool - Whether to verify SSL certificates. Defaults to True.
        :return: Response object from the PUT request.
        """
        try:

            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (
                        self.username,
                        self.password
                    )
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                headers["Content-Type"] = "application/json"

                response = session.put(
                    url=url,
                    json=data,
                    headers=headers
                )
        except Exception as e:
            logger.error(f"Error sending PUT request: {e}")
        else:
            logger.debug(f"PUT request to URL: {response.url}")
            return response

    def delete(self, endpoint: str, headers: dict = None, data: dict = None, verify: bool = True):
        """
        Sends a DELETE request to the specified API endpoint.

        :param endpoint: str - The API endpoint to send the request to.
        :param headers: dict - Optional headers for the request.
        :param data: dict - Optional data for the request.
        :param verify: bool - Whether to verify SSL certificates. Defaults to True.
        :return: Response object from the DELETE request.
        """
        try:
            url = self._add_endpoint_to_url(endpoint)

            with req.Session() as session:
                if self.username and self.password:
                    session.auth = (
                        self.username,
                        self.password
                    )
                elif self.token:
                    headers = self._add_token_to_headers(headers)

                session.verify = verify

                response = session.delete(
                    url=url,
                    headers=headers,
                    params=data
                )
        except Exception as e:
            logger.error(f"Error sending DELETE request: {e}")
        else:
            logger.debug(f"DELETE request to URL: {response.url}")
            return response

    def _add_endpoint_to_url(self, endpoint: str):
        clean_base_url = self.base_url.rstrip('/')
        url = f"{clean_base_url}/{endpoint}" if self._has_valid_protocol(clean_base_url) else f"https://{clean_base_url}/{endpoint}"
        return url

    def _has_valid_protocol(self, url: str):
        return url.startswith(('http://', 'https://'))

    def _add_token_to_headers(self, headers: dict = None):
        if not headers:
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
        else:
            if "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {self.token}"

        return headers
