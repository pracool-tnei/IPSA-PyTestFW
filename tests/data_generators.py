import pandas as pd


def get_sheet_cases(
        benchmark_file,
        result_file,
        model_name):

    xls = pd.ExcelFile(benchmark_file)

    cases = []

    for sheet in xls.sheet_names:

        cases.append({
            "model": model_name,
            "sheet": sheet,
            "benchmark_file": benchmark_file,
            "result_file": result_file
        })

    return cases