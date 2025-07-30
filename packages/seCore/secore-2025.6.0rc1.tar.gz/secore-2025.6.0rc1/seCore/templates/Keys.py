import json
import uuid
from datetime import date, timedelta

# Constants
DEFAULT_EXPIRY_DAYS = 365


def generate_key_entry(key: str, description: str, roles: list):
    """
    Generate a dictionary representation of a key entry, including metadata about
    its creation time, expiration date, associated roles, and description.

    This method creates a record containing a key, the date it was created, its
    expiration date based on a default expiry period, a textual description, and the
    roles assigned to this key. This data structure is typically used to manage
    access control or resource permissions.

    :param key: The unique identifier for the key entry.
    :type key: str
    :param description: The textual description associated with the key entry.
    :type description: str
    :param roles: The list of roles or permissions assigned to the key entry.
    :type roles: list[str]

    :return: A dictionary containing metadata for the key entry, including its
             unique identifier, creation date, expiration date, description, and roles.
    :rtype: dict
    """
    return {
        "Key": key,
        "Created": str(date.today()),
        "Expires": str(date.today() + timedelta(days=DEFAULT_EXPIRY_DAYS)),
        "Description": description,
        "Roles": roles,
    }


def create_default_keys():
    """
    Creates default API keys for a web application and returns them serialized as a JSON
    string. The keys generated include a SuperAdmin key, an Admin key, and a User key.
    Each key is associated with a description and corresponding roles.

    :raises ValueError: If there is an issue, generate the key entries.

    :return: A JSON string containing the default API keys with associated descriptions
        and roles. Each key entry consists of the following:
        - A unique identifier as the key.
        - A description of the key's intended use.
        - A list of roles that the key corresponds to.
    :rtype: str
    """
    super_admin_key = str(uuid.uuid4())
    admin_key = str(uuid.uuid4())
    user_key = str(uuid.uuid4())

    DEFAULT_KEYS = {
        super_admin_key: generate_key_entry(
            super_admin_key,
            "SuperAdmin key for application: Create, Update, Delete API keys",
            ["User", "Administrator", "SuperAdmin"]
        ),
        admin_key: generate_key_entry(
            admin_key,
            "Admin key for application: Create, Update API keys",
            ["User", "Administrator"]
        ),
        user_key: generate_key_entry(
            user_key,
            "User key for application",
            ["User"]
        ),
    }

    return json.dumps(DEFAULT_KEYS, indent=4)
