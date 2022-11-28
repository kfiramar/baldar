import pandas as pd


def get_csv(path):
    result_csv = pd.read_csv(path)
    return result_csv


def get_first_lines(path: str, number_of_lines: int):
    csv = pd.read_csv(path, nrows=number_of_lines)

    return csv


def get_top_packages(file_path: str, line_amount: int = 20):
    return list(get_first_lines(file_path, line_amount)['project'])
