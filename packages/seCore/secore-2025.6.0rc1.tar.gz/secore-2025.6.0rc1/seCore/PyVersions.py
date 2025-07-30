from bs4 import BeautifulSoup
from .HttpRest import HttpRest, HttpAction


def compare_versions(v1: str, v2: str) -> bool:
    """
    Compares two version strings to determine if the first is greater than or equal to the second.
    The version strings are formatted as dot-separated integers (e.g., '1.0.0').

    :param v1: The first version string to compare.
    :type v1: str
    :param v2: The second version string to compare.
    :type v2: str
    :return: True if the first version is greater than or equal to the second,
        otherwise False.
    :rtype: bool
    """
    _v1 = tuple(map(int, v1.split(".")))
    _v2 = tuple(map(int, v2.split(".")))
    return _v1 >= _v2


class PyVersions:
    """Manages fetching, parsing, and processing Python version and release data.

    This class is designed to interact with a specified URL to retrieve Python version
    statistics. It identifies supported versions and processes release data as per
    defined thresholds. The class can be used to access current Python versions and
    release information in an organized manner.

    :ivar SUPPORTED_VERSIONS: A list of Python versions actively supported by this
        implementation.
    :type SUPPORTED_VERSIONS: list of str
    :ivar RELEASE_THRESHOLD: The minimum version considered for identifying releases,
        expressed in the conventional versioning format.
    :type RELEASE_THRESHOLD: str
    """
    SUPPORTED_VERSIONS = ["3.13", "3.12", "3.11"]
    RELEASE_THRESHOLD = "3.11.10"

    def __init__(self, url: str = 'https://www.python.org/downloads/'):
        """
        Represents an object for managing and parsing Python download URLs,
        maintaining information about Python versions and releases.

        :ivar __url: The URL to be used for retrieving Python download information.
        :ivar __versions: A list that stores the version information of Python releases.
        :ivar __releases: A list that stores the release data of Python versions.

        :param url: The URL passed during initialization, defaulting to
                    'https://www.python.org/downloads/'.
        :type url: str
        """
        self.__url = url
        self.__versions = []
        self.__releases = []
        self.stats_update()

    def stats_update(self) -> None:
        """
        Updates the internal statistics of the object by fetching the latest data
        from a specified URL and parsing the data as an HTML response. The method
        throws a 404 error if the data is not available or if the HTTP request does
        not return a valid response.

        This method is designed to handle HTTP GET requests, parse the HTML data
        into structured information and update relevant internal attributes like
        versions and releases.

        :raises NotFound: if the HTTP status code is not 200 or the response is empty.
        """
        rest_api = HttpRest()
        response, status = rest_api.http_request(HttpAction.GET, self.__url, http_verify=True)
        # Throw 404 if the response is empty or None
        if status != 200 or not response:
            # raise NotFound(description=f"No data found at URL: {self.__url}")
            response = ""
        soup = BeautifulSoup(response, 'html.parser')
        parsed_data = soup.find_all('ol')
        self.__versions, self.__releases = self.parse_python_data(parsed_data)

    def parse_python_data(self, data) -> (list, list):
        """
        Parses a dataset to extract Python version and release information by
        analyzing HTML elements. Filters the versions and releases based
        on predefined criteria, including support status and version thresholds,
        and organizes the information into two categories: supported versions
        and filtered release details. Ensures releases are sorted in descending
        order based on their version.

        :param data: HTML data structure containing Python release information.
        :type data: list
        :return: A tuple containing a list of dictionaries for supported Python
            versions and a list of dictionaries for filtered and sorted releases.
        :rtype: tuple
        """
        python_versions = []
        python_releases = []

        for row in data:
            for o in row.find_all('li'):
                if release_version := o.find(class_='release-version'):
                    version_info = {
                        "version": release_version.text,
                        "status": o.find(class_='release-status').text,
                        "released": o.find(class_='release-start').text,
                        "eos": o.find(class_='release-end').text,
                    }
                    if version_info['version'] in self.SUPPORTED_VERSIONS:
                        python_versions.append(version_info)

                if release_number := o.find(class_='release-number'):
                    release_info = {
                        "version": release_number.text.replace("Python ", ""),
                        "date": o.find(class_='release-date').text
                    }
                    if compare_versions(release_info["version"], self.RELEASE_THRESHOLD):
                        python_releases.append(release_info)
        python_releases_sorted = sorted(
            python_releases,
            key=lambda x: (
                tuple(map(int, x["version"].split("."))),  # Convert version string into tuple
            ),
            reverse=True
        )
        return python_versions, python_releases_sorted

    @property
    def versions(self) -> list:
        """
        Retrieves a list of available versions.

        This property fetches the versions associated with the object
        in the form of a list. It does not take any parameters and
        only returns the versions stored internally.

        :return: A list of versions stored in the object.
        :rtype: list
        """
        return self.__versions

    @property
    def releases(self) -> list:
        """
        Property to access the private attribute __releases.

        This property provides a way to retrieve the data stored in the
        ``__releases`` attribute, ensuring encapsulation and controlled
        access through the getter.

        :return: The list of releases.
        :rtype: list
        """
        return self.__releases
