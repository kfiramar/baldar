import requests
import re
from pydantic import BaseModel
import csv


def pypi_list():
    r = requests.get("https://pypi.org/simple")
    x = re.findall('\>(.*?)\<', r.text)
    return x


def write_to_csv(path, package_name, Health_score):
    with open(path, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([package_name, Health_score])


def python_health_score(package_name):
    try:
        r = requests.get(
            "https://snyk.io/advisor/python/{}/".format(package_name))
        x = re.search('package health:\s*([^\n\r]*)\/100">', r.text)
        return x.group(1)
    except Exception:
        return "invalid pakage name"


def python_AllHealthScore(path, package_list):
    package_list = pypi_list()
    for package in package_list:
        try:
            score = python_health_score(package)
            write_to_csv(path, package, score)
        except Exception:
            None
