## seCore

seCore is a high-performance and secure framework designed for building scalable applications. It provides developers with essential tools and libraries to streamline development, enhance security, and improve code maintainability. With support for modern programming paradigms, seCore aims to empower developers to focus on delivering robust solutions quickly.

Key Features:
- Security-First Approach: Built-in security measures to prevent common vulnerabilities.
- Scalability: Optimized to handle high loads and large-scale applications.
- Modularity: Highly modular architecture, allowing seamless integration and customization.
- Ease of Use: Developer-friendly APIs and comprehensive documentation.

Goals:
- Accelerate development time while maintaining high code quality.
- Provide a flexible foundation to meet diverse application needs.
- Ensure application security without compromising performance.

---

### Installation

To install `seCore`, use pip:

 ```bash
 pip install seCore
 ```

---

### **_CustomLogging:_**

```python
from seCore import logger

if __name__ == '__main__':
    """Logs a message using the specified log level."""
    logger.debug(f'Provides detailed information that’s valuable to you as a developer.')
    logger.info(f'Provides general information about what’s going on with your program.')
    logger.warning(f'Indicates that there’s something you should look into.')
    logger.error(f'Alerts you to an unexpected problem that’s occured in your program.')
    logger.critical(f'Tells you that a serious error has occurred and may have crashed your app.')
```

#### **_output_**

```shell
seCore | DEBUG    | Provides detailed information that’s valuable to you as a developer.
seCore | INFO     | Provides general information about what’s going on with your program.
seCore | WARNING  | Indicates that there’s something you should look into.
seCore | ERROR    | Alerts you to an unexpected problem that’s occured in your program.
seCore | CRITICAL | Tells you that a serious error has occurred and may have crashed your app.
```

---

### **_ConfigSettings:_**

```python
import json

from seCore import logger
from seCore import settings, settings_not_set
# from seCore.KeyManager import keyManager
# from seCore.KeyManagerVault import keyManager

# Constants
FORMAT_PADDING = 20
FORMAT_LOG_MESSAGE = '{setting:>{padding}}: {value}'
SEPARATOR_LINE = "-" * 160


def log_sorted_settings(system_settings):
    """Logs the key-value pairs of sorted settings."""
    for setting_name, setting_value in system_settings:
        logger.info(f'{setting_name:>{FORMAT_PADDING}}: {setting_value}')


def log_unset_settings(system_settings):
    """Logs unset settings with different log levels based on their required level."""
    for setting in system_settings:
        setting_value = json.loads(settings_not_set[setting])
        message = FORMAT_LOG_MESSAGE.format(setting=setting, value=setting_value, padding=FORMAT_PADDING)
        match setting_value["settingRequired"]["level"]:
            case "CRITICAL":
                logger.critical(message)
            case "ERROR":
                logger.error(message)
            case "WARNING":
                logger.warning(message)
            case _:
                logger.info(message)


if __name__ == '__main__':
    # Log sorted settings
    logger.info(SEPARATOR_LINE)
    sorted_settings = sorted(settings)
    log_sorted_settings(sorted_settings)

    # Log unset settings
    sorted_keys = sorted(settings_not_set)
    log_unset_settings(sorted_keys)
```

#### **_output_**

```shell
seCore | INFO     | ----------------------------------------------------------------------------------------------------------------------------------------------------------------
seCore | INFO     |          ENVIRONMENT: Local
seCore | INFO     |               FN_KEY: l911qB1keWvIykhvswzdKCQbr6h35Cabu8OeckOUbP4=
seCore | INFO     |          LOG_APPNAME: seCore
seCore | INFO     |           LOG_FORMAT: {extra[app]} | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>
seCore | INFO     |            LOG_LEVEL: DEBUG
seCore | INFO     |       MSSQL_DATABASE: {default_database}
seCore | INFO     |       MSSQL_HOSTNAME: {hostname}
seCore | INFO     |       MSSQL_PASSWORD: {password}
seCore | INFO     |           MSSQL_PORT: {port}
seCore | INFO     |          MSSQL_TRUST: {trust}
seCore | INFO     |       MSSQL_USERNAME: {username}
seCore | INFO     |         PROJECT_ROOT: /Users/rjd/GitHub/PyCharm/seCore
seCore | INFO     |            SETTING_1: value_1
seCore | INFO     |            SETTING_2: value_2
seCore | INFO     |         VERSION_CORE: 2025.6.0.rc1
```

---

### **_Encryption:_**

```python
from seCore import logger
from seCore import encryption

# Constants
FORMAT_PADDING = 20
WELCOME_MESSAGE = "Welcome to the seCore!"

def log_formatted(key, value):
    """Helper to standardize log output."""
    logger.info(f'{key:>{FORMAT_PADDING}}: {value}')

if __name__ == '__main__':
    encryption_service = encryption()

    # Log encryption key
    encryption_key = encryption_service.key.decode()
    log_formatted("Key", encryption_key)

    # Encrypt and log
    encrypted_message = encryption_service.encrypt(WELCOME_MESSAGE).decode()
    log_formatted("Encrypt", f"{WELCOME_MESSAGE} -> {encrypted_message}")

    # Decrypt and log
    decrypted_message = encryption_service.decrypt(encrypted_message)
    log_formatted("Decrypt", f"{encrypted_message} -> {decrypted_message}")
```

#### **_output_**
```shell
seCore | INFO     |                  Key: l911...UbP4=
seCore | INFO     |              Encrypt: Welcome to the seCore! -> gAAAAABna04F3P6S6eARPSEHgiCSPmixKnergtRf75SyDPVXd8tMOeBv5m02buuT3cP0-1MNDP_OY5pEEuFIRn9MJiePZgESBpKzS5HD_R-rVYb7g_cbnmQ=
seCore | INFO     |              Decrypt: gAAAAABna04F3P6S6eARPSEHgiCSPmixKnergtRf75SyDPVXd8tMOeBv5m02buuT3cP0-1MNDP_OY5pEEuFIRn9MJiePZgESBpKzS5HD_R-rVYb7g_cbnmQ= -> Welcome to the seCore!
```

---

### **_HttpRest:_**
```python
from seCore import logger
from seCore import HttpRest, HttpAction

# Constants
FORMAT_PADDING = 15
INDENTATION_LEVEL = 4
DEFAULT_HEADERS = {"Custom-Header": "value"}


def make_request_and_log(http_rest, http_action, http_url):
    """Make an HTTP request and log the result."""
    result, status_code = http_rest.http_request(http_action, http_url, DEFAULT_HEADERS)
    logger.info(f'{status_code} - {result}')


if __name__ == '__main__':
    rest_api = HttpRest()

    # List of requests to perform
    requests = [
        (HttpAction.GET, "https://httpbin.org/get"),
        (HttpAction.POST, "https://httpbin.org/post"),
        (HttpAction.PATCH, "https://httpbin.org/patch"),
    ]

    # Process request
    for action, url in requests:
        make_request_and_log(rest_api, action, url)
```

#### **_output_**

```shell
seCore | INFO     | 200 - {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Custom-Header": "value", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-676b6675-79001edf69c8245a0128421a"
  }, 
  "origin": "185.187.171.99", 
  "url": "https://httpbin.org/get"
}

seCore | INFO     | 200 - {
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "0", 
    "Custom-Header": "value", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-676b6675-58c7fe7b1527fa04719687ac"
  }, 
  "json": null, 
  "origin": "185.187.171.99", 
  "url": "https://httpbin.org/post"
}

seCore | INFO     | 200 - {
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "0", 
    "Custom-Header": "value", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-676b6675-3460a1cb5653a05d127a7b93"
  }, 
  "json": null, 
  "origin": "185.187.171.99", 
  "url": "https://httpbin.org/patch"
}
```
---

### **_PyVersions:_**

```python
import json
from seCore import logger
from seCore import PyVersions

# Constants
FORMAT_PADDING = 15
INDENTATION_LEVEL = 4

def log_formatted(key, value):
    """Standardize log output."""
    logger.info(f'{key:>{FORMAT_PADDING}}: {value}')

def log_json(key, data):
    """Log JSON formatted data."""
    formatted_data = json.dumps(data, indent=INDENTATION_LEVEL)
    log_formatted(key, formatted_data)

def log_py_versions(py_versions):
    """Log Python versions and releases."""
    log_json("pyVersions", py_versions.versions)
    log_json("pyReleases", py_versions.releases)

if __name__ == '__main__':
    try:
        py_versions = PyVersions()
        log_py_versions(py_versions)
    except Exception as e:
        logger.error(f'{"pyVersions":>{FORMAT_PADDING}}: {e}')
```

#### **_output_**

```shell
seCore | INFO     |      pyVersions: [
    {
        "version": "3.13",
        "status": "bugfix",
        "released": "2024-10-07",
        "eos": "2029-10"
    },
    {
        "version": "3.12",
        "status": "bugfix",
        "released": "2023-10-02",
        "eos": "2028-10"
    },
    {
        "version": "3.11",
        "status": "security",
        "released": "2022-10-24",
        "eos": "2027-10"
    }
]
seCore | INFO     |      pyReleases: [
    {
        "version": "3.13.3",
        "date": "April 8, 2025"
    },
    {
        "version": "3.12.10",
        "date": "April 8, 2025"
    },
    {
        "version": "3.11.12",
        "date": "April 8, 2025"
    }
]
```

### **_KeyManager:_**

```python
import json

from seCore import logger
from seCore.KeyManager import keyManager

# Constants
FORMAT_PADDING = 20
FORMAT_LOG_MESSAGE = '{setting:>{padding}}: {value}'
SEPARATOR_LINE = "-" * 160


logger.info(SEPARATOR_LINE)

# Get the first key
first_key = next(iter(keyManager.get_all_keys()))
bad_key = '8acc102b-bda2-43dc-919a-aeed7c9bb55f'
logger.info(f'{"first_key":>{FORMAT_PADDING}}: {first_key}')

# Validate key exists
validated_key = keyManager.validate_key(first_key)
logger.info(f'{"validated_key":>{FORMAT_PADDING}}: {first_key} - {validated_key}')

# Validate key doesn't exists
validated_key = keyManager.validate_key(bad_key)
logger.info(f'{"validated_key":>{FORMAT_PADDING}}: {bad_key} - {validated_key}')

# Get a list of keys masked
masked_keys = keyManager.get_masked_keys()
logger.info(f'{"masked_keys":>{FORMAT_PADDING}}: {json.dumps(masked_keys)}')

# Get a list of keys masked
all_keys = keyManager.get_all_keys()
logger.info(f'{"masked_keys":>{FORMAT_PADDING}}: {json.dumps(all_keys)}')


# Validate key exists and has the appropriate role
oValidRoles = ["User", "3rd Party"]
oIsValid = keyManager.validate_role(first_key, oValidRoles)
logger.info(f'{"validate_role":>{FORMAT_PADDING}}: {oIsValid} - {oValidRoles} ')
```

#### **_output_**

```shell
seCore | INFO     | ----------------------------------------------------------------------------------------------------------------------------------------------------------------
seCore | INFO     | {"key_manager": {"key_cnt": 3, "keys": ["8acc102b-bda2-43dc-919a-aeed7c9bb55e", "36d9572b-deac-466b-b7e0-bc9c7cae98d6", "0ff54cdd-58ec-4945-84eb-b4894285e59f"]}}
seCore | INFO     | ----------------------------------------------------------------------------------------------------------------------------------------------------------------
seCore | INFO     |            first_key: 8acc102b-bda2-43dc-919a-aeed7c9bb55e
seCore | INFO     |        validated_key: 8acc102b-bda2-43dc-919a-aeed7c9bb55e - True
seCore | INFO     |        validated_key: 8acc102b-bda2-43dc-919a-aeed7c9bb55f - False
seCore | INFO     |          masked_keys: {"aeed7c9bb55e": {"Key": "aeed7c9bb55e", "Created": "2025-04-27", "Expires": "2026-04-27", "Description": "SuperAdmin key for application: Create, Update, Delete API keys", "Roles": ["User", "Administrator", "SuperAdmin"]}, "bc9c7cae98d6": {"Key": "bc9c7cae98d6", "Created": "2025-04-27", "Expires": "2026-04-27", "Description": "Admin key for application: Create, Update API keys", "Roles": ["User", "Administrator"]}, "b4894285e59f": {"Key": "b4894285e59f", "Created": "2025-04-27", "Expires": "2026-04-27", "Description": "User key for application", "Roles": ["User"]}}
seCore | INFO     |          masked_keys: {"8acc102b-bda2-43dc-919a-aeed7c9bb55e": {"Key": "aeed7c9bb55e", "Created": "2025-04-27", "Expires": "2026-04-27", "Description": "SuperAdmin key for application: Create, Update, Delete API keys", "Roles": ["User", "Administrator", "SuperAdmin"]}, "36d9572b-deac-466b-b7e0-bc9c7cae98d6": {"Key": "bc9c7cae98d6", "Created": "2025-04-27", "Expires": "2026-04-27", "Description": "Admin key for application: Create, Update API keys", "Roles": ["User", "Administrator"]}, "0ff54cdd-58ec-4945-84eb-b4894285e59f": {"Key": "b4894285e59f", "Created": "2025-04-27", "Expires": "2026-04-27", "Description": "User key for application", "Roles": ["User"]}}
seCore | INFO     |        validate_role: True - ['User', '3rd Party'] 
```

### **_KeyManagerVault:_**
```python
import json

from seCore import logger
from seCore.KeyManagerVault import keyManager

# Constants
FORMAT_PADDING = 20
FORMAT_LOG_MESSAGE = '{setting:>{padding}}: {value}'
SEPARATOR_LINE = "-" * 160


logger.info(SEPARATOR_LINE)

# Get the first key
first_key = next(iter(keyManager.get_all_keys()))
bad_key = '8acc102b-bda2-43dc-919a-aeed7c9bb55f'
logger.info(f'{"first_key":>{FORMAT_PADDING}}: {first_key}')

# Validate key exists
validated_key = keyManager.validate_key(first_key)
logger.info(f'{"validated_key":>{FORMAT_PADDING}}: {first_key} - {validated_key}')

# Validate key doesn't exists
validated_key = keyManager.validate_key(bad_key)
logger.info(f'{"validated_key":>{FORMAT_PADDING}}: {bad_key} - {validated_key}')

# Get a list of keys masked
masked_keys = keyManager.get_masked_keys()
logger.info(f'{"masked_keys":>{FORMAT_PADDING}}: {json.dumps(masked_keys)}')

# Get a list of keys masked
all_keys = keyManager.get_all_keys()
logger.info(f'{"masked_keys":>{FORMAT_PADDING}}: {json.dumps(all_keys)}')


# Validate key exists and has the appropriate role
oValidRoles = ["User", "3rd Party"]
oIsValid = keyManager.validate_role(first_key, oValidRoles)
logger.info(f'{"validate_role":>{FORMAT_PADDING}}: {oIsValid} - {oValidRoles} ')
```

#### **_output_**

```shell
seCore | INFO     | ----------------------------------------------------------------------------------------------------------------------------------------------------------------
seCore | INFO     | {"key_manager_vault": {"secrets_folder": "seCore/dev/keys"}}
seCore | INFO     | {"key_manager_vault": {"secrets": {"project": "seCore/dev/keys", "key": "km", "value": "gAAAAABm6OQGWeo1KJs4zyNNDIpUpkSOvSgvLKAnt0hsqXJ6WzuZbKFNVEEGFHi6xJNKRrCH3W2qZuwn7vRt3dKymTtR9g67Y4RJrQ1d4l_UfExmfN7dovZC53IzxPJhj6zU-42AlOPdFZaKEnD6cs0D7hEKxRcnWWV-PH0ab63KcciLYZZb_jp-zu2cN8VPvEdIHMG-cVYErTtEUx1h9QyFBXEhlXwY2iiiPbv46bvwbScAj8TlvejQLN4LYioB8ygOgUOwQ4GydJ_4F1tT8EGmvkFzcNfE7q8R0cRgIBmgUh3rN0bCHJ9PeNVYNSxn7_iZzae9v2RP6CeiKkXmVMz4tYb-_EpeFhJmDb2G1yCPKACtkD5EJTnQbCZ3qmysTL4_gc2eHZZGTf9I9kX1feqJwOi3LHrtNTC1FUP5D2LF-RayiHhNxojda4MYA0jmTOvg3uzKpKY0PNPp3NY8kdVJWMTVJW8_8JUzD3skcMbAz5tAxKzp0i6qKLTcbcjc3IFb0-KQs-T_NqzZTlvAhsvSiVp55igzuAzGm5AQ5x7vbtgMtUjBpqFeJ620uwflemBbgmul1pN0lPbfFi6ix8kKKit0_GHouydElWGY0aMuiPiRLwro2gnftjxitnceRnJgHdLOZmEY3pA-JfJlV4OE3K03gMIM3pyHZlCTAmPCCyZTizMc3V97_dOuYxZYKZmYEnsyAM0pCsNR1l_IzettAuEUIb3sbnX9s5hj2J1tHa1gq9H0bE8JUl5MRcI0WG_uDuB8NwGFbuZrnJcaetivT9bKWj3sqW9W6S4xmJbUEhIY-3bmjP8dRlMN1zZSoedOaXw9N2vaPkUMxnjvP1NtHwUfyEMwfDGacKSvhZt0s2EDLGq2KDnDf9aVQ2A6t38ksa5crP5VkH4TzeN5CtC2tBJ6He8lryqofj_AkCk4q8ZxtAhoC9D-T5d_exYLGMquT2qk08fXpuPCO9PcTrYv3PYM7ln61kWx0jNVVP5c92RSfb5UIi90VCt-m_haF5QU6g_pXcpYC-Ay-Rog8ydUcNG87V3gJpNBEXXhtq_hQ5fS6K7Pr_HayW6sQC7ZjZRTlMstglLdCZzl9DJcbLKyJa_Z--Oz0oZcRdRGEn_KDPiRLFjqf56InxYKbMD5qFkHXBu5WSVyjVwo5FosqyCS5vk41m759UmNJtnEGLV80ngLJeUTeBHso9paR5bUIy6SUklkx7rniY0ed68cQD93UqKcN1tPv-5QASnGLZNzE4nh-0Sag90kCMNGiqqqj_X37pU9obgpVIDtr-SakUENxcKT6tHfkgoh3FTKP2avL4zWg2IYdjeueZE9MP_A5aIjioxqJ9gfTfw3wxnDR9tYvEFK-oaTPI5y8WgUW6SXuSSS2ckdhU4AF6Sc2FGVknaPU2VHy1gz3eKsGNbUkRcBE8hPMPNV61-miG68aDvoqzGKJ0BOZt9Qu8li5xEIm-NBWvhd4J2dXIuIDD6gpUIMYcaNvuXmXXiOevT6_HEiCNpOnAZ4FqNjgPSnsTMzScf9UszAJOQKweI-aqDOrDqIm-o2JxHVlQOV_qp5G6DVhHdGmgvSeYiEphM_YLqOZu2-idDeRpNyTAalcrxycSbaMKKWAZRq178ruV-N5AVfM76xAVc6deQmyJ59c6Rg4DS14OdVWGqPq_znuAEwO6dAoWTqaABiTjiiLY3ms34t9dbJz6YlHfeQ4ay_QmUjBTAm9p0S_uSzHAQ8fh7yXytP68psGzYfFGYy2hT6mf06EEhULjrhIbR1phMIg-c6qeC5xbpVmnp5SY2Q7Ick_103BpGeOllDRg=="}}}
seCore | INFO     | {"key_manager_vault": {"key_cnt": 5, "keys": ["6cdf31d0-367a-4bb0-91e4-244c9d7157dc", "dd603c0f-6701-4e69-b410-8e41e235f427", "cd2180a9-4539-4745-9c22-736171d075cc", "3aa0fc14-d1c0-4135-b314-75b18237db38", "d2d2f21a-fd5c-4093-b552-88583675fa9c"]}}
seCore | INFO     | ----------------------------------------------------------------------------------------------------------------------------------------------------------------
seCore | INFO     |            first_key: 6cdf31d0-367a-4bb0-91e4-244c9d7157dc
seCore | INFO     |        validated_key: 6cdf31d0-367a-4bb0-91e4-244c9d7157dc - True
seCore | INFO     |        validated_key: 8acc102b-bda2-43dc-919a-aeed7c9bb55f - False
seCore | INFO     |          masked_keys: {"244c9d7157dc": {"Key": "244c9d7157dc", "Owner": "x2rw3", "Project": "project/{env}/admin_edsap", "Roles": ["User", "Administrator"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "8e41e235f427": {"Key": "8e41e235f427", "Owner": "x2rw3", "Project": "project/{env}/superadmin_edsap", "Roles": ["User", "Administrator", "SuperAdmin"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "736171d075cc": {"Key": "736171d075cc", "Owner": "x2rw3", "Project": "project/{env}/john_api_testing", "Roles": ["User"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "75b18237db38": {"Key": "75b18237db38", "Owner": "x2rw3", "Project": "project/{env}/crms", "Roles": ["User"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "88583675fa9c": {"Key": "88583675fa9c", "Owner": "k4mq2", "Project": "project/{env}/my_cdsw_dev_project", "Roles": ["User"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}}
seCore | INFO     |          masked_keys: {"6cdf31d0-367a-4bb0-91e4-244c9d7157dc": {"Key": "244c9d7157dc", "Owner": "x2rw3", "Project": "project/{env}/admin_edsap", "Roles": ["User", "Administrator"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "dd603c0f-6701-4e69-b410-8e41e235f427": {"Key": "8e41e235f427", "Owner": "x2rw3", "Project": "project/{env}/superadmin_edsap", "Roles": ["User", "Administrator", "SuperAdmin"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "cd2180a9-4539-4745-9c22-736171d075cc": {"Key": "736171d075cc", "Owner": "x2rw3", "Project": "project/{env}/john_api_testing", "Roles": ["User"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "3aa0fc14-d1c0-4135-b314-75b18237db38": {"Key": "75b18237db38", "Owner": "x2rw3", "Project": "project/{env}/crms", "Roles": ["User"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}, "d2d2f21a-fd5c-4093-b552-88583675fa9c": {"Key": "88583675fa9c", "Owner": "k4mq2", "Project": "project/{env}/my_cdsw_dev_project", "Roles": ["User"], "Created": "2024-09-16", "Expires": "2025-09-16", "CI": null}}
seCore | INFO     |        validate_role: True - ['User', '3rd Party'] 
```