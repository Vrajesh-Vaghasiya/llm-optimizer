from optimizer.exceptions import OptimizerAPIException, OptimizerAPIClientException, OptimizerAPIServerException
from urllib.parse import urlunparse

from optimizer.session import RetrySession
from optimizer.settings import PATHS, HTTPS_CERTIFICATE_LOCATION
import logging


logger = logging.getLogger('root')


class Optimizer:

    def __new__(cls, *args, **kwargs):
        self = "__self__"
        if not hasattr(cls, self):
            instance = object.__new__(cls)
            instance.__init__(*args, **kwargs)
            setattr(cls, self, instance)
        return getattr(cls, self)

    def __init__(self, api_domain, api_schema, access_key):
        super().__init__()
        self.API_DOMAIN = api_domain
        self.API_SCHEME = api_schema
        self.access_key = access_key
        self._session = RetrySession(self)

    def get_task(self, task_id: str) -> any:
        url = urlunparse((self.API_SCHEME, self.API_DOMAIN, f"{PATHS['TASK_PATH']}/{task_id}", '', '', ''))
        headers = {'access-key': self.access_key}
        resp = self._session.get(url, headers=headers, verify=HTTPS_CERTIFICATE_LOCATION)
        self._handle_api_resp(method='GET', url=url, resp=resp)
        if not resp.json():
            logger.error(f"Failed to call the API.")
            raise OptimizerAPIException("API call failed.")
        return resp.json()

    def create_task(self, message_text: str, model: str, temprature: int, max_token: int, input_token: int) -> dict:
        assert isinstance(message_text, str)
        assert isinstance(model, str)
        assert isinstance(temprature, int)
        assert isinstance(max_token, int)
        assert isinstance(input_token, int)

        payload = {
            "model": model,
            "temperature": temprature,
            "max_token": max_token,
            "input_token": input_token,
            "message_text": message_text
        }
        url = urlunparse((self.API_SCHEME, self.API_DOMAIN, f"{PATHS['TASK_PATH']}", '', '', ''))
        headers = {"access-key": self.access_key}
        resp = self._session.post(json=payload, url=url, headers=headers)
        self._handle_api_resp(method='GET', url=url, resp=resp)
        if not resp.json():
            logger.error(f"Failed to call the API.")
            raise OptimizerAPIException("API call failed.")

        return resp.json()

    def _handle_api_resp(self, method, url, resp):
        if not resp.ok:
            logger.debug(f"{method} url: {url} resp: {resp.status_code} {resp.text}")
            if 400 <= resp.status_code < 500:
                raise OptimizerAPIClientException(resp.text)
            elif 500 <= resp.status_code < 600:
                raise OptimizerAPIServerException(resp.text)
            else:
                raise OptimizerAPIException(resp.text)
