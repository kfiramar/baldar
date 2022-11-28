from typing import List
from requests import get

from app.models.package import Package

from app.core.config import PYTHON_PACKAGE_NAME

from app.services import get_latest_db_version, is_newer_version, sort_versions_list

formatted_pypi_json_url = "https://pypi.org/pypi/{}/json"


def get_all_releases(package_name: str) -> list:
    package_json = get(formatted_pypi_json_url.format(package_name)).json()
    releases = package_json["releases"]
    return releases


def generate_releases_to_download(package_name: str) -> list:
    download_list = []
    releases = get_all_releases(package_name)
    releases_versions = list(releases.keys())
    sorted_versions = sort_versions_list(releases_versions)
    latest_version = sorted_versions[len(sorted_versions) - 1]
    latest_db_version = get_latest_db_version(
        package_name, PYTHON_PACKAGE_NAME)

    if(not is_newer_version(latest_version, latest_db_version)):
        return download_list

    for release in reversed(sorted_versions):
        if(not is_newer_version(release, latest_db_version)):
            break
        for file in releases[release]:
            file["version"] = release
            download_list.append(file)

    return download_list


def generate_python_download_list(package_name: str) -> List[Package]:
    download_list: List[Package] = []
    releases: list = generate_releases_to_download(package_name)

    for release in releases:
        download_list.append(
            Package(package_name=package_name,
                    file_name=release["filename"],
                    download_url=release["url"],
                    package_type=PYTHON_PACKAGE_NAME,
                    version=release["version"]))

    return download_list
