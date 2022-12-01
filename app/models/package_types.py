import enum

from app.core.config import NPM_PACKAGE_NAME, PYTHON_PACKAGE_NAME


class PackageType(str, enum.Enum):
    python = PYTHON_PACKAGE_NAME
    npm = NPM_PACKAGE_NAME
