from packaging import version
from functools import cmp_to_key
from app.core.config import BASE_VERSION


def get_latest_version_from_dataset(versions: list) -> str:
    latest_version = BASE_VERSION
    for version_value in versions:
        string_version = str(version_value)
        string_version = string_version[2:string_version.rindex("'")]
        if compare(string_version, latest_version):
            latest_version = string_version

    return latest_version


def is_newer_version(first_version: str, second_version: str) -> bool:
    return version.parse(first_version) > version.parse(second_version)


def compare(first_version: str, second_version: str) -> bool:
    if version.parse(first_version) > version.parse(second_version):
        return 1
    if version.parse(first_version) < version.parse(second_version):
        return -1
    return 0


def sort_versions_list(versions: list) -> list:
    return sorted(versions, key=cmp_to_key(compare))


def get_latest_version(versions: list) -> str:
    return sort_versions_list(versions)[len(versions) - 1]
