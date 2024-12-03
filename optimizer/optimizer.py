from optimizer.exceptions import OptimizerAPIException, OptimizerAPIClientException, OptimizerAPIServerException
from urllib.parse import urlunparse
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

    def __init__(self, api_domain, api_schema):
        super().__init__()
        self.API_DOMAIN = api_domain
        self.API_SCHEME = api_schema

    def get_task(self, task_id):
        url = urlunparse((self.API_SCHEME, self.API_DOMAIN, f"{PATHS['TASK_PATH']}/{task_id}", '', '', ''))
        params = {}
        resp = self._session.get(url, params={}, verify=HTTPS_CERTIFICATE_LOCATION)
        self._handle_api_resp(method='GET', url=url, params={}, resp=resp)
        if not resp.json():
            logger.error(f"Failed to call the API.")
            raise OptimizerAPIException("API call failed.")
        return resp.json()

    def _handle_api_resp(self, method, url, data, resp):
        if not resp.ok:
            logger.debug(f"{method} url: {url} data: {data}\nresp: {resp.status_code} {resp.text}")
            if 400 <= resp.status_code < 500:
                raise OptimizerAPIClientException(resp.text)
            elif 500 <= resp.status_code < 600:
                raise OptimizerAPIServerException(resp.text)
            else:
                raise OptimizerAPIException(resp.text)
