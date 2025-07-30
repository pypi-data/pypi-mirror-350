import json
import os

from bitflags import BitFlags
from .CustomLogging import logger
from .ProjectRoot import project_root
from .templates import Keys

# Constants
ENV_FILE_SECRETS = ".env.secrets"
KEYS_FILE_SECRETS = "keys.json"
DEFAULT_CONFIG_PATH = os.path.join(project_root(), "app")
DEFAULT_SECRET_PATH = os.path.join(DEFAULT_CONFIG_PATH, "secrets")
SEPARATOR_LINE = "-" * 160


class Logging(BitFlags):
    options = {
        0: "init_secrets",
        1: "show_keys"
    }


class KeyManager:
    _ROLES_KEY = "Roles"

    def __init__(self, secret_path=DEFAULT_SECRET_PATH):
        """
        Initializes the KeyManager by loading keys from a file or defaults.
        """

        # Logging settings
        self.__loggingFlags = Logging()
        self.__loggingFlags.set("init_secrets", value=1)
        self.__loggingFlags.set("show_keys", value=1)
        # self.__loggingFlags.value =
        self._secret_dir: str = secret_path

        if self.__loggingFlags.value > 0:
            logger.info(SEPARATOR_LINE)

            logger.debug(json.dumps({"key_manager": {"logging": f'{self.__loggingFlags.value} - {self.__loggingFlags}'}}))

        self._setup_directories_and_configs()
        self._keys = self._load_keys_from_file()

        if self.__loggingFlags.show_keys:
            logger.info(json.dumps({"key_manager": {"key_cnt": len(self._keys),
                                                    "keys": list(self._keys.keys())}}))

    def _setup_directories_and_configs(self):

        self._create_directory_if_missing(self._secret_dir)

        keys_file = os.path.join(self._secret_dir, KEYS_FILE_SECRETS)
        self._initialize_file(keys_file, Keys.create_default_keys())

    @staticmethod
    def _create_directory_if_missing(path: str):
        """
        Ensures that the specified directory exists. If the directory does not exist,
        it will be created. If it already exists, no action will be taken.

        :param path: The directory path to ensure exists.
        :type path: Str
        :return: None
        """
        os.makedirs(path, exist_ok=True)

    def _initialize_file(self, filepath: str, default_content: str = ""):
        """
        Initializes a file at the specified path. If the file does not exist, it creates the
        file and writes the default content to it. Additionally, logs an informational
        message if initialization logging is enabled.

        :param filepath: The path of the file to initialize. Should include the full
            path along with the file name.
        :type filepath: str
        :param default_content: Content to be written into the file if it is being
            initialized. Defaults to an empty string.
        :type default_content: str
        :return: None
        """
        if not os.path.exists(filepath):  # pragma: no cover
            with open(filepath, "w") as file:
                file.write(default_content)
            if self.__loggingFlags.init_secrets:
                logger.info(json.dumps({"key_manager": {"init_secrets": f'{self._secret_dir}/{KEYS_FILE_SECRETS}'}}))

    @staticmethod
    def _load_keys_from_file() -> dict:
        """
        Loads keys from the default JSON file or uses default keys.
        """
        file_path = os.path.join(DEFAULT_SECRET_PATH, KEYS_FILE_SECRETS)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return json.loads(Keys.create_default_keys())

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


# Singleton instance of the KeyManager.
keyManager = KeyManager()
