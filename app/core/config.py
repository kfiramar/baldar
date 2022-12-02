from os import environ
from datetime import datetime
CONNECTION_STRING: str = environ["DB_CONNECTION"]
DOWNLOAD_FOLDER: str = environ["DOWNLOAD_PATH"]
BASE_VERSION: str = '0.0.0'
PYTHON_PACKAGE_NAME: str = 'python'
NPM_PACKAGE_NAME: str = 'npm'

NPM_PACKAGES_TO_DOWNLOAD_RELATIVE_PATH = 'assets\\npm_requirements.txt'
NPM_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH = 'assets\\npm_full_download_list.txt'
PYPI_PACKAGES_TO_DOWNLOAD_FULL_LIST_RELATIVE_PATH = r'assets/pypi_requirements.txt'

LAST_UPDATED_DATE = datetime.strptime("2022-12-01T00:00:00", "%Y-%m-%dT%H:%M:%S")