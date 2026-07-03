from pathlib import Path
from io import StringIO
import ipsa
import os
import sys 
import pandas as pd

def returnCSVObject(results):
    return StringIO(results)

def runHarmonics(ipsanetwork, net, cwd, ipsa_version, IPSA_file_name):

    def findHarmonicsCalculationType_index(harmonics_calculation_type):
        match harmonics_calculation_type:
            case 'Penetration':
                harmonics_calculation_type_index = 1
            case 'Voltage Waveform':
                harmonics_calculation_type_index = 2
            case 'Impedance Scan':
                harmonics_calculation_type_index = 3
            case _:
                harmonics_calculation_type_index = -1
        return harmonics_calculation_type_index
    
    def findHarmonicsSequenceIndex(harmonics_sequence):
        match harmonics_sequence:
            case 'Default':
                harmonics_sequence_index = 0
            case 'Positive':
                harmonics_sequence_index = 1
            case 'Zero':
                harmonics_sequence_index = 3
            case _:
                harmonics_sequence_index = -1
        return harmonics_sequence_index
    
    def findHarmonicModelIndex(harmonic_model):
        match harmonic_model:
            case 'Polynomial':
                harmonic_model_index = 0
            case 'sqrt(h).R':
                harmonic_model_index = 1
            case 'Constant X by R':
                harmonic_model_index = 2
            case 'Series R-X':
                harmonic_model_index = 0
            case 'Parallel R-X (1)':
                harmonic_model_index = 1
            case 'Parallel R-X (2)': 
                harmonic_model_index = 2
            case 'X plus parallel R-X': 
                harmonic_model_index = 3
            case _:
                harmonic_model_index = -1
        return harmonic_model_index
    
    def fetchBusbarsHarmonicsData(net, ipsanetwork, calculation_type):
        dict_busbars = net.GetBusbars()
        if dict_busbars =={}:
            return False
        if calculation_type == 'Penetration':
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.BusbarHM)
            busbars_summary_data = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.BusbarHM)
            return busbars_summary_data, None #csv object

        busbars_voltage_data_list = []
        busbars_impedance_data_list = []

        first_bus = next(iter(dict_busbars.values()))
        voltage_orders = first_bus.GetVoltageOrders()
        impedance_orders = first_bus.GetImpedanceOrders()

        if calculation_type == 'Voltage Waveform':
            # ipsanetwork.DisplayResultsTable(ipsa.IscInterface.BusbarHM)
            busbars_voltage_data = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarHM, 1))
            # ipsanetwork.CloseResultsTable(ipsa.IscInterface.BusbarHM)
            return busbars_voltage_data, None #csv object
            # for bus in dict_busbars.values():
            #     busbar_name = bus.GetSValue(bus.Name)
            #     busbars_voltage_data_dict = {
            #                     'Name': busbar_name,
            #                     }
            #     for order in voltage_orders:
            #         order_mag_pc = bus.GetVoltageMagnitudePC(order)
            #         order_angle = bus.GetVoltageAngle(order)
            #         busbars_voltage_data_dict[f'Order {order} Mag.(%)'] = order_mag_pc
            #         busbars_voltage_data_dict[f'Order {order} Angle'] = order_angle
            #     busbars_voltage_data_list.append(busbars_voltage_data_dict)
            # return busbars_voltage_data_list, None

        if calculation_type == 'Impedance Scan':
            busbars_impedance_data = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarHM, 1))
            return busbars_impedance_data, impedance_orders
            # for bus in dict_busbars.values():
            #     busbar_name = bus.GetSValue(bus.Name)
            #     busbars_impedance_data_dict = {
            #                     'Name': busbar_name,
            #                     }
            #     for order in impedance_orders:
            #         order_real = bus.GetImpedanceReal(order)
            #         order_imag = bus.GetImpedanceImaginary(order)
            #         busbars_impedance_data_dict[f'Order {order} Real'] = order_real
            #         busbars_impedance_data_dict[f'Order {order} Imag.'] = order_imag
            #     busbars_impedance_data_list.append(busbars_impedance_data_dict)
            # return busbars_impedance_data_list, impedance_orders
    
    def generatorHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders):
        dict_syn_machines = net.GetSynMachines()
        if dict_syn_machines =={}:
            return False
        
        if calculation_type in ['Penetration', 'Voltage Waveform']:
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.GeneratorHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.GeneratorHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.GeneratorHM)
            return currents

        syn_machines_current_data_list = []
        syn_machines_impedance_data_list = []

        # if calculation_type == 'Voltage Waveform':
            # for syn in dict_syn_machines.values():
            #     syn_machine_name = syn.GetSValue(syn.Name)
            #     syn_machines_current_data_dict = {
            #                             'Name': syn_machine_name,
            #                             }
            #     for order in current_orders:
            #         order_mag = syn.GetCurrentMagnitude(order)
            #         order_angle = syn.GetCurrentAngle(order)
            #         syn_machines_current_data_dict[f'Order {order} Mag.'] = order_mag
            #         syn_machines_current_data_dict[f'Order {order} Angle'] = order_angle
            #     syn_machines_current_data_list.append(syn_machines_current_data_dict)
            # return syn_machines_current_data_list

        if calculation_type == 'Impedance Scan':
            busbars_impedance_data = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.BusbarHM, 2))
            return busbars_impedance_data
            # for syn in dict_syn_machines.values():
            #     syn_machine_name = syn.GetSValue(syn.Name)
            #     syn_machines_impedance_data_dict = {
            #                     'Name': syn_machine_name,
            #                     }
            #     for order in impedance_orders:
            #         order_mag = syn.GetImpedanceMagnitude(order)
            #         syn_machines_impedance_data_dict[f'Order {order} Mag.'] = order_mag
            #     syn_machines_impedance_data_list.append(syn_machines_impedance_data_dict)
            # return syn_machines_impedance_data_list

    def loadHarmonicsData(net, ipsanetwork, calculation_type):
        dict_loads = net.GetLoads()
        if dict_loads == {}:
            return False
        if calculation_type in ['Penetration', 'Voltage Waveform']:
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.LoadHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.LoadHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.LoadHM)
            return currents
        else:
            return False
    
    #Induction machine
    def inductionMachineHarmonicsData(net, ipsanetwork, calculation_type):
        dict_induction_machines = net.GetIndMachines()
        if dict_induction_machines =={}:
            return False
        if calculation_type in ['Penetration', 'Voltage Waveform']:
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.IMachineHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.IMachineHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.IMachineHM)
            return currents
        
        induction_machines_impedance_data_list = []
        if calculation_type == 'Impedance Scan':
            return False
            for ind in dict_induction_machines.values():
                induction_machine_name = ind.GetSValue(ind.Name)
                induction_machines_impedance_data_dict = {
                                'Name': induction_machine_name,
                                }
                for order in impedance_orders:
                    order_mag = ind.GetImpedanceMagnitude(order)
                    induction_machines_impedance_data_dict[f'Order {order} Mag.'] = order_mag
                induction_machines_impedance_data_list.append(induction_machines_impedance_data_dict)
            return induction_machines_impedance_data_list

    def filterHarmonicsData(net, ipsanetwork, calculation_type):
        dict_harmonic_filters = net.GetFilters()
        if dict_harmonic_filters == {}:
            return False
        if calculation_type in ['Penetration', 'Voltage Waveform']:
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.FilterHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.FilterHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.FilterHM)
            return currents
        else:
            return False
    
    #Branches - single
    def lineHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders):
        dict_branches = net.GetBranches()
        if dict_branches=={}:
            return False
        if calculation_type in ['Penetration', 'Voltage Waveform']:
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.LineHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.LineHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.LineHM)
            return currents
        branch_impedeance_data_list = []
        if calculation_type == 'Impedance Scan':
            for branch in dict_branches.values():
                branch_from_busbar = branch.GetSValue(ipsa.IscBranch.FromBusName)
                branch_to_busbar = branch.GetSValue(ipsa.IscBranch.ToBusName)
                branch_from_nom_voltage_kv = net.GetBusbar(branch_from_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
                branch_to_nom_voltage_kv = net.GetBusbar(branch_to_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
                branch_name = branch.GetSValue(branch.Name)
                branch_impedance_data_dict = {
                                'From Busbar' : branch_from_busbar,
                                'To Busbar' : branch_to_busbar,
                                'From Nominal Voltage (kV)' : branch_from_nom_voltage_kv,
                                'To Nominal Voltage (kV)' : branch_to_nom_voltage_kv,
                                'Name': branch_name,
                                }
                for order in impedance_orders:
                    order_resistance = branch.GetResistance(order)
                    order_reactance = branch.GetReactance(order)
                    # order_susceptance = branch.GetSusceptance(order)
                    # print(order_susceptance)
                    branch_impedance_data_dict[f'Order {order} Resistance'] = order_resistance
                    branch_impedance_data_dict[f'Order {order} Reactance'] = order_reactance
                    # branch_impedance_data_dict[f'Order {order} Susceptance'] = order_susceptance
                branch_impedeance_data_list.append(branch_impedance_data_dict)
            return branch_impedeance_data_list
    
    #Transformers - single
    def transformerHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders):
        dict_transformer = net.GetTransformers()
        if dict_transformer =={}:
            return False
        if calculation_type in ['Penetration', 'Voltage Waveform']: 
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.TransformerHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.TransformerHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.TransformerHM)
            return currents
        transformer_impedeance_data_list = []
        if calculation_type == 'Impedance Scan':
            for transformer in dict_transformer.values():
                transformer_from_busbar = transformer.GetSValue(ipsa.IscTransformer.FromBusName)
                transformer_to_busbar = transformer.GetSValue(ipsa.IscTransformer.ToBusName)
                transformer_from_nom_voltage_kv = net.GetBusbar(transformer_from_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
                transformer_to_nom_voltage_kv = net.GetBusbar(transformer_to_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
                transformer_name = transformer.GetSValue(transformer.Name)
                transformer_impedance_data_dict = {
                                'From Busbar' : transformer_from_busbar,
                                'To Busbar' : transformer_to_busbar,
                                'From Nominal Voltage (kV)' : transformer_from_nom_voltage_kv,
                                'To Nominal Voltage (kV)' : transformer_to_nom_voltage_kv,
                                'Name': transformer_name,
                                }
                for order in impedance_orders:
                    order_resistance = transformer.GetResistance(order)
                    order_reactance = transformer.GetReactance(order)
                    transformer_impedance_data_dict[f'Order {order} Resistance'] = order_resistance
                    transformer_impedance_data_dict[f'Order {order} Reactance'] = order_reactance
                transformer_impedeance_data_list.append(transformer_impedance_data_dict)
            return transformer_impedeance_data_list

    #3W Transformers - single
    def _3WtransformerHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders):
        dict_ThreeWtransformer = net.Get3WTransformers()
        if dict_ThreeWtransformer=={}:
            return False
        if calculation_type in ['Penetration', 'Voltage Waveform']: 
            ipsanetwork.DisplayResultsTable(ipsa.IscInterface.ThreeWindingTransformerHM)
            currents = returnCSVObject(ipsanetwork.GetResultsTableText(ipsa.IscInterface.ThreeWindingTransformerHM))
            ipsanetwork.CloseResultsTable(ipsa.IscInterface.ThreeWindingTransformerHM)
            return currents
        ThreeWtransformer_impedeance_data_list = []
        if calculation_type == 'Impedance Scan':
            for ThreeWtransformer in dict_ThreeWtransformer.values():
                ThreeWtransformer_from_busbar = ThreeWtransformer.GetSValue(ipsa.Isc3Wtransformer.FromBusName)
                ThreeWtransformer_to_busbar = ThreeWtransformer.GetSValue(ipsa.Isc3Wtransformer.ToBusName)
                ThreeWtransformer_from_nom_voltage_kv = net.GetBusbar(ThreeWtransformer_from_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
                ThreeWtransformer_to_nom_voltage_kv = net.GetBusbar(ThreeWtransformer_to_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
                ThreeWtransformer_name = ThreeWtransformer.GetSValue(ThreeWtransformer.Name)
                ThreeWtransformer_impedance_data_dict = {
                                'From Busbar' : ThreeWtransformer_from_busbar,
                                'To Busbar' : ThreeWtransformer_to_busbar,
                                'From Nominal Voltage (kV)' : ThreeWtransformer_from_nom_voltage_kv,
                                'To Nominal Voltage (kV)' : ThreeWtransformer_to_nom_voltage_kv,
                                'Name': ThreeWtransformer_name,
                                }
                for order in impedance_orders:
                    for wdg in [1,2,3]:
                        order_resistance = ThreeWtransformer.GetResistance(wdg, order)
                        order_reactance = ThreeWtransformer.GetReactance(wdg, order)
                        ThreeWtransformer_impedance_data_dict[f'Order {wdg} {order} Resistance'] = order_resistance
                        ThreeWtransformer_impedance_data_dict[f'Order {wdg} {order} Reactance'] = order_reactance
                ThreeWtransformer_impedeance_data_list.append(ThreeWtransformer_impedance_data_dict)
            return ThreeWtransformer_impedeance_data_list
    
    def generateReport(harmonic_results_data, calculation_type, sequence, load_model, model):
        HM = net.GetAnalysisHM()
        HM.SetIValue(HM.MinimumHarmonicOrder, 1)
        HM.SetIValue(HM.MaximumHarmonicOrder, 50)

        HM.SetIValue(HM.HarmonicUseLongLines, 0)
        HM.SetIValue(HM.HarmonicGlobalLoadModel, 0)
        HM.SetIValue(HM.HarmonicGlobalLineModel, 0)
        HM.SetIValue(HM.HarmonicGlobalTransformerModel, 0)
        HM.SetIValue(HM.HarmonicGlobalShuntModel, 0)
        HM.SetIValue(HM.HarmonicGlobalGeneratorModel, 0)
        HM.SetIValue(HM.HarmonicGlobalMotorModel, 0)

        if findHarmonicsCalculationType_index(calculation_type) != -1:
            HM.SetIValue(HM.HarmonicStudyType, findHarmonicsCalculationType_index(calculation_type))
        else:
            print("Invalid Harmonics Study Input")

        if findHarmonicsSequenceIndex(sequence) != -1:
            HM.SetIValue(HM.HarmonicSequence, findHarmonicsSequenceIndex(sequence))
        else:
            print("Invalid Harmonic Sequence Input")

        sheet = ''
        
        if net.GetLoads() != {}:
            if findHarmonicModelIndex(load_model) != -1:
                HM.SetIValue(HM.HarmonicGlobalLoadModel, findHarmonicModelIndex(load_model))
                sheet = 'loads_'

        if net.GetBranches() != {}:
            if findHarmonicModelIndex(model) != -1:
                HM.SetIValue(HM.HarmonicUseLongLines, 1)
                HM.SetIValue(HM.HarmonicGlobalLineModel, findHarmonicModelIndex(model))
                sheet += 'lines_'
        if net.GetTransformers() != {}:
            if findHarmonicModelIndex(model) != -1:
                HM.SetIValue(HM.HarmonicGlobalTransformerModel, findHarmonicModelIndex(model))
                sheet += 'tf_'
        if net.GetSynMachines() != {}:
            if findHarmonicModelIndex(model) != -1:
                HM.SetIValue(HM.HarmonicGlobalGeneratorModel, findHarmonicModelIndex(model))
                sheet += 'gen_'
        if net.GetIndMachines() != {}:
            if findHarmonicModelIndex(model) != -1:
                HM.SetIValue(HM.HarmonicGlobalMotorModel, findHarmonicModelIndex(model))
                sheet += 'imach_'

        if calculation_type in ['Penetration', 'Voltage Waveform']:
            harmonic_study = net.DoHarmPenetration()

        else:
            harmonic_study = net.DoHarmSensitivity()
        
        busbars_data, impedance_orders = fetchBusbarsHarmonicsData(net, ipsanetwork, calculation_type)
        generators_data = generatorHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders)
        loads_data = loadHarmonicsData(net, ipsanetwork, calculation_type)
        induction_machine_data = inductionMachineHarmonicsData(net, ipsanetwork, calculation_type)
        harmonic_filters_data = filterHarmonicsData(net, ipsanetwork, calculation_type)
        lines_data = lineHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders)
        transformers_data = transformerHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders)
        ThreeWtransformers_data = _3WtransformerHarmonicsData(net, ipsanetwork, calculation_type, impedance_orders)            
        
        dict_harm = {
            'harm calc type': calculation_type[:3],
            'harm sequence': sequence[:3],
            'harm model': model[:3], #sheet +
            'Busbars': busbars_data,
            'Generators': generators_data,
            'Loads': loads_data,
            'Induction machine': induction_machine_data,
            'Harmonic Filters' : harmonic_filters_data,
            'Lines and cables': lines_data,
            'Transformers': transformers_data,
            'Three Winding Transformers': ThreeWtransformers_data
            }
        filtered_dict_harm = {k: v for k, v in dict_harm.items() if v is not False}
        harmonic_results_data.append(filtered_dict_harm)

    folder = os.path.dirname(cwd)
    folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
    folder_path.mkdir(parents=True, exist_ok=True)
    sub1_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'Harmonic Analysis' 
    sub1_folder_path.mkdir(parents=True, exist_ok=True)
    harmonics_calculation_type = ['Penetration', 'Voltage Waveform', 'Impedance Scan'] 
    harmonics_sequence = ['Default', 'Positive', 'Zero']
    harmonic_models = ['Polynomial', 'sqrt(h).R', 'Constant X by R']
    load_override_models = ['Series R-X', 'Parallel R-X (1)', 'Parallel R-X (2)', 'X plus parallel R-X']


    file_paths = []
    for calculation_type in harmonics_calculation_type:
        harmonic_results_data = []
        print("Harmonics calculation type:", calculation_type)
        sub2_folder_path = sub1_folder_path / calculation_type
        sub2_folder_path.mkdir(parents=True, exist_ok=True)
        for sequence in harmonics_sequence:
            for model in harmonic_models:
                if net.GetLoads() != {}:
                    for load_model in load_override_models:
                        generateReport(harmonic_results_data, calculation_type, sequence, load_model, model)
                else:
                    generateReport(harmonic_results_data, calculation_type, sequence, None, model)

        try:
            # file_paths = []
            data = ['harm calc type', 'harm sequence', 'harm model']
            excel = {}
            for harmonics in harmonic_results_data:
                harmonics_type = harmonics['harm calc type']
                harmonics_value = harmonics['harm sequence']
                harmonics_model = harmonics['harm model']
                sheet_name = f"{harmonics_type}_{harmonics_value}_{harmonics_model}"
                for key, value in harmonics.items():
                    if key in data:
                        continue
                    file_name = (f"{IPSA_file_name[:-4]}_{harmonics_type}_{key}_{ipsa_version}.xlsx")
                    file_path = sub2_folder_path / file_name
                    
                    if key not in excel:
                        excel[key] = pd.ExcelWriter(file_path, engine='openpyxl')
                        file_paths.append(file_path)
                    if type(value) == list:
                        df = pd.DataFrame(value)
                    else:
                        df = pd.read_csv(value, sep='\t')
                    df.to_excel(excel[key], sheet_name=sheet_name[:33], index=False)
            for w in excel.values():
                w.close()
            # all_paths.append(file_paths)
        except Exception as e:
            print(e)
            print("Close the excel file before running script")

    return file_paths #[i for i in items for items in all_paths]        


#For testing of Harmonic Study function :-
# ipsascript = ipsa.GetInterface()
# net = ipsascript.ReadFile(r"C:\Users\ruben.pulayath\Downloads\harmonics.i3f")
# ipsa_version = ipsascript.GetVersion()
# IPSA_file_name= ipsascript.GetNetworkFileName()

# cwd = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.abspath(cwd))
# sys.path.extend([x[0] for x in os.walk(sys.exec_prefix + r"/Lib")])
# runHarmonics(ipsascript, net, cwd, ipsa_version, IPSA_file_name)