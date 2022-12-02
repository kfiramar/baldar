from typing import List
from app.models.requirement import Requirement
from app.models.package_types import PackageType
import os 


def generate_package_list(file_path: str, package_type: PackageType) -> List[Requirement]:
    requirement_list: List[Requirement] = []
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            package_name = line.rstrip('\n')
            if package_name != '':
                requirement_list.append(Requirement(
                    package_name=package_name, package_type=package_type))
    return requirement_list
