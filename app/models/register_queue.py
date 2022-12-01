from app.core.config import NPM_PACKAGE_NAME, PYTHON_PACKAGE_NAME
import threading

from time import sleep
from typing import List
from queue import Queue
from app.models.requirement import Requirement

from app.models.package import Package
from app.python.main import generate_python_download_list
from app.js.main import generate_npm_download_list
from app.models.package import Package
from app.services.db_handler import get_latest_db_version, insert_new_package, update_package


class RegisterWorker(threading.Thread):
    """Threaded packages scrapper"""

    def __init__(self, queue, packages_queue: Queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.packages_queue = packages_queue

    def run(self):
        while True:
            download_list: List[Package] = []
            requirement: Requirement = self.queue.get()

            if requirement.package_type == NPM_PACKAGE_NAME:
                download_list = generate_npm_download_list(
                    requirement.package_name)
            else:
                download_list = generate_python_download_list(
                    requirement.package_name)

            for package in download_list:
                self.packages_queue.put(package)

            # if download_list:
            #     latest_db_version = get_latest_db_version(
            #         requirement.package_name, download_list[0].package_type)

                # checks if the package is already in the database
                # inserting / updateing the version on db
                # if latest_db_version != BASE_VERSION:
                #     update_package(download_list[0])
                # else:
                #     insert_new_package(download_list[0])

            sleep(2)

            self.queue.task_done()
