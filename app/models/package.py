from pydantic import BaseModel


class Package(BaseModel):
    package_name: str
    version: str
    file_name: str
    package_type: str
    download_url: str
