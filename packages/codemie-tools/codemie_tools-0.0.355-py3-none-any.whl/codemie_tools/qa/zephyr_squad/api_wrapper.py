import hashlib
import jwt
import time
import logging
import requests
from json import dumps
from urllib.parse import urlencode
from requests import HTTPError
from typing import List, Dict

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 75
DEFAULT_BASE_URL = "https://prod-api.zephyr4jiracloud.com/connect"
DEFAULT_RELATIVE_PATH = "/public/rest/api/1.0"
JWT_EXPIRE_SEC = 3000


# API DOCS:
# General info https://zephyrdocs.atlassian.net/wiki/spaces/ZFJCLOUD/pages/1925120024/REST+API
# Interactive API https://zephyrsquad.docs.apiary.io/#reference/config/get-general-configuration
class ZephyrRestAPI(object):
    def __init__(
        self,
        account_id: str,
        access_key: str,
        secret_key: str,
        base_url: str = DEFAULT_BASE_URL,
        relative_path: str = DEFAULT_RELATIVE_PATH,
        timeout: str =DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url
        self.relative_path = relative_path
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.timeout = int(timeout)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
 
    def request(
        self,
        method="GET",
        path="/",
        data=None,
        json=None,
        flags=None,
        params=None,
        headers=None,
        files=None,
    ):
        """Perform and HTTP request"""
        method = method.upper()

        if not path.startswith("/"):
            path = "/" + path

        raw_url = self.base_url + self.relative_path + path
        url = self._prepare_url(raw_url, flags, params) 

        if files is None:
            data = None if not data else dumps(data)

        headers = self._get_headers(method=method, path=path)
        response = requests.Session().request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=self.timeout,
            files=files,
        )
        response.encoding = "utf-8"

        logger.debug("HTTP: %s %s -> %s %s", method, path, response.status_code, response.reason)
        logger.debug("HTTP: Response text -> %s", response.text)

        self._raise_for_status(response)
        return response

    @staticmethod
    def _prepare_url(url: str, flags: List = None, params: Dict = None):
        """Does some URL encoding magic"""
        if not flags:
            flags = []
        
        if not params:
            params = {}

        params_already_in_url = ("?" in url)

        if params or flags:
            if params_already_in_url:
                url += "&"
            else:
                url += "?"
        if params:
            url += urlencode(params or {})

        if flags:
            url += ("&" if params or params_already_in_url else "") + "&".join(flags or [])

        return url
    
    def _get_headers(self, method: str, path: str):
        """Generate headers"""
        jwt = self._generate_jwt(method=method, path=path)
        return {
            'Authorization': 'JWT '+ jwt,
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }
    
    def _generate_jwt(self, method: str, path: str, jwt_expire_sec: int = JWT_EXPIRE_SEC) -> str:
        """Generate JWT token for header"""
        if "?" not in path: # Without we get 401
            path += "?"
    
        canonical_path = (method + '&' + self.relative_path + path).replace('?', '&')

        payload_token = {
            'sub': self.account_id,
            'qsh': hashlib.sha256(canonical_path.encode('utf-8')).hexdigest(),
            'iss': self.access_key,
            'exp': int(time.time()) + jwt_expire_sec,
            'iat': int(time.time())
        }
        return jwt.encode(payload_token, self.secret_key, algorithm='HS256').strip()


    def _raise_for_status(self, response):
        """Checks the response for errors and throws an exception if return code >= 400"""
        if response.status_code == 401 and response.headers.get("Content-Type") != "application/json;charset=UTF-8":
            raise HTTPError("Unauthorized (401)", response=response)

        if 400 <= response.status_code < 600:
            try:
                error_msg = self._handle_error_message(response.json())
            except Exception as e:
                logger.error(e)
                response.raise_for_status()
            else:
                raise HTTPError(error_msg, response=response)
        else:
            response.raise_for_status()
    
    def _handle_error_message(self, json: str) -> str:
        """Hadles error messages from API response"""
        error_msg_list = json.get("errorMessages", [])
        errors = json.get("errors", {})

        if len(errors):
            if isinstance(errors, dict):
                error_msg_list.append(errors.get("message", ""))
            elif isinstance(errors, list):
                error_msg_list.extend([v.get("message", "") if isinstance(v, dict) else v for v in errors])

        if error := json.get("error"):
            error_msg_list.append(error)

        if error := json.get("clientMessage"):
            error_msg_list.append(error)

        return ",".join(error_msg_list)


