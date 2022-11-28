import threading
from pydantic.types import FilePath
from requests import get

from app.models.package import Package

from app.core.config import DOWNLOAD_FOLDER

from os import makedirs


class DownloaderWorker(threading.Thread):
    """Threaded File Downloader"""

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # gets the url from the queue
            package = self.queue.get()

            # download the file
            self.download_file(package)

            # send a signal to the queue that the job is done
            self.queue.task_done()

    def download_file(self, package: Package) -> None:
        file_path = f"{DOWNLOAD_FOLDER}\{package.package_type}\{package.package_name}\{package.file_name}"

        with get(package.download_url, stream=True) as request:
            request.raise_for_status()
            try:
                with open(file_path, 'wb') as file:
                    for chunk in request.iter_content(chunk_size=8192):
                        file.write(chunk)
            except FileNotFoundError:
                directory_path = file_path[0:file_path.rindex('\\')]
                makedirs(directory_path)
