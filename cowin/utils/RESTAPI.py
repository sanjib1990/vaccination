from requests.exceptions import HTTPError
import requests
from typing import Union

from cowin.utils.logit import get_logger
from cowin.utils.user_agents import random_user_agent


class RestAPI(object):
    def call(self, rest_method_name: str, url: str,
             headers=None, data=None) -> Union[HTTPError, dict]:
        logger = get_logger(__name__)
        user_agent = random_user_agent()
        logger.debug(f"{user_agent}")
        headers = {'User-Agent': user_agent}
        module = __import__('requests')
        rest_method = getattr(module, rest_method_name)
        response = rest_method(url, headers=headers)
        try:
            response.raise_for_status()
        except HTTPError as e:
            return False, e
        return True, response.json()
