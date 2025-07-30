import os
import re
import json
import yaml

from typing import Any
from string import Template
from cryptography.fernet import Fernet
from pydantic.v1 import BaseSettings, Extra
from pydantic.v1.env_settings import SettingsSourceCallable
from .templates import ConfigSettings
from .ProjectRoot import project_root
from .__about__ import __version__

# Constants
ENV_FILE_SETTINGS = ".env.settings"
ENV_FILE_SECRETS = ".env.secrets"
DEFAULT_CONFIG_PATH = os.path.join(project_root(), "app")
DEFAULT_SECRET_PATH = os.path.join(DEFAULT_CONFIG_PATH, "secrets")
VALIDATION_RULES = {
    "log_level": "ERROR",
    "log_appname": "ERROR",
}

# Constant for an encryption key
FN_KEY = "Z46GMhKyW9rHU8c2T0296Zgr153HSIPD5mo3-faiHdQ="

CONFIG_KEY_PATTERN = re.compile(r"^[^#].+=[\"|\']*.*[\"|\']*$")  # Regex to match key-value pairs


class ConfigManager:
    """
    Manages configuration settings, ensuring directories and files are set up properly while
    validating and loading configuration data. Designed to handle and validate application
    settings and secrets stored in files.

    This class provides methods for loading configurations from files, managing directories,
    and validating configurations based on predefined rules. It ensures that the required
    directory structures and default configurations are initialized, with support for
    overwriting these defaults by loading external configuration files.

    :ivar parameters: Stores key-value pairs loaded from configuration files.
    :type parameters: dict
    :ivar validation_rules: Defines required configuration keys and their validation levels.
    :type validation_rules: dict
    :ivar errors: Tracks any errors or missing required keys during validation.
    :type errors: dict
    :ivar error_occurred: Indicates whether an error state exists in the configuration.
    :type error_occurred: bool
    :ivar config_dir: Path to the directory where configuration files are stored.
    :type config_dir: str
    :ivar secret_dir: Path to the directory where secret files are stored.
    :type secret_dir: str
    """

    def __init__(self, validation_rules=None, config_path=DEFAULT_CONFIG_PATH, secret_path=DEFAULT_SECRET_PATH):
        self.parameters: dict[str, str] = {}
        self.validation_rules: dict[str, str] = validation_rules or {}
        self.errors: dict[str, str] = {}
        self.error_occurred: bool = False
        self.config_dir: str = config_path
        self.secret_dir: str = secret_path

        self._setup_directories_and_configs()

    def _setup_directories_and_configs(self):
        """
        Sets up the necessary directories and configuration files required for the application
        to run. This includes ensuring that the directories exist, initializing necessary
        configuration files with default values if they do not exist, and loading configurations
        from these files.

        Supported directories include the configuration directory and the secret directory.

        The method also ensures environmental and secret configuration files exist by default
        and reads configuration values from them.

        :raises FileNotFoundError: If a necessary directory or file cannot be found.
        """
        self._ensure_directory(self.config_dir)
        self._ensure_directory(self.secret_dir)
        # self._initialize_file(os.path.join(self.config_dir, ENV_FILE_SETTINGS), Template(ConfigSettings.DEFAULT_ENV_SETTINGS).safe_substitute(fn_key=Fernet.generate_key().decode()))
        self._initialize_file(os.path.join(self.config_dir, ENV_FILE_SETTINGS), Template(ConfigSettings.DEFAULT_ENV_SETTINGS).safe_substitute(fn_key='l911qB1keWvIykhvswzdKCQbr6h35Cabu8OeckOUbP4='))
        self.load_configuration(os.path.join(self.config_dir, ENV_FILE_SETTINGS))

        secrets_file = os.path.join(self.secret_dir, ENV_FILE_SECRETS)
        self._initialize_file(secrets_file, ConfigSettings.DEFAULT_ENV_SECRET_SETTINGS)

        if os.path.exists(secrets_file):
            self.load_configuration(secrets_file)

        # keys_file = os.path.join(self.secret_dir, KEYS_FILE_SECRETS)
        # self._initialize_file(keys_file, Keys.create_default_keys())

    @staticmethod
    def _ensure_directory(path: str):
        """
        Ensures that the specified directory exists. If the directory does not exist,
        it will be created. If it already exists, no action will be taken.

        :param path: The directory path to ensure exists.
        :type path: str
        :return: None
        """
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def _initialize_file(filepath: str, default_content: str = ""):
        """
        Initializes a file at the specified filepath. If the file does not already exist,
        it creates the file and optionally writes the provided default content to it.

        :param filepath: The path to the file to be initialized.
        :type filepath: str
        :param default_content: The content to write to the file if it is created.
                                Defaults to an empty string.
        :type default_content: str, optional
        """
        if not os.path.exists(filepath):
            with open(filepath, "w") as file:
                file.write(default_content)

    def load_configuration(self, filename: str):
        """
        Loads configuration parameters from a specified file. The function reads the file line-by-line,
        searching for configuration keys matching a predefined pattern. If a valid key-value pair is
        found, it is parsed and added to the `parameters` dictionary of the instance. This allows dynamic
        configuration loading from external files.

        :param filename: The path to the configuration file to read.
        :type filename: str
        :return: None
        """
        with open(filename, "r") as file:
            for line in file:
                if CONFIG_KEY_PATTERN.search(line):
                    key, value = self._parse_line(line)
                    self.parameters[key] = value

    @staticmethod
    def _parse_line(line: str) -> tuple[str, str]:
        """
        Parses a configuration line, extracting a key-value pair by removing comments and cleaning whitespace and
        quotes. The method ensures that the key is converted to uppercase for uniformity.

        :param line: A string containing a configuration line, which may contain a key-value pair and comments.
        :type line: str

        :return: A tuple containing the extracted key (in uppercase) and cleaned value.
        :rtype: tuple[str, str]
        """
        key_value = line.split("#", 1)[0].strip()  # Remove comments
        key, value = key_value.split("=", 1)
        return key.strip().upper(), value.strip().strip('"\'')  # Cleanup quotes

    def validate_configuration(self):
        """
        Validates the configuration parameters against the defined validation rules and
        determines whether any errors have occurred. Missing parameters are identified,
        and detailed error messages are generated for each missing parameter according
        to its required validation level.

        :raises KeyError: if required, parameters are not uppercased in the validation rules.

        :return: None
        """
        self.errors = {
            param.upper(): json.dumps({
                "settingRequired": {
                    "details": f"'{param}' is missing.",
                    "level": level,
                }
            })
            for param, level in self.validation_rules.items()
            if param.upper() not in self.parameters
        }
        self.error_occurred = any("ERROR" in error.upper() for error in self.errors.values())


class Settings(BaseSettings):
    """
    Manages application settings and configurations, enabling the retrieval and
    management of environment variables and project-specific attributes. This
    class serves as a centralized configuration handler to ensure consistent
    and systematic access to application settings.
    """
    VERSION_CORE: str = __version__
    FN_KEY: str = os.getenv("FN_KEY", FN_KEY)
    PROJECT_ROOT: str = f'{project_root()}'

    class Config:
        extra = Extra.allow
        env_prefix = "medium_"

        @classmethod
        def customise_sources(
                cls,
                init_settings: SettingsSourceCallable,
                env_settings: SettingsSourceCallable,
                file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            """
            Customizes and overrides the default sequence of settings sources for loading
            configuration values. Takes three callable sources as input—`init_settings`,
            `env_settings`, and `file_secret_settings`—and allows users to specify their
            custom sequence of sources to be applied.

            :param init_settings: Initial callable source for fetching configuration values.
            :param env_settings: Callable source for fetching environment variable-based
                                 configuration values.
            :param file_secret_settings: Callable source for fetching configuration values
                                         from secret files.
            :return: A tuple of callable sources representing the customized sequence of
                     settings to be used.
            """
            return init_settings, env_settings, env_secrets_settings


def env_secrets_settings(_settings: BaseSettings) -> dict[str, Any]:
    """
    Processes the given BaseSettings object to extract environment-specific
    secret settings and returns them as a dictionary.

    This function uses a YAML-safe loader to transform configuration
    parameters managed by the config_manager into a dictionary of secrets,
    specifically designed for applications with environment-specific settings.

    :param _settings: An instance of BaseSettings that provides application
        configuration settings.
    :type _settings: BaseSettings
    :return: A dictionary containing the parsed environment-specific
        secret settings.
    :rtype: dict[str, Any]
    """
    return yaml.safe_load(str(config_manager.parameters))


# Initialize and validate configuration
config_manager = ConfigManager(VALIDATION_RULES)
config_manager.validate_configuration()

# Check for any unset settings
settings_not_set = config_manager.errors
settings = Settings()
