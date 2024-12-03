from requests.sessions import Session
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from optimizer.settings import API_BACKOFF_FACTOR, API_RETRY_COUNT, API_STATUS_FORCE_LIST


class RetrySession(Session):
    """
    A Session which refreshes the auth token and retries the request if the response returns a 401.
    """

    def __init__(self, optimizer, with_retry=True) -> None:
        self.optimizer = optimizer
        super().__init__()
        if with_retry:
            # If backoff_factor is 0.5 and API_RETRY_COUNT is 3, api is called after [0.5,1,2]
            # If backoff_factor is 1 and API_RETRY_COUNT is 3, api is called after [1,2,4]
            # this is formula: sleep time = {backoff factor} * (2 ** ({number of total retries} - 1))
            retry = Retry(total=API_RETRY_COUNT, backoff_factor=API_BACKOFF_FACTOR, status_forcelist=[int(x) for x in API_STATUS_FORCE_LIST.split(',')], allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"])
            adapter = HTTPAdapter(max_retries=retry)
            self.mount('http://', adapter)
            self.mount('https://', adapter)

    def get(self, url, **kwargs) -> Response:
        response = super().get(url, **kwargs)
        if response.status_code == 401:
            self.optimizer.refresh_token()
            response = self.get(url, **kwargs)
        return response

    def post(self, url, data=None, json=None, **kwargs) -> Response:
        response = super().post(url, data=data, json=json, **kwargs)
        if response.status_code == 401:
            self.optimizer.refresh_token()
            response = self.post(url, data=data, json=json, **kwargs)
        return response


class PostRetrySession(Session):
    def __init__(self, optimizer, with_retry=True) -> None:
        self.optimizer = optimizer
        super().__init__()
        if with_retry:
            # If backoff_factor is 0.5 and API_RETRY_COUNT is 3, api is called after [0.5,1,2]
            # If backoff_factor is 1 and API_RETRY_COUNT is 3, api is called after [1,2,4]
            # this is formula: sleep time = {backoff factor} * (2 ** ({number of total retries} - 1))
            retry = Retry(total=API_RETRY_COUNT, backoff_factor=API_BACKOFF_FACTOR, status_forcelist=[501, 502, 503], allowed_methods=["HEAD", "OPTIONS", "POST"])
            adapter = HTTPAdapter(max_retries=retry)
            self.mount('http://', adapter)
            self.mount('https://', adapter)

    def post(self, url, data=None, json=None, **kwargs) -> Response:
        response = super().post(url, data=data, json=json, **kwargs)
        if response.status_code == 401:
            self.optimizer.refresh_token()
            response = self.post(url, data=data, json=json, **kwargs)
        return response
