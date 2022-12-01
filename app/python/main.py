from typing import List
from requests import get
from datetime import datetime

from app.models.package import Package

from app.core.config import PYTHON_PACKAGE_NAME

from app.services import get_latest_db_version, is_newer_version, sort_versions_list

formatted_pypi_json_url = "https://pypi.org/pypi/{}/json"

LAST_UPDATED_DATE = datetime.strptime("2022-09-15T00:00:00", "%Y-%m-%dT%H:%M:%S")

def get_all_releases(package_name: str) -> list:
    package_json = get(formatted_pypi_json_url.format(package_name)).json()
    releases = package_json["releases"]
    return releases

def cast_releases_to_dates(releases):
    releases_dates = []
    for release in (releases.values()):
        if release:
            releases_dates.append(get_date_from_release(release))
    releases_dates.sort()
    return releases_dates

def date_to_version(date, releases):
    for release in releases:
        if get_date_from_release(releases[release]) == date:
            return release
    raise Exception("Weird - ERROR")



def get_date_from_release(release):
    try:
        return (datetime.strptime(release[1]['upload_time'], "%Y-%m-%dT%H:%M:%S"))
    except IndexError:
        return (datetime.strptime(release[0]['upload_time'], "%Y-%m-%dT%H:%M:%S"))

def generate_releases_to_download_by_dates(package_name: str) -> list:
    download_list = []
    releases = get_all_releases(package_name)
    releases_dates = cast_releases_to_dates(releases)
    latest_date = releases_dates[len(releases_dates) - 1]
    if (not LAST_UPDATED_DATE < latest_date):
        return download_list
    for date in releases_dates:
        if (not LAST_UPDATED_DATE < latest_date):
            break
        for file in releases[date_to_version(date, releases)]:
            file["version"] = release
            download_list.append(file)

    return download_list

def generate_releases_to_download(package_name: str) -> list:
    download_list = []
    releases = get_all_releases(package_name)
    releases_versions = list(releases.keys())
    sorted_versions = sort_versions_list(releases_versions)
    latest_version = sorted_versions[len(sorted_versions) - 1]
    latest_db_version = get_latest_db_version(
        package_name, PYTHON_PACKAGE_NAME)
# change to is_newer_release_date
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
    releases: list = generate_releases_to_download_by_dates(package_name)

    for release in releases:
        download_list.append(
            Package(package_name=package_name,
                    file_name=release["filename"],
                    download_url=release["url"],
                    package_type=PYTHON_PACKAGE_NAME,
                    version=release["version"]))

    return download_list
    
