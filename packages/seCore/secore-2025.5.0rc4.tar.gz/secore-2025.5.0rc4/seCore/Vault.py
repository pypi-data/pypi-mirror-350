import base64
import inspect
import json
import os
import sys
from pickle import FALSE
from typing import Any

import urllib3

# from app.core.Attributes import class_function
from .CustomLogging import logger
from .Exceptions import Vault_KeyError, Vault_FolderError
from .HttpRest import HttpRest, HttpAction

urllib3.disable_warnings()


class VaultEngine:
    """
    A class for authenticating with Hashicorp Vault.

    Attributes:
    - domain (str): Hashicorp Vault Url
    - namespace (str): Vault Namespace
    - app_role (str): Vault AppRole ID
    - role_id (str): Vault Role ID
    - secret_id (str): Vault Secret ID

    - vault_token (str): set during authentication in app_init
    - value_value (str): set during get_value
    - update_value (int): status_code
    """

    def __init__(self, domain: str, namespace: str, app_role: str, role: str, secret: str, headers: str = "", loggingEnabled: bool = False):
        """
        Initializes a new instance of the VaultEngine class.

        Parameters:
        - url (str): Hashicorp Vault Url
        - role_id (str): Vault Role ID
        - secret_id (str): Vault Secret ID
        """
        if len(namespace) == 0:
            self.__urlLogin = f'{domain}/v1/auth/approle/login'
            self.__urlKV_Data = f'{domain}/v1/kv/data'
        else:
            self.__urlLogin = f'{domain}/v1/{namespace}/auth/{app_role}/login'
            self.__urlKV_Data = f'{domain}/v1/{namespace}/kv/data'

        self.__logging_enabled = loggingEnabled
        self.__role_id = base64.b64decode(role).decode()
        self.__secret_id = base64.b64decode(secret).decode()
        self.__headers = ({} if len(headers) == 0 else {x.replace(' ', ''): v.replace(' ', '') for x, v in dict(s.split(':') for s in headers.split(",")).items()})
        self.__hashicorp_keys = {}
        self.hashicorp_token = None
        self.hashicorp_value = None

        self.app_init()

    def app_init(self):
        """
        Initializes the GitHub App and generates a token for the Vault.
        """
        self.hashicorp_token = self.get_token()

    @property
    def vault_token(self):
        """
        Gets the token for the hashicorp to pull settings.

        Returns:
        - str: the hashicorp token
        """
        return self.hashicorp_token

    @property
    def vault_value(self):
        """
        Gets the value from hashicorp settings.

        Returns:
        - str: hashicorp value
        """
        return self.hashicorp_value

    # @property
    # def vault_keys(self, ):
    #     """
    #     Gets the keys from hashicorp project settings.
    #
    #     Returns:
    #     - dict: hashicorp keys to given project
    #     """
    #     return self.__keys

    # @class_function
    def get_token(self) -> str:
        """
        Gets the hashicorp token

        Returns:
            - str: the hashicorp token
        """
        try:
            body = {
                "role_id": self.__role_id,
                "secret_id": self.__secret_id
            }
            logger.debug(json.dumps({"vault": "get_token", "body": body}))

            rest_api = HttpRest()
            url = self.__urlLogin
            response, _ = rest_api.http_request(HttpAction.POST,url, body=body)
            self.hashicorp_token = json.loads(response)["auth"]["client_token"]
            if self.__logging_enabled:  # Logging: get_token
                logger.info(json.dumps({"vault": "get_token",
                                        "body": body,
                                        "token": self.hashicorp_token}))
        except Exception as ex:
            self.hashicorp_token = ""
            logger.error(json.dumps({"vault": "get_token", "result": "Failed to login to Vault", "error": str(ex)}))

        return self.hashicorp_token

    # @class_function
    def get_value(self, secrets_folder: str = "", key: str = "") -> tuple[dict[str, str] | dict[str, str], Any | None]:
        """
        Gets the hashicorp value from settings

        Returns:
        - str: the hashicorp settings value
        - int: status_code
        """
        status_code = None
        try:
            rest_api = HttpRest()
            headers = {"X-Vault-Token": self.hashicorp_token} | self.__headers

            url = f'{self.__urlKV_Data}/{secrets_folder}'
            if self.__logging_enabled:  # Logging: get_value - url
                logger.info(json.dumps({"vault": {"url": url}}))

            response, status_code = rest_api.http_request(HttpAction.GET,url, headers=headers)
            response = json.loads(response)
            match status_code:
                case 200:
                    selfKeys = {k.lower(): v for k, v in response["data"]["data"].items()}
                    if self.__logging_enabled:  # Logging: get_value - keys
                        logger.info(json.dumps({"vault": {"keys": list(selfKeys.keys())}}))
                    self.hashicorp_value = {
                        "project": secrets_folder,
                        "key": key.lower(),
                        "value": selfKeys.get(key.lower(), "** not found **")}
                case _:
                    raise Exception(response)

        except TypeError:
            self.hashicorp_value = {
                "project": secrets_folder,
                "key": key.lower(),
                "value": "** not found **"
            }  # pragma: NotTested

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            logger.error(json.dumps({f'{inspect.currentframe().f_code.co_name}': {
                'exception_type': f'{exception_type}',
                'file': os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1],
                'line_number': exception_traceback.tb_lineno,
                'msg': f'{e}'
            }}))

        return self.hashicorp_value, status_code

    # @class_function
    def get_values(self, secrets_folder: str = "") -> tuple[dict[str, str] | dict[str, str], dict | None]:
        """
        Gets the hashicorp values from foldes

        Returns:
        - str: the hashicorp settings values
        - int: status_code
        """
        status_code = None
        data = {}
        try:
            rest_api = HttpRest()
            headers = {"X-Vault-Token": self.hashicorp_token} | self.__headers

            url = f'{self.__urlKV_Data}/{secrets_folder}'

            response, status_code = rest_api.httpGet(url, headers=headers)
            data = response["data"]["data"]

            logger.info(json.dumps({"vault": "get_values",
                                    "folder": secrets_folder,
                                    "status_code": status_code, }))

        except Exception as e:  # pragma: no cover
            exception_type, exception_object, exception_traceback = sys.exc_info()
            # logger.error(json.dumps({f'{inspect.currentframe().f_code.co_name}': {'exception_type': f'{exception_type}','file': os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1],'line_number': exception_traceback.tb_lineno,'msg': f'{e}'}}))
            logger.error(json.dumps({'vault': 'get_values',
                                     'folder': secrets_folder,
                                     'status_code': status_code,
                                     'description': 'Invalid path. This can both mean that the path truly doesn''t exist or that you don''t have permission to view a specific path.',
                                     'exception_type': f'{exception_type}',
                                     'file': os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1],
                                     'line_number': exception_traceback.tb_lineno,
                                     'msg': f'{e}'
                                     }))
            raise Vault_FolderError(json.dumps(
                {
                    "folder": secrets_folder,
                    "value": "Invalid path. This can both mean that the path truly doesn't exist or that you don't have permission to view a specific path."
                }))

        return data, status_code

    # @class_function
    def update_folder(self, secrets_folder: str, secrets_data: dict) -> int:
        """
        Update the hashicorp value from settings

        Returns:
        - int: status_code
        """
        status_code = None
        try:
            rest_api = HttpRest()
            headers = {"X-Vault-Token": self.hashicorp_token} | self.__headers

            url = f'{self.__urlKV_Data}/{secrets_folder}'
            body = {
                'data': secrets_data
            }

            if self.__logging_enabled:  # Logging: update_folder - body
                logger.info(f'update_folder - Body: {json.dumps(body)}')
            response, status_code = rest_api.httpPost(url, headers=headers, body=body)

        except TypeError:  # pragma: NotTested
            self.hashicorp_value = {
                "project": secrets_folder,
                "key": key.lower(),
                "value": "** not found **"
            }

        except Exception as e:  # pragma: NotTested
            exception_type, exception_object, exception_traceback = sys.exc_info()
            logger.error(json.dumps({f'{inspect.currentframe().f_code.co_name}': {
                'exception_type': f'{exception_type}',
                'file': os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1],
                'line_number': exception_traceback.tb_lineno,
                'msg': f'{e}'
            }}))

        return status_code

    # @class_function
    def update_value(self, secrets_folder: str, key: str, value: str, update: bool = True) -> int:
        """
        Update the hashicorp value from settings

        Returns:
        - int: status_code
        """
        status_code = None
        try:
            _currentFolder, status_code = self.get_values(secrets_folder)
            _currentFolder[key] = value
            if self.__logging_enabled:  # Logging: update_value - value
                logger.info(json.dumps({"update_value": {key: value}}))
                logger.info(json.dumps(_currentFolder, indent=2))

            if update:
                rest_api = HttpRest()
                headers = {"X-Vault-Token": self.hashicorp_token} | self.__headers

                url = f'{self.__urlKV_Data}/{secrets_folder}'
                body = {
                    "data": _currentFolder
                }

                if self.__logging_enabled:  # Logging: update_value - body
                    logger.info(f'update_value - Body: {json.dumps(body)}')
                response, status_code = rest_api.httpPost(url, headers=headers, body=body)

        except TypeError:  # pragma: NotTested
            self.hashicorp_value = {
                "project": secrets_folder,
                "key": key.lower(),
                "value": "** not found **"
            }

        except Exception as e:  # pragma: NotTested
            exception_type, exception_object, exception_traceback = sys.exc_info()
            logger.error(json.dumps({f'{inspect.currentframe().f_code.co_name}': {
                'exception_type': f'{exception_type}',
                'file': os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1],
                'line_number': exception_traceback.tb_lineno,
                'msg': f'{e}'
            }}))

        return status_code

    # @class_function
    def delete_value(self, secrets_folder: str, key: str, update: bool = True) -> int:
        """
        Delete the hashicorp value from settings

        Returns:
        - int: status_code
        """
        status_code = None
        try:
            _currentFolder, status_code = self.get_values(secrets_folder)
            _deletedKey = _currentFolder.pop(key)
            if self.__logging_enabled:  # Logging: delete_value - value
                logger.info(json.dumps({"deleted_key": _deletedKey}))
                logger.info(json.dumps(_currentFolder, indent=2))
            if update:
                rest_api = HttpRest()
                headers = {"X-Vault-Token": self.hashicorp_token} | self.__headers

                url = f'{self.__urlKV_Data}/{secrets_folder}'
                body = {
                    "data": _currentFolder
                }

                if self.__logging_enabled:  # Logging: delete_value - body
                    logger.info(f'delete_value - Body: {json.dumps(body)}')
                response, status_code = rest_api.httpPost(url, headers=headers, body=body)

        except KeyError:
            raise Vault_KeyError(json.dumps(
                {
                    "folder": secrets_folder,
                    "key": key.lower(),
                    "value": "** not found **"
                }))

        return status_code
