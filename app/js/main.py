import re
from requests import get
from typing import List
from app.core.config import NPM_PACKAGE_NAME
from app.services import get_latest_db_version, is_newer_version, sort_versions_list
from app.models.package import Package

formatted_npm_json_url = "https://registry.npmjs.org/{}"


def get_dep(package_name: str, visited: dict):
    if package_name in visited:
        return
    else:
        visited[package_name] = 1

    inner_dict = {}
    data = get(formatted_npm_json_url.format(package_name))
    json = data.json()
    version = list(json["versions"].keys())[-1]

    for value in json["versions"].values():
        try:
            for dependency in json["versions"][version]['dependencies'].keys():
                inner_dict[dependency] = 1
        except:
            pass

    for dep in inner_dict.keys():
        get_dep(dep, visited)

def clean_file(file_path: str):
    f = open(file_path, 'r+')
    f.truncate(0)

def get_all_dependencies(packages_file_path: str , dependencies_file_path: str,  all_packages: dict):
    with open(packages_file_path) as file:
        for line in file:
            if line.rstrip() != '' :
                get_dep(line.rstrip(), all_packages)
    with open(dependencies_file_path, "a") as file:
        for package in all_packages.keys():
            file.write(package+ "\n")


def get_all_releases(package_name: str):
    release_dict: dict = {}
    data = get(formatted_npm_json_url.format(package_name))
    json = data.json()

    for key in json['versions'].keys():
        if not (re.search('[a-zA-Z]', key)):
            release_dict[key] = json['versions'][key]

    return release_dict


def generate_releases_to_download(package_name: str) -> list:
    download_list = []
    releases = get_all_releases(package_name)
    releases_versions = list(releases.keys())
    sorted_versions = sort_versions_list(releases_versions)
    latest_version = sorted_versions[len(sorted_versions) - 1]
    latest_db_version = get_latest_db_version(
        package_name, NPM_PACKAGE_NAME)

    if(not is_newer_version(latest_version, latest_db_version)):
        return download_list

    for release in reversed(sorted_versions):
        if(not is_newer_version(release, latest_db_version)):
            break
        download_list.append(releases[release])

    return download_list


def generate_npm_download_list(package_name: str) -> List[Package]:
    download_list: List[Package] = []
    releases: list = generate_releases_to_download(package_name)

    for release in releases:
        download_list.append(
            Package(package_name=package_name,
                    file_name=release['dist']['tarball'][release['dist']['tarball'].rfind(
                        '/') + 1:len(release['dist']['tarball'])],
                    download_url=release['dist']['tarball'],
                    package_type=NPM_PACKAGE_NAME,
                    version=release["version"]))

    return download_list
