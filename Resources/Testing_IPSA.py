import ipsa
import os
import sys
from pathlib import Path 

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(cwd))
sys.path.extend([x[0] for x in os.walk(sys.exec_prefix + r"/Lib")])

import Loadflow
import Fault_Level
import IEC_Fault
import Harmonics_Study
import Create_difference_file
import GeneratePDF

#file copy and unzip
import shutil
import zipfile

#config parser
import configparser

#logging
from Logger import debug, info, error, setLoggerMode

#macro controlled execution
IsBenchmarkGeneration = False
IsBenchmarkComparison = not IsBenchmarkGeneration

BASE_VERSION = 'vbenchmark' #Enter the version of IPSA to be compared with
TEST_VERSION = 'v3.2.2' #Enter the version of IPSA to compare
NETWORK_BENCHMARK = r"S:\Adarsh\vbenchmark.zip"
LOCAL_BENCHMARK = ""

def parse_config():
    config = configparser.ConfigParser()

    config_path = Path(__file__).parent / "config.ini"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    config.read(config_path)

    global IsBenchmarkGeneration
    IsBenchmarkGeneration = config.getboolean(
        "Benchmark",
        "IsBenchmarkGeneration"
    )
    global IsBenchmarkComparison
    IsBenchmarkComparison = not IsBenchmarkGeneration

    global BASE_VERSION
    BASE_VERSION = config.get(
        "Benchmark",
        "BASE_VERSION"
    )

    global TEST_VERSION
    TEST_VERSION = config.get(
        "Benchmark",
        "TEST_VERSION"
    )

    global NETWORK_BENCHMARK
    NETWORK_BENCHMARK = config.get(
        "Benchmark",
        "NETWORK_BENCHMARK"
    )
    info( "IsBenchmarkGeneration " + str(IsBenchmarkGeneration))
    info ("BASE_VERSION " + BASE_VERSION)
    info("TEST_VERSION " + TEST_VERSION)
    info("NETWORK_BENCHMARK "  + NETWORK_BENCHMARK)


def ensure_local_benchmark(cwd):
    local_benchmark_root = Path(cwd).parent / "Test Results" / "vbenchmark"

    # Already cached locally
    if local_benchmark_root.exists():
        print(f"Using local benchmark cache: {local_benchmark_root}")
        return str(local_benchmark_root)

    network_zip = NETWORK_BENCHMARK

    if not os.path.exists(network_zip):
        raise FileNotFoundError(
            f"Benchmark archive not found:\n{network_zip}"
        )

    debug(f"Downloading benchmark archive from : {network_zip}...")

    local_zip = Path(cwd).parent / "Test Results" / "vbenchmark.zip"

    os.makedirs(local_zip.parent, exist_ok=True)

    shutil.copy2(network_zip, local_zip)

    debug("Extracting benchmark archive...")

    with zipfile.ZipFile(local_zip, 'r') as zf:
        zf.extractall(local_zip.parent)

    debug("Benchmark extraction complete.")

    return str(local_benchmark_root)


def compareFiles(test_file_paths, new_name, comparison_status):
    debug(f"test_file_paths : {test_file_paths} new_name : {new_name}")
    test_file_paths = str(test_file_paths)
    base_file_path = test_file_paths.replace(TEST_VERSION, BASE_VERSION)
    output_folder = os.path.dirname(test_file_paths)
    output_file = os.path.join(output_folder, f'Test_differences{new_name}_{TEST_VERSION}_{BASE_VERSION}.xlsx')
    comparison_success, all_differences = Create_difference_file.compare_and_highlight(base_file_path, test_file_paths, output_file)
    if comparison_success == False:
        base_file_name = os.path.basename(base_file_path)
        test_file_name = os.path.basename(test_file_paths)
        comparison_status[(base_file_name, test_file_name, str(output_file))] = [comparison_success, all_differences]

"""
if __name__ == "__main__":
    try:
        parse_config()
        if IsBenchmarkComparison:
            LOCAL_BENCHMARK = ensure_local_benchmark(cwd)
        #Provide the path of files that are to be tested
        files=[ 
                # "C:\\Users\\ruben.pulayath\\OneDrive - TNEI Services Ltd\\Desktop\\Testing IPSA\\Models\\Basic Testing I\\ENWL INM AllGen 240423.i2f",
                # "C:\\Users\\ruben.pulayath\\OneDrive - TNEI Services Ltd\\Desktop\\Testing IPSA\\Models\\Basic Testing I\\NGED West Midlands Connected CDP.i2f",
                # "C:\\Users\\ruben.pulayath\\OneDrive - TNEI Services Ltd\\Desktop\\Testing IPSA\\Models\\Basic Testing I\\SPM Current Model CIM R0.69.i2f",
                # "C:\\Users\\ruben.pulayath\\OneDrive - TNEI Services Ltd\\Desktop\\Testing IPSA\\Models\\Basic Testing I\\SuperGrid R1.i2f",
                #"C:\\Users\\ruben.pulayath\\OneDrive - TNEI Services Ltd\\Desktop\\Testing IPSA\\Models\\Windfarm Harmonics Example.i3f" #BASIC TESTING III
                # "C:\\Users\\ruben.pulayath\\OneDrive - TNEI Services Ltd\\Desktop\\Testing IPSA\\Models\\Simple Defined Fault.i3f" #BASIC TESTING III

               ]

        models_folder = Path(cwd) / "models"
        print("Current working directory " + str(models_folder))


        # Recursively find all .i3f files under Models folder
        files = [str(f.resolve()) for f in models_folder.rglob("*.i*f")]

        #print the name of network files
        print("Networks found for testing:")
        for file in files:
            print(file)

        ipsanetwork = ipsa.GetInterface()
        comparison_status = {}
        for file in files:
            net = ipsanetwork.ReadFile(file)
            if IsBenchmarkGeneration == True:
                ipsa_version= "vbenchmark"
            else:
                ipsa_version = ipsanetwork.GetVersion()


            IPSA_file_name= ipsanetwork.GetNetworkFileName()
            #Basic Testing III
            if IPSA_file_name == "IEEE 9 Bus Network.i3f":
                load_flow_test_file_path = Loadflow.run_loadflow(ipsanetwork,net,cwd,ipsa_version,IPSA_file_name)
                if IsBenchmarkComparison == True:
                    compareFiles(load_flow_test_file_path, '_', comparison_status)
                fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,"Fault levels on all busbars")
                if IsBenchmarkComparison == True:
                    compareFiles(fault_test_file_path, '_', comparison_status)
                # fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault levels on selected busbars')
                # compareFiles(fault_test_file_path, '_', comparison_status)
                iec_fault_path = IEC_Fault.run_iec_fault_level(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name)
                if IsBenchmarkComparison == True:
                    compareFiles(iec_fault_path, '_', comparison_status)
            elif IPSA_file_name == "Simple Network Fault Level 3ph.i3f":
                load_flow_test_file_path = Loadflow.run_loadflow(ipsanetwork,net,cwd,ipsa_version,IPSA_file_name)
                fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault levels on selected busbars')
                if IsBenchmarkComparison == True:
                    compareFiles(fault_test_file_path, '_', comparison_status)
            elif IPSA_file_name == "Simple Defined Fault.i3f":
                fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,"Fault levels on all busbars")
                if IsBenchmarkComparison == True:
                    compareFiles(fault_test_file_path, '_', comparison_status)
                fault_test_file_paths = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault on single busbar')
                for path in fault_test_file_paths:
                    name = path.name
                    parts = name.split('_')
                    new_name =  '_'.join(parts[-2:-1])
                    new_name = '_' + new_name
                    if IsBenchmarkComparison == True:
                        compareFiles(path, new_name, comparison_status)
            elif IPSA_file_name == "IEEE 9 Bus Network2.i3f":
                fault_test_file_paths= Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault along a line')
                for path in fault_test_file_paths:
                    name = path.name
                    parts = name.split('_')
                    new_name =  '_'.join(parts[-2:-1])
                    new_name = '_' + new_name
                    if IsBenchmarkComparison == True:
                        compareFiles(path, new_name, comparison_status)
            elif IPSA_file_name == "Windfarm Harmonics Example.i3f":
                harmonics_file_paths = Harmonics_Study.runHarmonics(ipsanetwork,net,cwd,ipsa_version,IPSA_file_name)
                for path in harmonics_file_paths:
                    name = path.name
                    parts = name.split('_')
                    new_name =  '_'.join(parts[-2:-1])
                    new_name = '_' + new_name
                    # compareFiles(path, new_name, comparison_status)
            else:
                #BASIC TESTING I
                load_flow_test_file_path = Loadflow.run_loadflow(ipsanetwork,net,cwd,ipsa_version,IPSA_file_name)
                if IsBenchmarkComparison == True:
                    compareFiles(load_flow_test_file_path, '_', comparison_status)
                fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,"Fault levels on all busbars")
                if IsBenchmarkComparison == True:
                    compareFiles(fault_test_file_path, '_', comparison_status)
                FL = net.GetAnalysisFL()
                sel_busbars = FL.GetBusesToFault()
                if sel_busbars:
                    fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault levels on selected busbars')
                    if IsBenchmarkComparison == True:
                        compareFiles(fault_test_file_path, '_', comparison_status)

                # fault_test_file_paths = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault on single busbar')
                # for path in fault_test_file_paths:
                #     name = path.name
                #     parts = name.split('_')
                #     new_name =  '_'.join(parts[-2:-1])
                #     new_name = '_' + new_name
                #     compareFiles(path, new_name, comparison_status)
                # fault_test_file_paths= Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault along a line')
                # for path in fault_test_file_paths:
                #     name = path.name
                #     parts = name.split('_')
                #     new_name =  '_'.join(parts[-2:-1])
                #     new_name = '_' + new_name
                #     compareFiles(path, new_name, comparison_status)

            # print(f"{IPSA_file_name} is closed : {ipsanetwork.CloseNetwork()}")

        folder = os.path.dirname(cwd)
        report_file_name = folder + '\\' + 'Test Results' +'\\' + TEST_VERSION + '\\' + 'Comparison_Report.pdf'
        print(cwd)
        print(report_file_name)
        print(comparison_status)
        print(TEST_VERSION)
        print(BASE_VERSION)
        if IsBenchmarkComparison == True:
            GeneratePDF.generateGlobalPDF(cwd, report_file_name, comparison_status, TEST_VERSION, BASE_VERSION)
        print('debug analysis completed')
    except Exception as e:
        print(e)
        print ("Could not import IPSA")
        raise

"""

#handles main menu display
def print_main_menu():

    info("\n" + "=" * 60)
    info("IPSA Regression Test Framework")
    info("=" * 60)

    info("1. Run Load Flow Tests")
    info("2. Run Fault Analysis Tests")
    info("3. Run LoadFlow/Fault Analysis Tests")
    info("4. Generate Benchmarks")
    info("5. Set Logger Mode")
    info("6. Help")
    info("0. Exit")


#gets alll the models from current dir
def get_models():
    """
    Return all *.i3f models from ../models directory.
    """

    models_dir = Path(cwd) / "models"

    if not models_dir.exists():
        raise FileNotFoundError(
            f"Models directory not found:\n{models_dir}"
        )

    return sorted([str(f) for f in models_dir.glob("*.i3f")])


#display names of all the models present in the /models dir
def display_models(models):
    debug("\nAvailable Models\n")

    for idx, model in enumerate(models, start=1):
        debug(f"{idx}. {Path(model).stem}")

    debug(f"{len(models)+1}. Run ALL Models")
    debug("0. Back")


#select the model of choice
def get_model_selection(models):

    while True:

        display_models(models)

        choice = input("\nEnter option: ")

        try:
            choice = int(choice)

            if choice == 0:
                return []

            elif choice == len(models) + 1:
                return models

            elif 1 <= choice <= len(models):
                return [models[choice - 1]]

        except:
            pass

        error("Invalid option")

def run_single_test(
        model_path,
        comparison_status,
        run_loadflow=True,
        run_fault=True):
    net = ipsanetwork.ReadFile(model_path)
    debug("IsBenchmarkGeneration " + str(IsBenchmarkGeneration))
    debug("IsBenchmarkComparison " + str(IsBenchmarkComparison))


    if IsBenchmarkGeneration == True:
        ipsa_version = "vbenchmark"
    else:
        ipsa_version = ipsanetwork.GetVersion()

    IPSA_file_name = ipsanetwork.GetNetworkFileName()
    # Basic Testing III
    if IPSA_file_name == "IEEE 9 Bus Network.i3f":
        if run_loadflow == True:
            load_flow_test_file_path = Loadflow.run_loadflow(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name)
            if IsBenchmarkComparison == True:
                compareFiles(load_flow_test_file_path, '_', comparison_status)
        if run_fault == True:
            fault_test_file_path = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                           "Fault levels on all busbars")
            if IsBenchmarkComparison == True:
                compareFiles(fault_test_file_path, '_', comparison_status)
            # fault_test_file_path = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault levels on selected busbars')
            # compareFiles(fault_test_file_path, '_', comparison_status)
            iec_fault_path = IEC_Fault.run_iec_fault_level(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name)
            if IsBenchmarkComparison == True:
                compareFiles(iec_fault_path, '_', comparison_status)
    elif IPSA_file_name == "Simple Network Fault Level 3ph.i3f":
        if run_loadflow == True:
            load_flow_test_file_path = Loadflow.run_loadflow(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name)
        if run_fault == True:
            fault_test_file_path = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                           'Fault levels on selected busbars')
            if IsBenchmarkComparison == True:
                compareFiles(fault_test_file_path, '_', comparison_status)
    elif IPSA_file_name == "Simple Defined Fault.i3f":
        if run_fault == True:
            fault_test_file_path = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                           "Fault levels on all busbars")
            if IsBenchmarkComparison == True:
                compareFiles(fault_test_file_path, '_', comparison_status)

            fault_test_file_paths = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                            'Fault on single busbar')
            for path in fault_test_file_paths:
                name = path.name
                parts = name.split('_')
                new_name = '_'.join(parts[-2:-1])
                new_name = '_' + new_name
                if IsBenchmarkComparison == True:
                    compareFiles(path, new_name, comparison_status)
    elif IPSA_file_name == "IEEE 9 Bus Network2.i3f":
        if run_fault == True:
            fault_test_file_paths = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                            'Fault along a line')
            for path in fault_test_file_paths:
                name = path.name
                parts = name.split('_')
                new_name = '_'.join(parts[-2:-1])
                new_name = '_' + new_name
                if IsBenchmarkComparison == True:
                    compareFiles(path, new_name, comparison_status)
    elif IPSA_file_name == "Windfarm Harmonics Example.i3f":
        if run_fault == True:
            harmonics_file_paths = Harmonics_Study.runHarmonics(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name)
            for path in harmonics_file_paths:
                name = path.name
                parts = name.split('_')
                new_name = '_'.join(parts[-2:-1])
                new_name = '_' + new_name
                # compareFiles(path, new_name, comparison_status)
    else:
        # BASIC TESTING I
        if  run_loadflow == True:
            load_flow_test_file_path = Loadflow.run_loadflow(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name)
            if IsBenchmarkComparison == True:
                compareFiles(load_flow_test_file_path, '_', comparison_status)
        if run_fault == True:
            fault_test_file_path = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                               "Fault levels on all busbars")
            if IsBenchmarkComparison == True:
                compareFiles(fault_test_file_path, '_', comparison_status)

            FL = net.GetAnalysisFL()
            sel_busbars = FL.GetBusesToFault()
            if sel_busbars:
                fault_test_file_path = Fault_Level.run_fault_level(net, cwd, ipsa_version, IPSA_file_name,
                                                                   'Fault levels on selected busbars')
                if IsBenchmarkComparison == True:
                    compareFiles(fault_test_file_path, '_', comparison_status)

        # fault_test_file_paths = Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault on single busbar')
        # for path in fault_test_file_paths:
        #     name = path.name
        #     parts = name.split('_')
        #     new_name =  '_'.join(parts[-2:-1])
        #     new_name = '_' + new_name
        #     compareFiles(path, new_name, comparison_status)
        # fault_test_file_paths= Fault_Level.run_fault_level(net,cwd,ipsa_version,IPSA_file_name,'Fault along a line')
        # for path in fault_test_file_paths:
        #     name = path.name
        #     parts = name.split('_')
        #     new_name =  '_'.join(parts[-2:-1])
        #     new_name = '_' + new_name
        #     compareFiles(path, new_name, comparison_status)

    # print(f"{IPSA_file_name} is closed : {ipsanetwork.CloseNetwork()}")

#run load flow only
def run_loadflow_tests(selected_models):
    comparison_status = {}
    for model in selected_models:

        debug("\nRunning Load Flow")

        IPSA_file_name = Path(model).name

        debug(f"Model : {IPSA_file_name}")

        run_single_test(
            model,
            comparison_status,
            run_loadflow=True,
            run_fault=False

        )

    folder = os.path.dirname(cwd)
    report_file_name = folder + '\\' + 'Test Results' + '\\' + TEST_VERSION + '\\' + 'Comparison_Report.pdf'

    debug(f"cwd : {cwd}  report_file_name : {report_file_name}  comparison_status : {comparison_status} TEST_VERSION : {TEST_VERSION} BASE_VERSION : {BASE_VERSION}")
    if IsBenchmarkComparison == True:
        GeneratePDF.generateGlobalPDF(cwd, report_file_name, comparison_status, TEST_VERSION, BASE_VERSION)
    print('debug analysis completed')

#run fault analysis only
def run_fault_tests(selected_models):
    comparison_status = {}
    for model in selected_models:

        debug("\nRunning Fault Analysis")

        IPSA_file_name = Path(model).name

        debug(f"Model : {IPSA_file_name}")

        run_single_test(
            model,
            comparison_status,
            run_loadflow=False,
            run_fault=True
        )
    folder = os.path.dirname(cwd)
    report_file_name = folder + '\\' + 'Test Results' + '\\' + TEST_VERSION + '\\' + 'Comparison_Report.pdf'

    debug(
        f"cwd : {cwd}  report_file_name : {report_file_name}  comparison_status : {comparison_status} TEST_VERSION : {TEST_VERSION} BASE_VERSION : {BASE_VERSION}")
    if IsBenchmarkComparison == True:
        GeneratePDF.generateGlobalPDF(cwd, report_file_name, comparison_status, TEST_VERSION, BASE_VERSION)
    print('debug analysis completed')

#run benchmark generation
def generate_benchmarks():

    global IsBenchmarkGeneration
    global IsBenchmarkComparison

    IsBenchmarkGeneration = True
    IsBenchmarkComparison = False

    models = get_models()

    debug(
        f"\nGenerating benchmarks "
        f"for {len(models)} models"
    )

    comparison_status = {}
    for model in models:

        debug(f"Generating benchmark : {model}")

        try:
            run_single_test(
                model,
                comparison_status,
                run_loadflow=True,
                run_fault=True
            )
        finally:
            #ipsanetwork.CloseNetwork()
            print("finally")

def print_logger_modes():

    info("\n" + "=" * 60)
    info("Logger Modes")
    info("=" * 60)

    info("1. Info")
    info("2. Debug")
    info("0. Exit")

#display help
def show_help():

    info("\nHelp")
    info("-" * 40)

    debug("Load Flow Tests:")
    debug("    Executes load flow analysis on selected models.")
    debug()

    debug("Fault Analysis Tests:")
    debug("    Executes fault analysis on selected models.")
    debug()

    debug("Generate Benchmarks:")
    debug("    Generates benchmark results for all models.")

if __name__ == "__main__":

    parse_config()
    if IsBenchmarkComparison:
        LOCAL_BENCHMARK = ensure_local_benchmark(cwd)

    ipsanetwork = ipsa.GetInterface()
    comparison_status = {}

    while True:

        print_main_menu()

        option = input("\nSelect option: ")

        if option == "1":
            IsBenchmarkGeneration = False
            IsBenchmarkComparison = True
            models = get_models()
            selected = get_model_selection(models)
            if selected:
                run_loadflow_tests(selected)

        elif option == "2":
            IsBenchmarkGeneration = False
            IsBenchmarkComparison = True
            models = get_models()
            selected = get_model_selection(models)

            if selected:
                run_fault_tests(selected)
        elif option == "3":
            IsBenchmarkGeneration = False
            IsBenchmarkComparison = True
            models = get_models()
            selected = get_model_selection(models)
            if selected:
                run_loadflow_tests(selected)
                run_fault_tests(selected)

        elif option == "4":
            confirm = input(
                "\nGenerate benchmarks for ALL models? (y/n): "
            )

            if confirm.lower() == "y":
                generate_benchmarks()

        elif option == "5":
            print_logger_modes()
            option = input("\nSelect option: ")
            if option == "1":
                setLoggerMode(False)
            elif option == "2":
                setLoggerMode(True)
            elif option == "3":
                pass

        elif option == "6":

            show_help()

        elif option == "0":

            info("Exiting...")
            sys.exit(0)

        else:
            error("Invalid option")