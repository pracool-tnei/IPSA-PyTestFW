import ipsa
import os
import pandas as pd
from io import StringIO
from pathlib import Path
from Logger import debug, info,error


def returnCSVObject(results):
    return StringIO(results)

def busbarsLFData(net, ipsanetwork):
    dict_busbars = net.GetBusbars()
    if dict_busbars =={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.BusbarLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.BusbarLF)
    return main

def generatorsLFData(net, ipsanetwork):
    dict_generators = net.GetSynMachines()
    if dict_generators == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.GeneratorLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.GeneratorLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.GeneratorLF)
    return main

def gridInfeedsLFData(net, ipsanetwork):
    dict_grid_infeeds = net.GetGridInfeeds()
    if dict_grid_infeeds == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.GridInfeedLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.GridInfeedLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.GridInfeedLF)
    return main

def loadsLFData(net, ipsanetwork):
    dict_loads = net.GetLoads()
    if dict_loads == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.LoadLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.LoadLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.LoadLF)
    return main

#Induction machine
def inductionMachineLFData(net, ipsanetwork):
    dict_induction_machines = net.GetIndMachines()
    if dict_induction_machines =={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.IMachineLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.IMachineLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.IMachineLF)
    return main

def universalMachineLFData(net, ipsanetwork):
    dict_universal_machines = net.GetUMachines()
    if dict_universal_machines =={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.UMachineLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.UMachineLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.UMachineLF)
    return main

def harmonicfiltersLFData(net, ipsanetwork):
    dict_harmonic_filters = net.GetFilters()
    if dict_harmonic_filters == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.FilterLF)
    currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.FilterLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.FilterLF)
    return currents

def mechSwCapLFData(net, ipsanetwork):
    dict_msc = net.GetMechSwCapacitors()
    if dict_msc == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.MechSwCapLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.MechSwCapLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.MechSwCapLF)
    return main

def staticVCsLFData(net, ipsanetwork):
    dict_svc = net.GetStaticVCs()
    if dict_svc == {}:
        return False
    else:                                                                   
        status = [ins.GetIValue(ins.Status) for ins in dict_svc.values()]
        if set(status) != {-1}:                               #If component exists in the network but every component is switched out, there will be no results generated.
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.StaticVCLF)
            main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.StaticVCLF))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.StaticVCLF)
            return main
        else:
            return False

def batteryLFData(net, ipsanetwork):
    dict_battery = net.GetBatteries()
    if dict_battery == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.BatteryLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BatteryLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.BatteryLF)
    return main

def dCMachineLFData(net, ipsanetwork):
    dict_dc = net.GetDCMachines()
    if dict_dc == {}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.DCMachineLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.DCMachineLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.DCMachineLF)
    return main

#Branches - single
def lineLFData(net, ipsanetwork):
    dict_branches = net.GetBranches()
    if dict_branches=={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.LineLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.LineLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.LineLF)
    return main

#Transformers - single
def transformerLFData(net, ipsanetwork):
    dict_transformer = net.GetTransformers()
    if dict_transformer =={}:
        return False 
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.TransformerLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.TransformerLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.TransformerLF)
    return main

#3W Transformers - single
def _3WtransformerLFData(net, ipsanetwork):
    dict_ThreeWtransformer = net.Get3WTransformers()
    if dict_ThreeWtransformer=={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.ThreeWindingTransformerLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.ThreeWindingTransformerLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.ThreeWindingTransformerLF)
    return main

def converterLFData(net, ipsanetwork):
    dict_converter = net.GetConverters()
    if dict_converter=={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.ConverterLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.ConverterLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.ConverterLF)
    return main

def chopperLFData(net, ipsanetwork):
    dict_chopper = net.GetChoppers()
    if dict_chopper=={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.ChopperLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.ChopperLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.ChopperLF)
    return main

def mGLFData(net, ipsanetwork):
    dict_mgsets = net.GetMGSets()
    if dict_mgsets=={}:
        return False
    ipsanetwork.DisplayResultsTable(ipsa.IscInterface.MGSetLF)
    main = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.MGSetLF))
    ipsanetwork.CloseResultsTable(ipsa.IscInterface.MGSetLF)
    return main

def run_loadflow(ipsanetwork,net,cwd,ipsa_version,IPSA_file_name):
    #Do flatstart before loadflow
    if IPSA_file_name=="SuperGrid R1.i2f":
        debug("SuperGrid")
        slack_bus_names=["Load Flow","D0"]
        for bus in slack_bus_names:
            net.SetBusbarSlack(bus)
    elif IPSA_file_name=="ENWL INM AllGen 240423.i2f":
        debug("ENWL_INM_AllGen_240423")
        slack_bus_names=["NG_EGGB41","risley_132_gt2","iom_33_a"]
        for bus in slack_bus_names:
            net.SetBusbarSlack(bus)
    elif IPSA_file_name=="NGED West Midlands Connected CDP.i2f":
        debug("NGED-West Midlands-Connected_CDP")
        slack_bus_names=["CELL4","HAMS4","RUGE4","WALH4","BUST2_RES","IROA2","KITW2","NECE2","OCKH2","OLDB2","PENN2","WIEN2A","DRAK1_DUM"]
        for bus in slack_bus_names:
            net.SetBusbarSlack(bus)
            
    elif IPSA_file_name=="SPM Current Model CIM R0.69.i2f":
        debug("SPM Current Model CIM R0.69.i2f")
        slack_bus_names=["IRON41"]
        for bus in slack_bus_names:
            net.SetBusbarSlack(bus)

    LF = net.GetAnalysisLF()
    LF.SetBValue(LF.InitFlatStart, True)
    LF.SetBValue(LF.FSSetBusbarVoltages, True)
    LF.SetDValue(LF.FSVoltageMagnitudePU, 1.0)
    LF.SetDValue(LF.FSVoltageAngleDeg, 0.0)
    LF.SetBValue(LF.FSSetTransformerTaps, True)
    LF.SetIValue(LF.FSNominalTaps, 1)
    LF.SetBValue(LF.FSSetInductionMachineSlips, True)
    LF.SetDValue(LF.FSSlipPC, 0.1)
    # flatstart=net.DoFlatStart(True, True, True)
    
    #Check convergence by doing load flow
    convergence = net.DoLoadFlow()

    busbars_data = busbarsLFData(net, ipsanetwork)
    generators_data = generatorsLFData(net, ipsanetwork)
    grid_data = gridInfeedsLFData(net,ipsanetwork)
    loads_data = loadsLFData(net, ipsanetwork)
    induction_machine_data = inductionMachineLFData(net, ipsanetwork)
    universal_machine_data = universalMachineLFData(net, ipsanetwork)
    harmonic_filters_data = harmonicfiltersLFData(net, ipsanetwork)
    msc_data =  mechSwCapLFData(net, ipsanetwork)
    svc_data = staticVCsLFData(net, ipsanetwork)
    battery_data = batteryLFData(net, ipsanetwork)
    dc_machine_data = dCMachineLFData(net, ipsanetwork)
    lines_data = lineLFData(net, ipsanetwork)
    transformers_data = transformerLFData(net, ipsanetwork)
    ThreeWtransformers_data = _3WtransformerLFData(net, ipsanetwork)
    converter_data = converterLFData(net, ipsanetwork)
    chopper_data = chopperLFData(net, ipsanetwork)
    mg_data = mGLFData(net, ipsanetwork)                            

    dict_lf = {
        'Busbars': busbars_data,
        'Generators': generators_data,
        'Grid' : grid_data,
        'Loads': loads_data,
        'Induction machine': induction_machine_data,
        'Lines and cables': lines_data,
        'Transformers': transformers_data,
        'Three Winding Transformers': ThreeWtransformers_data,
        'Static VAr compensators' : svc_data,
        'Mech. switched capacitors' : msc_data,
        'Universal machines' : universal_machine_data,
        'Harmonic filters' : harmonic_filters_data,
        'Batteries' : battery_data,
        'DC machines' : dc_machine_data,
        'AC_DC converters' : converter_data,
        'DC choppers' : chopper_data,
        'MG sets' : mg_data      
            }
    filtered_dict_lf = {k: v for k, v in dict_lf.items() if v is not False}

    try:
        folder = os.path.dirname(cwd)
        folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
        folder_path.mkdir(parents=True, exist_ok=True)
        sub_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'Load Flow'
        sub_folder_path.mkdir(parents=True, exist_ok=True)
        file_path = sub_folder_path / f"{IPSA_file_name[:-4]}_LoadFlow_{ipsa_version}.xlsx"
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, value in filtered_dict_lf.items():
                value.seek(0)
                df = pd.read_csv(value, sep="\t")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        return file_path
    except Exception as e:
        error(e)
        error("Close the excel file before running script")