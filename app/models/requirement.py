from pydantic import BaseModel
from app.models.package_types import PackageType


class Requirement(BaseModel):
    package_name: str
    package_type: PackageType

    class Config:
        use_enum_values = True
