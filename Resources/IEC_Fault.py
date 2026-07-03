from pathlib import Path
from io import StringIO
import os
import random
import ipsa
import pandas as pd

DEBUG_MODE = True

import builtins
import inspect
import os
from datetime import datetime

# Save original print
_original_print = builtins.print

if DEBUG_MODE:
    def print(*args, **kwargs):
        """
        Custom print that prepends:
        [timestamp] [filename:line] [function]
        """

        frame = inspect.currentframe().f_back

        filename = os.path.basename(frame.f_code.co_filename)
        lineno = frame.f_lineno
        function = frame.f_code.co_name

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prefix = (
            f"[{timestamp}] "
            f"[{filename}:{lineno}] "
            f"[{function}]"
        )

        _original_print(prefix, *args, **kwargs)

def find_fault_study_type_index(fault_study_type):
    match fault_study_type:
        case 'Fault levels on all busbars':
            fault_study_type_index = 1
        case 'Fault levels on selected busbars':
            fault_study_type_index = 2
        case _:
            fault_study_type_index = -1
    return fault_study_type_index

def find_fault_type_index(fault_type):
    match fault_type:
        case 'LG':
            fault_type_index = 1
        case 'LL':
            fault_type_index = 2
        case 'LLG':
            fault_type_index = 3
        case 'LLL':
            fault_type_index = 4
        case _:
            fault_type_index = -1
    return fault_type_index

def returnCSVObject(results):
    return StringIO(results)

def busbarsFLData(net, ipsanetwork):
    dict_busbars = net.GetBusbars()
    if dict_busbars =={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.BusbarFL)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarFL))
    print(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarFL))
    return main

def run_iec_fault_level(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name):
    for fault_study_type in ['Fault levels on all busbars']: #, 'Fault levels on selected busbars']:
        fault_level_results_data = []
        fault_types = ['LLL', 'LG', 'LL', 'LLG']
        for fault_type in fault_types:
            FL = net.GetAnalysisFL()
            FL.SetIValue(FL.FaultEngine, 1)
            FL.SetDValue(FL.FaultTime, 0.1)

            if find_fault_study_type_index(fault_study_type) != -1:
                FL.SetIValue(FL.FaultStudyType, find_fault_study_type_index(fault_study_type))
            else:
                print("Invalid Fault Level Study Input")

            if find_fault_type_index(fault_type) != -1:
                FL.SetIValue(FL.FaultEngineType, find_fault_type_index(fault_type))
            else:
                print("Invalid Fault Type Input")

            fault_level = net.DoIECFaultLevel()

            busbars_data = busbarsFLData(net, ipsanetwork)
            dict_fault = {
                            'fault_study_type': fault_study_type,
                            'fault type': fault_type,
                            'fault_success': fault_level,
                            'busbars_data': busbars_data
                        }
            fault_level_results_data.append(dict_fault)
            # filtered_dict_fault = {k: v for k, v in dict_fault.items() if v is not False}

        try:
            folder = os.path.dirname(cwd)
            folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
            folder_path.mkdir(parents=True, exist_ok=True)
            sub_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'Fault Analysis' / 'IEC 60909' /f'{fault_study_type}'
            sub_folder_path.mkdir(parents=True, exist_ok=True)
            file_path = sub_folder_path / f"{IPSA_file_name[:-4]}_{fault_study_type}_{ipsa_version}.xlsx"
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for fault in fault_level_results_data:
                    sheet_name = fault['fault type']
                    df = pd.read_csv(fault['busbars_data'], sep="\t")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            return file_path
        except Exception as e:
            print(e)
            print("Close the excel file before running script")
