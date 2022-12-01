from app.models.package import Package
from pyodbc import Connection, connect
from datetime import datetime
from app.services.version_service import get_latest_version_from_dataset
from app.core.config import CONNECTION_STRING

now = datetime.now()


def get_sql_connection() -> Connection:
    return connect(CONNECTION_STRING)


def find_registered_version(package_name: str, package_type: str) -> list:
    query_results = []
    connection = get_sql_connection()

    with connection:
        cursor = connection.cursor()
        execution_result = cursor.execute(
            f"SELECT Package_Version FROM [dbo].[Packages] WHERE Package_Name='{package_name}' AND Package_Type='{package_type}'")

        query_results = execution_result.fetchall()

    return query_results


def get_latest_db_version(package_name: str, package_type: str) -> str:
    return '0.0.0'
    # versions = find_registered_version(package_name, package_type)

    # return get_latest_version_from_dataset(versions)


def insert_new_package(package: Package) -> None:
    connection = get_sql_connection()
    with connection:
        cursor = connection.cursor()
        cursor.execute('''
                    INSERT INTO dbo.Packages(Package_Name, Package_Version, Package_Type, Bidul_Date)
                    VALUES (?,?,?,?)
                    ''',
                       package.package_name,
                       package.version,
                       package.package_type,
                       now
                       )
        connection.commit()


def update_package(package: Package) -> None:
    connection = get_sql_connection()
    with connection:
        cursor = connection.cursor()
        cursor.execute('''
                    UPDATE dbo.Packages SET Package_Version=?, Bidul_Date=?
                    WHERE Package_Name=?
                    AND Package_Type=?
                    ''',
                       package.version,
                       now,
                       package.package_name,
                       package.package_type
                       )
        connection.commit()
