import queue
import os.path
from typing import List
from app.core.config import NPM_PACKAGE_NAME, NPM_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH, NPM_PACKAGES_TO_DOWNLOAD_RELATIVE_PATH, PYPI_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH, PYTHON_PACKAGE_NAME
from app.models import RegisterWorker, DownloaderWorker
from app.models.package_types import PackageType
from app.models.requirement import Requirement
from app.services.csv_handler import get_top_packages
from app.js.main import get_all_dependencies
from app.js.main import clean_file
from time import sleep
from app.services.file_handler import generate_package_list
from app.python.main import generate_releases_to_download_by_dates







if __name__ == "__main__":
    requirement_list: List[Requirement] = []
    download_queue = queue.Queue()
    packages_queue = queue.Queue()


    # Checks if the npm full packages list needs to be updated
    # if (not os.path.isfile(NPM_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH)) or \
            # (os.path.getmtime(NPM_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH) <= os.path.getmtime(NPM_PACKAGES_TO_DOWNLOAD_RELATIVE_PATH)):
        # clean_file(NPM_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH)
        # get_all_dependencies(NPM_PACKAGES_TO_DOWNLOAD_RELATIVE_PATH, NPM_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH, {})


    # npm_list = generate_package_list(
        # NPM_PACKAGES_TO_DOWNLOAD_RELATIVE_PATH, PackageType(NPM_PACKAGE_NAME))

    pypi_list = generate_package_list(
        PYPI_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH, PackageType(PYTHON_PACKAGE_NAME))

    # requirement_list = npm_list + pypi_list
    requirement_list = pypi_list

    for index in range(2):
        thread = RegisterWorker(packages_queue, download_queue)
        thread.setDaemon(True)
        thread.start()

    for package in requirement_list:
        packages_queue.put(package)

    # create a thread pool and give them a queue
    # downloading thread pool
    for index in range(4):
        thread = DownloaderWorker(download_queue)
        thread.setDaemon(True)
        thread.start()

    # wait for the queue to finish
    packages_queue.join()
    download_queue.join()
