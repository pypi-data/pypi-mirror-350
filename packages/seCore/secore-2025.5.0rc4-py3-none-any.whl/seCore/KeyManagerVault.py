import json

from typing import Optional
from bitflags import BitFlags
from .ConfigSettings import settings
from .CustomLogging import logger
from .Encryption import Encryption
from .Vault import VaultEngine
from .jsondb import JsonDB
from .jsondb.db_types import NewKeyValidTypes

# Constants
SEPARATOR_LINE = "-" * 160


class Logging(BitFlags):
    options = {
        0: "init_folder",
        1: "init_secrets",
        2: "init_v1_schema",
        3: "init_v2_schema",
    }


class KeyManager:
    """
    A key management system that interfaces with Hashicorp Vault.
    
    This class provides functionality for managing and validating keys and their associated roles
    stored in Hashicorp Vault. It supports both v1 and v2 schema formats and includes features
    for key masking, role validation, and schema management.
    
    Attributes:
        _ROLES_KEY (str): Constant defining the key used for role storage in the vault
    """

    _ROLES_KEY = "Roles"

    def __init__(self, secret_key: str = settings.HV_SECRETS_KEY, loggingEnabled: bool = False):
        """
        Initialize the KeyManager with Vault connection settings.
        
        Args:
            secret_key: The secret key used to access the vault. Defaults to settings.HV_SECRETS_KEY
            loggingEnabled: Whether to enable detailed logging. Defaults to False
        
        Raises:
            TypeError: If unable to access or decrypt vault contents
        """
        try:
            # Logging settings
            self.__loggingFlags = Logging()
            self.__loggingFlags.set("init_folder", value=1)
            self.__loggingFlags.set("init_secrets", value=1)
            self.__loggingFlags.set("init_v1_schema", value=0)
            self.__loggingFlags.set("init_v2_schema", value=0)

            if self.__loggingFlags.value > 0:
                logger.info(SEPARATOR_LINE)

            logger.debug(json.dumps({"key_manager_vault": {"logging": f'{self.__loggingFlags.value} - {self.__loggingFlags}'}}))

            self._keys = {}
            self.__domain = settings.HV_DOMAIN
            self.__namespace = settings.HV_NAMESPACE
            self.__approle_name = settings.HV_APPROLE
            self.__approle_role_id = settings.HV_APPROLE_ROLE_ID
            self.__approle_secret_id = settings.HV_APPROLE_SECRET_ID
            # self.__secrets_folder = settings.HV_EDSAP_SECRETS_FOLDER.replace("{env}", settings.ENVIRONMENT.lower())
            self.__secrets_folder = f'{settings.HV_SECRETS_FOLDER}'
            self.__secret_key = secret_key
            self.encryption = Encryption()
            self.__logging_enabled = loggingEnabled
            self.__version = None

            if self.__loggingFlags.init_folder:  # Logging: __init__ - folder
                logger.info(json.dumps({"key_manager_vault": {"secrets_folder": self.__secrets_folder}}))

            self.vlt = VaultEngine(self.__domain,
                                   self.__namespace,
                                   self.__approle_name,
                                   self.__approle_role_id,
                                   self.__approle_secret_id)
            secrets, status_code = self.vlt.get_value(self.__secrets_folder, self.__secret_key)

            if self.__loggingFlags.init_secrets:  # Logging: __init__ - secrets
                logger.warning(json.dumps({"key_manager_vault": {"secrets": secrets}}))

            # Could not find km settings in Vault
            if "** not found **" in secrets['value']:
                logger.error(json.dumps({"key_manager_vault": {"folder": self.__secrets_folder},
                                         "code": 1501,
                                         "desc": "Key not found, Need to create new km values"}))
                # raise TypeError(f'Could not find secret key ({secrets["key"]}), check your secrets folder for the correct value')
            else:
                # Check for v2
                if 'data' in self.encryption.decrypt(secrets['value']):
                    if self.__loggingFlags.init_v2_schema:  # pragma: no cover
                        logger.warning(json.dumps({"key_manager_vault": {"v2_schema": json.loads(self.encryption.decrypt(secrets['value']))}}))
                    self.__db = JsonDB("", load_json=json.loads(self.encryption.decrypt(secrets['value'])))
                    self._keys = self._load_keys_from_vault()
                    self.__version = 2
                # Check for v1
                elif 'Roles' in self.encryption.decrypt(secrets['value']):

                    _defaultKeys = {
                        "keys": [],
                        "data": json.loads(self.encryption.decrypt(secrets['value']))
                    }
                    if self.__loggingFlags.init_v1_schema:  # pragma: no cover
                        logger.warning(json.dumps({"key_manager_vault": {"v1_schema": _defaultKeys}}))
                    self.__db = JsonDB("", load_json=_defaultKeys)
                    self._keys = self._load_keys_from_vault()
                    self.__version = 1

                # Error: not in the correct KM format
                else:
                    logger.error(json.dumps({"key_manager_vault": {"folder": self.__secrets_folder},
                                             "code": 1500,
                                             "desc": "Data is not in the correct format",
                                             "vault": json.loads(self.encryption.decrypt(secrets['value']))
                                             }, indent=4))

        except TypeError as e:
            logger.error(json.dumps({"keys": {"error": f'{e}'}}))

        logger.info(json.dumps({"key_manager_vault": {"key_cnt": len(self._keys),
                                                      "keys": list(self._keys.keys())}}))

    def _load_keys_from_vault(self) -> dict:
        return self.__db.get_all()

    # ---------------------------------------------------------------------------------------------

    def get_all_keys(self) -> dict:
        """
        Returns all keys as a dictionary.
        """
        return self._keys

    # ---------------------------------------------------------------------------------------------

    @staticmethod
    def get_masked_keys() -> dict:
        """
        Returns masked versions of all keys.
        """
        original_keys = keyManager.get_all_keys()
        masked_keys = {}
        for key, value in original_keys.items():
            masked_key = keyManager.mask_key(value["Key"])
            value["Key"] = masked_key
            masked_keys[masked_key] = value
        return masked_keys

    # ---------------------------------------------------------------------------------------------

    def validate_key(self, key: str) -> bool:
        """
        Checks if a given key is valid.
        """
        return key in self._keys

    # ---------------------------------------------------------------------------------------------

    def mask_key(self, key: str) -> str:
        """
        Masks a key by returning its last segment.
        """
        return key.split("-")[-1] if self.validate_key(key) else ""

    # ---------------------------------------------------------------------------------------------

    def get_roles(self, key: str) -> list:
        """
        Returns the roles associated with a given key.
        :param key: The key to retrieve roles for.
        :return: A list of roles.
        """
        return self._keys.get(key, {}).get("Roles", [""])

    # ---------------------------------------------------------------------------------------------

    def _get_roles_from_key(self, key: str) -> list:
        """Helper function to fetch roles for a given key."""
        key_data = self._keys.get(key)
        if key_data and self._ROLES_KEY in key_data:
            return key_data[self._ROLES_KEY]
        return []

    @staticmethod
    def _normalize_roles(roles: str | list[str]) -> list[str]:
        """Ensure roles is always a list."""
        return [roles] if isinstance(roles, str) else roles

    def validate_role(self, key: str, roles: str | list[str]) -> bool:
        """Validates if a role is associated with a key."""
        allowed_roles = self._get_roles_from_key(key)
        roles_to_validate = self._normalize_roles(roles)

        return bool(set(allowed_roles).intersection(roles_to_validate))

    def validate_key_role(self, key: str, roles: str | list[str]) -> dict:
        """
            Validates the given key and role(s) and returns a detailed dictionary
            containing the key, its roles, a masked version of the key, valid roles
            obtained for the key, and the result of the role validation.
            """
        return {
            "key": key,
            "roles": roles,
            "key_mask": self.mask_key(key),
            "valid_roles": self.get_roles(key),
            "role_valid": self.validate_role(key, roles),
        }

    def schema_version(self):
        """
        Retrieves the schema version associated with the current instance.

        The schema version is stored privately within the object and can
        be retrieved for operations requiring version control or checks.

        :return: The schema version of the instance.
        :rtype: str
        """
        return self.__version

    # ---------------------------------------------------------------------------------------------
    # Need to validate these functions, so skipping for now
    # ---------------------------------------------------------------------------------------------

    # todo: add_new_key - validate and test
    def add_new_key(self, key: str, default: Optional[NewKeyValidTypes] = None) -> None:  # pragma: no cover
        self.__db.add_new_key(key, default)

    # todo: set_schema - validate and test
    def set_schema(self, schema: dict):  # pragma: no cover
        """
        Update keys in Vault
        Args:
            schema: str

        Returns:
            None
        """
        self.__db = JsonDB("", load_json=schema)
        # logger.error(json.dumps(self.__db.dump_json()))
        self.vlt.app_init()  # pragma: no cover
        self.vlt.update_value(self.__secrets_folder, self.__secret_key, self.encryption.encrypt(json.dumps(self.__db.dump_json())).decode())  # pragma: no cover
        logger.info(json.dumps({"keys": {"count": len(self._keys)}}))  # pragma: no cover
        # logger.info(json.dumps({"key_manager_vault": {"key_cnt": len(self.keys),
        #                                "keys": list(self.keys.keys())}}))

    # todo: set_keys - validate and test
    def set_keys(self, keys: dict):  #
        """
        Update keys in Vault
        Args:
            keys: dict

        Returns:
            None
        """
        self._keys = keys  # pragma: no cover
        self.vlt.app_init()  # pragma: no cover
        self.vlt.update_value(self.__secrets_folder, self.__secret_key, self.encryption.encrypt(json.dumps(keys)).decode())  # pragma: no cover
        logger.info(json.dumps({"keys": {"count": len(self._keys)}}))  # pragma: no cover
        # logger.info(json.dumps({"key_manager_vault": {"key_cnt": len(self.keys),
        #                                "keys": list(self.keys.keys())}}))

    def get_key_element(self, key: str, element_name: str, default_value: any = None) -> any:  # pragma: no cover
        """
        Returns any element from the key data with a default value if not found.

        Args:
            key: The key to look up data for
            element_name: Name of the element to retrieve from key data
            default_value: Value to return if key or element is not found (default: None)

        Returns:
            The value of the requested element or the default_value if not found
        """
        key_data = self._keys.get(key, {})
        return key_data.get(element_name, default_value)


# Singleton instance of the KeyManager.
keyManager = KeyManager()
