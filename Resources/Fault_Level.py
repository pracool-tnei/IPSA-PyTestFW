from pathlib import Path
import os
import random
import ipsa
import pandas as pd

from Logger import debug, info,error

def run_fault_level(net, cwd, ipsa_version, IPSA_file_name, fault_study_type):
    def find_fault_study_type_index(fault_study_type):
        match fault_study_type:
            case 'Fault levels on all busbars':
                fault_study_type_index = 1
            case 'Fault levels on selected busbars':
                fault_study_type_index = 2
            case 'Fault on single busbar':
                fault_study_type_index = 3
            case 'Fault along a line':
                fault_study_type_index = 4
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

    def find_fault_value_index(fault_value):
        match fault_value:
            case 'SymRMS':
                fault_type_index = 1
            case 'Peak':
                fault_type_index = 2
            case 'AsymRMS':
                fault_type_index = 3
            case 'BusWave':
                fault_type_index = 4
            case 'BranchWave':
                fault_type_index = 5
            case _:
                fault_type_index = -1
        return fault_type_index

    def fetch_busbars_fault_data(net, fault_value, cdp):
        dict_busbars = net.GetBusbars()
        if dict_busbars =={}:
            return False
        busbars_data_list = []

        for bus in dict_busbars.values():
            bus_name = bus.GetSValue(ipsa.IscBusbar.Name)
            ac_mag_ka = bus.GetFaultACComponentkA()
            dc_mag_ka = bus.GetFaultDCComponentkA()
            dc_percentage=bus.GetFaultDCPercentage()
            #dc_percentage=0
            second_harmonic_mag_ka = bus.GetFault2HComponentkA()
            dc_x = bus.GetFaultDCTheveninX()
            dc_r = bus.GetFaultDCTheveninR()
            dc_xr = dc_x / dc_r if dc_r != 0 else 0
            red_mag_ka = bus.GetFaultRedComponentkA()
            red_angle_degree = bus.GetFaultRedComponentAngleDeg()
            yellow_mag_ka = bus.GetFaultYellowComponentkA()
            yellow_angle_degree = bus.GetFaultYellowComponentAngleDeg()
            blue_mag_ka = bus.GetFaultBlueComponentkA()
            blue_angle_degree = bus.GetFaultBlueComponentAngleDeg()
            positive_mag_ka = bus.GetFaultPositiveComponentkA()
            positive_angle_degree = bus.GetFaultPositiveComponentAngleDeg()
            negative_mag_ka = bus.GetFaultNegativeComponentkA()
            negative_angle_degree = bus.GetFaultNegativeComponentAngleDeg()
            zero_mag_ka = bus.GetFaultZeroComponentkA()
            zero_angle_degree = bus.GetFaultZeroComponentAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_bus_data = {
                    'Name': bus_name,
                    'AC Mag. (kA)': ac_mag_ka,
                    'DC Mag. (kA)': dc_mag_ka,
                    'DC %': dc_percentage,
                    'Second Harm. (kA)': second_harmonic_mag_ka,
                    'DC X / R(Driving point)': dc_xr,
                    'DC Thevenin X': dc_x,
                    'DC Thevenin R': dc_r,
                    'Red Phase Mag. (kA)': red_mag_ka,
                    'Red Phase Angle (deg)': red_angle_degree,
                    'Yellow Phase Mag. (kA)': yellow_mag_ka,
                    'Yellow Phase Angle (deg)': yellow_angle_degree,
                    'Blue Phase Mag. (kA)': blue_mag_ka,
                    'Blue Phase Angle (deg)': blue_angle_degree,
                    'Include CDPs': cdp
                }
            elif fault_value in ['SymRMS']:
                dict_bus_data = {
                    'Name': bus_name,
                    'AC Mag. (kA)': ac_mag_ka,
                    'DC Mag. (kA)': dc_mag_ka,
                    'DC %': dc_percentage,
                    'Second Harm. (kA)': second_harmonic_mag_ka,
                    'DC X / R(Driving point)': dc_xr,
                    'DC Thevenin X': dc_x,
                    'DC Thevenin R': dc_r,
                    'Red Phase Mag. (kA)': red_mag_ka,
                    'Red Phase Angle (deg)': red_angle_degree,
                    'Yellow Phase Mag. (kA)': yellow_mag_ka,
                    'Yellow Phase Angle (deg)': yellow_angle_degree,
                    'Blue Phase Mag. (kA)': blue_mag_ka,
                    'Blue Phase Angle (deg)': blue_angle_degree,
                    'Positive Phase Mag. (kA)': positive_mag_ka,
                    'Positive Phase Angle (deg)': positive_angle_degree,
                    'Negative Phase Mag. (kA)': negative_mag_ka,
                    'Negative Phase Angle (deg)': negative_angle_degree,
                    'Zero Phase Mag. (kA)': zero_mag_ka,
                    'Zero Phase Angle (deg)': zero_angle_degree,
                    'Include CDPs': cdp
                }
            busbars_data_list.append(dict_bus_data)
        return busbars_data_list
    
    #busbars-single
    def fault_on_single_busbar_data(net, fault_value, cdp):
        dict_busbars = net.GetBusbars()
        if dict_busbars =={}:
            return False
        busbars_data_list = []

        for bus in dict_busbars.values():
            bus_name = bus.GetSValue(ipsa.IscBusbar.Name)
            red_phase_voltage = bus.GetFaultRedVoltagePU()
            red_phase_angle = bus.GetFaultRedVoltageAngleDeg()
            yellow_phase_voltage = bus.GetFaultYellowVoltagePU()
            yellow_phase_angle = bus.GetFaultYellowVoltageAngleDeg()
            blue_phase_voltage = bus.GetFaultBlueVoltagePU()
            blue_phase_angle = bus.GetFaultBlueVoltageAngleDeg()
            positive_seq_voltage = bus.GetFaultPositiveVoltagePU()
            positive_seq_angle = bus.GetFaultPositiveVoltageAngleDeg()
            negative_seq_voltage = bus.GetFaultNegativeVoltagePU()
            negative_seq_angle = bus.GetFaultNegativeVoltageAngleDeg()  
            zero_seq_voltage = bus.GetFaultZeroVoltagePU()
            zero_seq_angle = bus.GetFaultZeroVoltageAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_bus_data = {
                    'Name': bus_name,
                    'Red Phase Voltage (pu)': red_phase_voltage,
                    'Red Phase Angle (deg)': red_phase_angle,
                    'Yellow Phase Voltage (pu)': yellow_phase_voltage,
                    'Yellow Phase Angle (deg)': yellow_phase_angle,
                    'Blue Phase Voltage (pu)': blue_phase_voltage,
                    'Blue Phase Angle (deg)': blue_phase_angle,
                    'Include CDPs': cdp
                }
            
            elif fault_value in ['SymRMS']:
                dict_bus_data = {
                    'Name': bus_name,
                    'Red Phase Voltage (pu)': red_phase_voltage,
                    'Red Phase Angle (deg)': red_phase_angle,
                    'Yellow Phase Voltage (pu)': yellow_phase_voltage,
                    'Yellow Phase Angle (deg)': yellow_phase_angle,
                    'Blue Phase Voltage (pu)': blue_phase_voltage,
                    'Blue Phase Angle (deg)': blue_phase_angle,
                    'Positive Seq. Voltage (pu)': positive_seq_voltage,
                    'Positive Seq. Angle (deg)': positive_seq_angle,
                    'Negative Seq. Voltage (pu)': negative_seq_voltage,
                    'Negative Seq. Angle (deg)': negative_seq_angle,
                    'Zero Seq. Voltage (pu)': zero_seq_voltage,
                    'Zero Seq. Angle (deg)': zero_seq_angle,
                    'Include CDPs': cdp
                }

            busbars_data_list.append(dict_bus_data)
        return busbars_data_list
    
    #generators-single
    def fault_on_single_generator_data(net, fault_value):
        dict_syn_machines = net.GetSynMachines()
        if dict_syn_machines =={}:
            return False
        generators_data_list = []

        for syn_machine in dict_syn_machines.values():
            generator_name = syn_machine.GetSValue(ipsa.IscSynMachine.Name)
            gen_ac_mag_ka = syn_machine.GetFaultACMagnitudekA()
            gen_dc_mag_ka = syn_machine.GetFaultDCMagnitudekA()
            gen_dc_percentage = syn_machine.GetFaultDCPC() 
            gen_second_harmonic_mag_ka = syn_machine.GetFaultSecondHarmonickA()
            gen_red_mag_ka = syn_machine.GetFaultRedMagnitudekA()
            gen_red_angle_degree = syn_machine.GetFaultRedAngleDeg()
            gen_yellow_mag_ka = syn_machine.GetFaultYellowMagnitudekA()
            gen_yellow_angle_degree = syn_machine.GetFaultYellowAngleDeg()
            gen_blue_mag_ka = syn_machine.GetFaultBlueMagnitudekA()
            gen_blue_angle_degree = syn_machine.GetFaultBlueAngleDeg()
            gen_pos_mag_ka = syn_machine.GetFaultPositiveMagnitudekA()
            gen_pos_angle_degree = syn_machine.GetFaultPositiveAngleDeg()
            gen_neg_mag_ka = syn_machine.GetFaultNegativeMagnitudekA()
            gen_neg_angle_degree = syn_machine.GetFaultNegativeAngleDeg()
            gen_zero_mag_ka = syn_machine.GetFaultZeroMagnitudekA()
            gen_zero_angle_degree = syn_machine.GetFaultZeroAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_gen_data = {
                    'Name': generator_name,
                    'AC Mag. (kA)': gen_ac_mag_ka,
                    'DC Mag. (kA)': gen_dc_mag_ka,
                    'DC %': gen_dc_percentage,
                    'Second Harm. (kA)': gen_second_harmonic_mag_ka,
                    'Red Phase Mag. (kA)': gen_red_mag_ka,
                    'Red Phase Angle (deg)': gen_red_angle_degree,
                    'Yellow Phase Mag. (kA)': gen_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': gen_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': gen_blue_mag_ka,
                    'Blue Phase Angle (deg)': gen_blue_angle_degree
                }
            
            elif fault_value in ['SymRMS']:
                dict_gen_data = {
                    'Name': generator_name,
                    'AC Mag. (kA)': gen_ac_mag_ka,
                    'DC Mag. (kA)': gen_dc_mag_ka,
                    'DC %': gen_dc_percentage,
                    'Second Harm. (kA)': gen_second_harmonic_mag_ka,
                    'Red Phase Mag. (kA)': gen_red_mag_ka,
                    'Red Phase Angle (deg)': gen_red_angle_degree,
                    'Yellow Phase Mag. (kA)': gen_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': gen_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': gen_blue_mag_ka,
                    'Blue Phase Angle (deg)': gen_blue_angle_degree,
                    'Positive Phase Mag. (kA)': gen_pos_mag_ka,
                    'Positive Phase Angle (deg)': gen_pos_angle_degree,
                    'Negative Phase Mag. (kA)': gen_neg_mag_ka,
                    'Negative Phase Angle (deg)': gen_neg_angle_degree,
                    'Zero Phase Mag. (kA)': gen_zero_mag_ka,
                    'Zero Phase Angle (deg)': gen_zero_angle_degree,
                }

            generators_data_list.append(dict_gen_data)
        return generators_data_list
    
    #grid infeed - single
    def fault_on_single_grid_infeed_data(net, fault_value):
        dict_grid_infeeds = net.GetGridInfeeds()
        if dict_grid_infeeds =={}:
            return False
        grid_infeeds_data_list = []

        for grid_infeed in dict_grid_infeeds.values():
            grid_name = grid_infeed.GetSValue(ipsa.IscGridInfeed.Name)
            grid_ac_mag_ka = grid_infeed.GetFaultACMagnitudekA()
            grid_dc_mag_ka = grid_infeed.GetFaultDCMagnitudekA()
            grid_dc_percentage = grid_infeed.GetFaultDCPC() 
            grid_second_harmonic_mag_ka = grid_infeed.GetFaultSecondHarmonickA()
            grid_red_mag_ka = grid_infeed.GetFaultRedMagnitudekA()
            grid_red_angle_degree = grid_infeed.GetFaultRedAngleDeg()
            grid_yellow_mag_ka = grid_infeed.GetFaultYellowMagnitudekA()
            grid_yellow_angle_degree = grid_infeed.GetFaultYellowAngleDeg()
            grid_blue_mag_ka = grid_infeed.GetFaultBlueMagnitudekA()
            grid_blue_angle_degree = grid_infeed.GetFaultBlueAngleDeg()
            grid_pos_mag_ka = grid_infeed.GetFaultPositiveMagnitudekA()
            grid_pos_angle_degree = grid_infeed.GetFaultPositiveAngleDeg()
            grid_neg_mag_ka = grid_infeed.GetFaultNegativeMagnitudekA()
            grid_neg_angle_degree = grid_infeed.GetFaultNegativeAngleDeg()
            grid_zero_mag_ka = grid_infeed.GetFaultZeroMagnitudekA()
            grid_zero_angle_degree = grid_infeed.GetFaultZeroAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_grid_infeed_data = {
                    'Name': grid_name,
                    'AC Mag. (kA)': grid_ac_mag_ka,
                    'DC Mag. (kA)': grid_dc_mag_ka,
                    'DC %': grid_dc_percentage,
                    'Second Harm. (kA)': grid_second_harmonic_mag_ka,
                    'Red Phase Mag. (kA)': grid_red_mag_ka,
                    'Red Phase Angle (deg)': grid_red_angle_degree,
                    'Yellow Phase Mag. (kA)': grid_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': grid_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': grid_blue_mag_ka,
                    'Blue Phase Angle (deg)': grid_blue_angle_degree
                    }
            
            elif fault_value in ['SymRMS']:
                dict_grid_infeed_data = {
                    'Name': grid_name,
                    'AC Mag. (kA)': grid_ac_mag_ka,
                    'DC Mag. (kA)': grid_dc_mag_ka,
                    'DC %': grid_dc_percentage,
                    'Second Harm. (kA)': grid_second_harmonic_mag_ka,
                    'Red Phase Mag. (kA)': grid_red_mag_ka,
                    'Red Phase Angle (deg)': grid_red_angle_degree,
                    'Yellow Phase Mag. (kA)': grid_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': grid_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': grid_blue_mag_ka,
                    'Blue Phase Angle (deg)': grid_blue_angle_degree,
                    'Positive Phase Mag. (kA)': grid_pos_mag_ka,
                    'Positive Phase Angle (deg)': grid_pos_angle_degree,
                    'Negative Phase Mag. (kA)': grid_neg_mag_ka,
                    'Negative Phase Angle (deg)': grid_neg_angle_degree,
                    'Zero Phase Mag. (kA)': grid_zero_mag_ka,
                    'Zero Phase Angle (deg)': grid_zero_angle_degree,
                }

            grid_infeeds_data_list.append(dict_grid_infeed_data)
        return grid_infeeds_data_list
    
    #Induction machine - single
    def fault_on_single_induction_machine_data(net, fault_value):
        dict_induction_machines = net.GetIndMachines()
        if dict_induction_machines =={}:
            return False
        induction_machines_data_list = []

        for induction_machine in dict_induction_machines.values():
            ind_machine_name = induction_machine.GetSValue(ipsa.IscIndMachine.Name)
            ind_machine_ac_mag_ka = induction_machine.GetFaultACMagnitudekA()
            ind_machine_dc_mag_ka = induction_machine.GetFaultDCMagnitudekA()
            ind_machine_dc_percentage = induction_machine.GetFaultDCPC() 
            # ind_machine_second_harmonic_mag_ka = induction_machine.GetFaultSecondHarmonickA()
            ind_machine_red_mag_ka = induction_machine.GetFaultRedMagnitudekA()
            ind_machine_red_angle_degree = induction_machine.GetFaultRedAngleDeg()
            ind_machine_yellow_mag_ka = induction_machine.GetFaultYellowMagnitudekA()
            ind_machine_yellow_angle_degree = induction_machine.GetFaultYellowAngleDeg()
            ind_machine_blue_mag_ka = induction_machine.GetFaultBlueMagnitudekA()
            ind_machine_blue_angle_degree = induction_machine.GetFaultBlueAngleDeg()
            ind_machine_pos_mag_ka = induction_machine.GetFaultPositiveMagnitudekA()
            ind_machine_pos_angle_degree = induction_machine.GetFaultPositiveAngleDeg()
            ind_machine_neg_mag_ka = induction_machine.GetFaultNegativeMagnitudekA()
            ind_machine_neg_angle_degree = induction_machine.GetFaultNegativeAngleDeg()
            ind_machine_zero_mag_ka = induction_machine.GetFaultZeroMagnitudekA()
            ind_machine_zero_angle_degree = induction_machine.GetFaultZeroAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_ind_machine_data = {
                    'Name': ind_machine_name,
                    'AC Mag. (kA)': ind_machine_ac_mag_ka,
                    'DC Mag. (kA)': ind_machine_dc_mag_ka,
                    'DC %': ind_machine_dc_percentage,
                    # 'Second Harm. (kA)': ind_machine_second_harmonic_mag_ka,
                    'Red Phase Mag. (kA)': ind_machine_red_mag_ka,
                    'Red Phase Angle (deg)': ind_machine_red_angle_degree,
                    'Yellow Phase Mag. (kA)': ind_machine_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': ind_machine_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': ind_machine_blue_mag_ka,
                    'Blue Phase Angle (deg)': ind_machine_blue_angle_degree
                }
            
            elif fault_value in ['SymRMS']:
                dict_ind_machine_data = {
                    'Name': ind_machine_name,
                    'AC Mag. (kA)': ind_machine_ac_mag_ka,
                    'DC Mag. (kA)': ind_machine_dc_mag_ka,
                    'DC %': ind_machine_dc_percentage,
                    # 'Second Harm. (kA)': ind_machine_second_harmonic_mag_ka,/
                    'Red Phase Mag. (kA)': ind_machine_red_mag_ka,
                    'Red Phase Angle (deg)': ind_machine_red_angle_degree,
                    'Yellow Phase Mag. (kA)': ind_machine_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': ind_machine_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': ind_machine_blue_mag_ka,
                    'Blue Phase Angle (deg)': ind_machine_blue_angle_degree,
                    'Positive Phase Mag. (kA)': ind_machine_pos_mag_ka,
                    'Positive Phase Angle (deg)': ind_machine_pos_angle_degree,
                    'Negative Phase Mag. (kA)': ind_machine_neg_mag_ka,
                    'Negative Phase Angle (deg)': ind_machine_neg_angle_degree,
                    'Zero Phase Mag. (kA)': ind_machine_zero_mag_ka,
                    'Zero Phase Angle (deg)': ind_machine_zero_angle_degree,
                }

            induction_machines_data_list.append(dict_ind_machine_data)
        return induction_machines_data_list
    
    #Branches - single
    def fault_on_single_line_data(net, fault_value):
        dict_branches = net.GetBranches()
        if dict_branches=={}:
            return False
        branches_data_list = []

        for branch in dict_branches.values():
            branch_from_busbar=branch.GetSValue(ipsa.IscBranch.FromBusName)
            branch_to_busbar=branch.GetSValue(ipsa.IscBranch.ToBusName)
            branch_from_nom_voltage_kv = net.GetBusbar(branch_from_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
            branch_to_nom_voltage_kv = net.GetBusbar(branch_to_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
            branch_name = branch.GetSValue(ipsa.IscBranch.Name)
            branch_status=branch.GetIValue(ipsa.IscBranch.Status)
            branch_red_mag_ka = branch.GetFaultRedComponentkA()
            branch_red_angle_degree = branch.GetFaultRedComponentAngleDeg()
            branch_yellow_mag_ka = branch.GetFaultYellowComponentkA()
            branch_yellow_angle_degree = branch.GetFaultYellowComponentAngleDeg()
            branch_blue_mag_ka = branch.GetFaultBlueComponentkA()
            branch_blue_angle_degree = branch.GetFaultBlueComponentAngleDeg()
            branch_pos_mag_ka = branch.GetFaultPositiveComponentkA()
            branch_pos_angle_degree = branch.GetFaultPositiveComponentAngleDeg()
            branch_neg_mag_ka = branch.GetFaultNegativeComponentkA()
            branch_neg_angle_degree = branch.GetFaultNegativeComponentAngleDeg()
            branch_zero_mag_ka = branch.GetFaultZeroComponentkA()
            branch_zero_angle_degree = branch.GetFaultZeroComponentAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_branch_data = {
                    'From Busbar': branch_from_busbar,
                    'To Busbar': branch_to_busbar,
                    'From Nominal Voltage (kV)' : branch_from_nom_voltage_kv,
                    'To Nominal Voltage (kV)' : branch_to_nom_voltage_kv,
                    'Name': branch_name,
                    'Status': branch_status,
                    'Red Phase Mag. (kA)': branch_red_mag_ka,
                    'Red Phase Angle (deg)': branch_red_angle_degree,
                    'Yellow Phase Mag. (kA)': branch_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': branch_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': branch_blue_mag_ka,
                    'Blue Phase Angle (deg)': branch_blue_angle_degree
                }
            elif fault_value in ['SymRMS']:
                dict_branch_data = {
                    'From Busbar': branch_from_busbar,
                    'To Busbar': branch_to_busbar,
                    'From Nominal Voltage (kV)' : branch_from_nom_voltage_kv,
                    'To Nominal Voltage (kV)' : branch_to_nom_voltage_kv,
                    'Name': branch_name,
                    'Status': branch_status,
                    'Red Phase Mag. (kA)': branch_red_mag_ka,
                    'Red Phase Angle (deg)': branch_red_angle_degree,
                    'Yellow Phase Mag. (kA)': branch_yellow_mag_ka,
                    'Yellow Phase Angle (deg)': branch_yellow_angle_degree,
                    'Blue Phase Mag. (kA)': branch_blue_mag_ka,
                    'Blue Phase Angle (deg)': branch_blue_angle_degree,
                    'Positive Phase Mag. (kA)': branch_pos_mag_ka,
                    'Positive Phase Angle (deg)': branch_pos_angle_degree,
                    'Negative Phase Mag. (kA)': branch_neg_mag_ka,
                    'Negative Phase Angle (deg)': branch_neg_angle_degree,
                    'Zero Phase Mag. (kA)': branch_zero_mag_ka,
                    'Zero Phase Angle (deg)': branch_zero_angle_degree,
                }

            branches_data_list.append(dict_branch_data)
        return branches_data_list
    
    #Transformers - single
    def fault_on_single_transformer_data(net, fault_value):
        dict_transformer = net.GetTransformers()
        if dict_transformer =={}:
            return False 
        transformers_data_list = []

        for transformer in dict_transformer.values():
            transformer_from_busbar=transformer.GetSValue(ipsa.IscTransformer.FromBusName)
            transformer_to_busbar=transformer.GetSValue(ipsa.IscTransformer.ToBusName)
            transformer_from_nom_voltage_kv = net.GetBusbar(transformer_from_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
            transformer_to_nom_voltage_kv = net.GetBusbar(transformer_to_busbar).GetDValue(ipsa.IscBusbar.NomVoltkV)
            transformer_name = transformer.GetSValue(ipsa.IscTransformer.Name)
            transformer_status=transformer.GetIValue(ipsa.IscBranch.Status) #Status taken from IscBranch
            transformer_red_from_mag_ka = transformer.GetFaultRedComponentFromkA()
            transformer_red_from_angle_degree = transformer.GetFaultRedComponentFromAngleDeg()
            transformer_yellow_from_mag_ka = transformer.GetFaultYellowComponentFromkA()
            transformer_yellow_from_angle_degree = transformer.GetFaultYellowComponentFromAngleDeg()
            transformer_blue_from_mag_ka = transformer.GetFaultBlueComponentFromkA()
            transformer_blue_from_angle_degree = transformer.GetFaultBlueComponentFromAngleDeg()
            transformer_red_to_mag_ka = transformer.GetFaultRedComponentTokA()
            transformer_red_to_angle_degree = transformer.GetFaultRedComponentToAngleDeg()
            transformer_yellow_to_mag_ka = transformer.GetFaultYellowComponentTokA()
            transformer_yellow_to_angle_degree = transformer.GetFaultYellowComponentToAngleDeg()
            transformer_blue_to_mag_ka = transformer.GetFaultBlueComponentTokA()
            transformer_blue_to_angle_degree = transformer.GetFaultBlueComponentToAngleDeg()
            transformer_pos_from_mag_ka = transformer.GetFaultPositiveComponentFromkA()
            transformer_pos_from_angle_degree = transformer.GetFaultPositiveComponentFromAngleDeg()
            transformer_neg_from_mag_ka = transformer.GetFaultNegativeComponentFromkA()
            transformer_neg_from_angle_degree = transformer.GetFaultNegativeComponentFromAngleDeg()
            transformer_zero_from_mag_ka = transformer.GetFaultZeroComponentFromkA()
            transformer_zero_from_angle_degree = transformer.GetFaultZeroComponentFromAngleDeg()
            transformer_pos_to_mag_ka = transformer.GetFaultPositiveComponentTokA()
            transformer_pos_to_angle_degree = transformer.GetFaultPositiveComponentToAngleDeg()
            transformer_neg_to_mag_ka = transformer.GetFaultNegativeComponentTokA()
            transformer_neg_to_angle_degree = transformer.GetFaultNegativeComponentToAngleDeg()
            transformer_zero_to_mag_ka = transformer.GetFaultZeroComponentTokA()
            transformer_zero_to_angle_degree = transformer.GetFaultZeroComponentToAngleDeg()
            if fault_value in ['Peak', 'AsymRMS']:
                dict_transformer_data = {
                    'From Busbar': transformer_from_busbar,
                    'To Busbar': transformer_to_busbar,
                    'From Nominal Voltage (kV)' : transformer_from_nom_voltage_kv,
                    'To Nominal Voltage (kV)' : transformer_to_nom_voltage_kv,
                    'Name': transformer_name,
                    'Status': transformer_status,
                    'Red Phase From Mag. (kA)': transformer_red_from_mag_ka,
                    'Red Phase From Angle (deg)': transformer_red_from_angle_degree,
                    'Yellow Phase From Mag. (kA)': transformer_yellow_from_mag_ka,
                    'Yellow Phase From Angle (deg)': transformer_yellow_from_angle_degree,
                    'Blue Phase From Mag. (kA)': transformer_blue_from_mag_ka,
                    'Blue Phase From Angle (deg)': transformer_blue_from_angle_degree,
                    'Red Phase To Mag. (kA)': transformer_red_to_mag_ka,
                    'Red Phase To Angle (deg)': transformer_red_to_angle_degree,
                    'Yellow Phase To Mag. (kA)': transformer_yellow_to_mag_ka,
                    'Yellow Phase To Angle (deg)': transformer_yellow_to_angle_degree,
                    'Blue Phase To Mag. (kA)': transformer_blue_to_mag_ka,
                    'Blue Phase To Angle (deg)': transformer_blue_to_angle_degree
                }
            elif fault_value in ['SymRMS']:
                dict_transformer_data = {
                    'From Busbar': transformer_from_busbar,
                    'To Busbar': transformer_to_busbar,
                    'From Nominal Voltage (kV)' : transformer_from_nom_voltage_kv,
                    'To Nominal Voltage (kV)' : transformer_to_nom_voltage_kv,
                    'Name': transformer_name,
                    'Status': transformer_status,
                    'Red Phase From Mag. (kA)': transformer_red_from_mag_ka,
                    'Red Phase From Angle (deg)': transformer_red_from_angle_degree,
                    'Yellow Phase From Mag. (kA)': transformer_yellow_from_mag_ka,
                    'Yellow Phase From Angle (deg)': transformer_yellow_from_angle_degree,
                    'Blue Phase From Mag. (kA)': transformer_blue_from_mag_ka,
                    'Blue Phase From Angle (deg)': transformer_blue_from_angle_degree,
                    'Positive Phase From Mag. (kA)': transformer_pos_from_mag_ka,
                    'Positive Phase From Angle (deg)': transformer_pos_from_angle_degree,
                    'Negative Phase From Mag. (kA)': transformer_neg_from_mag_ka,
                    'Negative Phase From Angle (deg)': transformer_neg_from_angle_degree,
                    'Zero Phase From Mag. (kA)': transformer_zero_from_mag_ka,
                    'Zero Phase From Angle (deg)': transformer_zero_from_angle_degree,
                    'Red Phase To Mag. (kA)': transformer_red_to_mag_ka,
                    'Red Phase To Angle (deg)': transformer_red_to_angle_degree,
                    'Yellow Phase To Mag. (kA)': transformer_yellow_to_mag_ka,
                    'Yellow Phase To Angle (deg)': transformer_yellow_to_angle_degree,
                    'Blue Phase To Mag. (kA)': transformer_blue_to_mag_ka,
                    'Blue Phase To Angle (deg)': transformer_blue_to_angle_degree,
                    'Positive Phase To Mag. (kA)': transformer_pos_to_mag_ka,
                    'Positive Phase To Angle (deg)': transformer_pos_to_angle_degree,
                    'Negative Phase To Mag. (kA)': transformer_neg_to_mag_ka,
                    'Negative Phase To Angle (deg)': transformer_neg_to_angle_degree,
                    'Zero Phase To Mag. (kA)': transformer_zero_to_mag_ka,
                    'Zero Phase To Angle (deg)': transformer_zero_to_angle_degree,
                }

            transformers_data_list.append(dict_transformer_data)
        return transformers_data_list
    
    #3W Transformers - single
    def fault_on_single_3Wtransformer_data(net, fault_value):
        dict_ThreeWtransformer = net.Get3WTransformers()
        if dict_ThreeWtransformer=={}:
            return False
        ThreeWtransformers_data_list = []

        for ThreeWtransformer in dict_ThreeWtransformer.values():
            ThreeWtransformer_primary_busbar = ThreeWtransformer.GetSValue(ipsa.Isc3WTransformer.FromBusName)
            ThreeWtransformer_secondary_busbar = ThreeWtransformer.GetSValue(ipsa.Isc3WTransformer.ToBusName)
            ThreeWtransformer_tertiary_busbar = ThreeWtransformer.GetSValue(ipsa.Isc3WTransformer.ThreeBusName)
            ThreeWtransformer_name = ThreeWtransformer.GetSValue(ipsa.Isc3WTransformer.Name)
            ThreeWtransformer_status = ThreeWtransformer.GetIValue(ipsa.Isc3WTransformer.Status)
            ThreeWtransformer_red_primary_mag_ka = ThreeWtransformer.GetFaultRedMagnitudekA(1)
            ThreeWtransformer_red_primary_angle_degree = ThreeWtransformer.GetFaultRedAngleDeg(1)
            ThreeWtransformer_yellow_primary_mag_ka = ThreeWtransformer.GetFaultYellowMagnitudekA(1)
            ThreeWtransformer_yellow_primary_angle_degree = ThreeWtransformer.GetFaultYellowAngleDeg(1)
            ThreeWtransformer_blue_primary_mag_ka = ThreeWtransformer.GetFaultBlueMagnitudekA(1)
            ThreeWtransformer_blue_primary_angle_degree = ThreeWtransformer.GetFaultBlueAngleDeg(1)
            ThreeWtransformer_red_secondary_mag_ka = ThreeWtransformer.GetFaultRedMagnitudekA(2)
            ThreeWtransformer_red_secondary_angle_degree = ThreeWtransformer.GetFaultRedAngleDeg(2)
            ThreeWtransformer_yellow_secondary_mag_ka = ThreeWtransformer.GetFaultYellowMagnitudekA(2)
            ThreeWtransformer_yellow_secondary_angle_degree = ThreeWtransformer.GetFaultYellowAngleDeg(2)
            ThreeWtransformer_blue_secondary_mag_ka = ThreeWtransformer.GetFaultBlueMagnitudekA(2)
            ThreeWtransformer_blue_secondary_angle_degree = ThreeWtransformer.GetFaultBlueAngleDeg(2)
            ThreeWtransformer_red_tertiary_mag_ka = ThreeWtransformer.GetFaultRedMagnitudekA(3)
            ThreeWtransformer_red_tertiary_angle_degree = ThreeWtransformer.GetFaultRedAngleDeg(3)
            ThreeWtransformer_yellow_tertiary_mag_ka = ThreeWtransformer.GetFaultYellowMagnitudekA(3)
            ThreeWtransformer_yellow_tertiary_angle_degree = ThreeWtransformer.GetFaultYellowAngleDeg(3)
            ThreeWtransformer_blue_tertiary_mag_ka = ThreeWtransformer.GetFaultBlueMagnitudekA(3)
            ThreeWtransformer_blue_tertiary_angle_degree = ThreeWtransformer.GetFaultBlueAngleDeg(3)
            ThreeWtransformer_positive_primary_mag_ka = ThreeWtransformer.GetFaultPositiveMagnitudekA(1)
            ThreeWtransformer_positive_primary_angle_degree = ThreeWtransformer.GetFaultPositiveAngleDeg(1)
            ThreeWtransformer_negative_primary_mag_ka = ThreeWtransformer.GetFaultNegativeMagnitudekA(1)
            ThreeWtransformer_negative_primary_angle_degree = ThreeWtransformer.GetFaultNegativeAngleDeg(1)
            ThreeWtransformer_zero_primary_mag_ka = ThreeWtransformer.GetFaultZeroMagnitudekA(1)
            ThreeWtransformer_zero_primary_angle_degree = ThreeWtransformer.GetFaultZeroAngleDeg(1)
            ThreeWtransformer_positive_secondary_mag_ka = ThreeWtransformer.GetFaultPositiveMagnitudekA(2)
            ThreeWtransformer_positive_secondary_angle_degree = ThreeWtransformer.GetFaultPositiveAngleDeg(2)
            ThreeWtransformer_negative_secondary_mag_ka = ThreeWtransformer.GetFaultNegativeMagnitudekA(2)
            ThreeWtransformer_negative_secondary_angle_degree = ThreeWtransformer.GetFaultNegativeAngleDeg(2)
            ThreeWtransformer_zero_secondary_mag_ka = ThreeWtransformer.GetFaultZeroMagnitudekA(2)
            ThreeWtransformer_zero_secondary_angle_degree = ThreeWtransformer.GetFaultZeroAngleDeg(2)
            ThreeWtransformer_positive_tertiary_mag_ka = ThreeWtransformer.GetFaultPositiveMagnitudekA(3)
            ThreeWtransformer_positive_tertiary_angle_degree = ThreeWtransformer.GetFaultPositiveAngleDeg(3)
            ThreeWtransformer_negative_tertiary_mag_ka = ThreeWtransformer.GetFaultNegativeMagnitudekA(3)
            ThreeWtransformer_negative_tertiary_angle_degree = ThreeWtransformer.GetFaultNegativeAngleDeg(3)
            ThreeWtransformer_zero_tertiary_mag_ka = ThreeWtransformer.GetFaultZeroMagnitudekA(3)
            ThreeWtransformer_zero_tertiary_angle_degree = ThreeWtransformer.GetFaultZeroAngleDeg(3)
            if fault_value in ['Peak', 'AsymRMS']:
                dict_ThreeWtransformer_data = {
                    'Primary Busbar': ThreeWtransformer_primary_busbar,
                    'Secondary Busbar': ThreeWtransformer_secondary_busbar,
                    'Tertiary Busbar': ThreeWtransformer_tertiary_busbar,
                    'Name': ThreeWtransformer_name,
                    'Status': ThreeWtransformer_status,
                    'Red Phase Primary Mag. (kA)': ThreeWtransformer_red_primary_mag_ka,
                    'Red Phase Primary Angle (deg)': ThreeWtransformer_red_primary_angle_degree,
                    'Yellow Phase Primary Mag. (kA)': ThreeWtransformer_yellow_primary_mag_ka,
                    'Yellow Phase Primary Angle (deg)': ThreeWtransformer_yellow_primary_angle_degree,
                    'Blue Phase Primary Mag. (kA)': ThreeWtransformer_blue_primary_mag_ka,
                    'Blue Phase Primary Angle (deg)': ThreeWtransformer_blue_primary_angle_degree,
                    'Red Phase Secondary Mag. (kA)': ThreeWtransformer_red_secondary_mag_ka,
                    'Red Phase Secondary Angle (deg)': ThreeWtransformer_red_secondary_angle_degree,
                    'Yellow Phase Secondary Mag. (kA)': ThreeWtransformer_yellow_secondary_mag_ka,
                    'Yellow Phase Secondary Angle (deg)': ThreeWtransformer_yellow_secondary_angle_degree,
                    'Blue Phase Secondary Mag. (kA)': ThreeWtransformer_blue_secondary_mag_ka,
                    'Blue Phase Secondary Angle (deg)': ThreeWtransformer_blue_secondary_angle_degree,
                    'Red Phase Tertiary Mag. (kA)': ThreeWtransformer_red_tertiary_mag_ka,
                    'Red Phase Tertiary Angle (deg)': ThreeWtransformer_red_tertiary_angle_degree,
                    'Yellow Phase Tertiary Mag. (kA)': ThreeWtransformer_yellow_tertiary_mag_ka,
                    'Yellow Phase Tertiary Angle (deg)': ThreeWtransformer_yellow_tertiary_angle_degree,
                    'Blue Phase Tertiary Mag. (kA)': ThreeWtransformer_blue_tertiary_mag_ka,
                    'Blue Phase Tertiary Angle (deg)': ThreeWtransformer_blue_tertiary_angle_degree,
                }
            elif fault_value in ['SymRMS']:
                dict_ThreeWtransformer_data = {
                    'Primary Busbar': ThreeWtransformer_primary_busbar,
                    'Secondary Busbar': ThreeWtransformer_secondary_busbar,
                    'Tertiary Busbar': ThreeWtransformer_tertiary_busbar,
                    'Name': ThreeWtransformer_name,
                    'Status': ThreeWtransformer_status,
                    'Red Phase Primary Mag. (kA)': ThreeWtransformer_red_primary_mag_ka,
                    'Red Phase Primary Angle (deg)': ThreeWtransformer_red_primary_angle_degree,
                    'Yellow Phase Primary Mag. (kA)': ThreeWtransformer_yellow_primary_mag_ka,
                    'Yellow Phase Primary Angle (deg)': ThreeWtransformer_yellow_primary_angle_degree,
                    'Blue Phase Primary Mag. (kA)': ThreeWtransformer_blue_primary_mag_ka,
                    'Blue Phase Primary Angle (deg)': ThreeWtransformer_blue_primary_angle_degree,
                    'Red Phase Secondary Mag. (kA)': ThreeWtransformer_red_secondary_mag_ka,
                    'Red Phase Secondary Angle (deg)': ThreeWtransformer_red_secondary_angle_degree,
                    'Yellow Phase Secondary Mag. (kA)': ThreeWtransformer_yellow_secondary_mag_ka,
                    'Yellow Phase Secondary Angle (deg)': ThreeWtransformer_yellow_secondary_angle_degree,
                    'Blue Phase Secondary Mag. (kA)': ThreeWtransformer_blue_secondary_mag_ka,
                    'Blue Phase Secondary Angle (deg)': ThreeWtransformer_blue_secondary_angle_degree,
                    'Red Phase Tertiary Mag. (kA)': ThreeWtransformer_red_tertiary_mag_ka,
                    'Red Phase Tertiary Angle (deg)': ThreeWtransformer_red_tertiary_angle_degree,
                    'Yellow Phase Tertiary Mag. (kA)': ThreeWtransformer_yellow_tertiary_mag_ka,
                    'Yellow Phase Tertiary Angle (deg)': ThreeWtransformer_yellow_tertiary_angle_degree,
                    'Blue Phase Tertiary Mag. (kA)': ThreeWtransformer_blue_tertiary_mag_ka,
                    'Blue Phase Tertiary Angle (deg)': ThreeWtransformer_blue_tertiary_angle_degree,
                    'Positive Phase Primary Mag. (kA)': ThreeWtransformer_positive_primary_mag_ka,
                    'Positive Phase Primary Angle (deg)': ThreeWtransformer_positive_primary_angle_degree,
                    'Negative Phase Primary Mag. (kA)': ThreeWtransformer_negative_primary_mag_ka,
                    'Negative Phase Primary Angle (deg)': ThreeWtransformer_negative_primary_angle_degree,
                    'Zero Phase Primary Mag. (kA)': ThreeWtransformer_zero_primary_mag_ka,
                    'Zero Phase Primary Angle (deg)': ThreeWtransformer_zero_primary_angle_degree,
                    'Positive Phase Secondary Mag. (kA)': ThreeWtransformer_positive_secondary_mag_ka,
                    'Positive Phase Secondary Angle (deg)': ThreeWtransformer_positive_secondary_angle_degree,
                    'Negative Phase Secondary Mag. (kA)': ThreeWtransformer_negative_secondary_mag_ka,
                    'Negative Phase Secondary Angle (deg)': ThreeWtransformer_negative_secondary_angle_degree,
                    'Zero Phase Secondary Mag. (kA)': ThreeWtransformer_zero_secondary_mag_ka,
                    'Zero Phase Secondary Angle (deg)': ThreeWtransformer_zero_secondary_angle_degree,
                    'Positive Phase Tertiary Mag. (kA)': ThreeWtransformer_positive_tertiary_mag_ka,
                    'Positive Phase Tertiary Angle (deg)': ThreeWtransformer_positive_tertiary_angle_degree,
                    'Negative Phase Tertiary Mag. (kA)': ThreeWtransformer_negative_tertiary_mag_ka,
                    'Negative Phase Tertiary Angle (deg)': ThreeWtransformer_negative_tertiary_angle_degree,
                    'Zero Phase Tertiary Mag. (kA)': ThreeWtransformer_zero_tertiary_mag_ka,
                    'Zero Phase Tertiary Angle (deg)': ThreeWtransformer_zero_tertiary_angle_degree
                }

            ThreeWtransformers_data_list.append(dict_ThreeWtransformer_data)
        return ThreeWtransformers_data_list
    # print("fault study type:", fault_study_type)

    if fault_study_type in ['Fault levels on all busbars', 'Fault levels on selected busbars']:
        fault_level_results_data = []
        fault_types = ['LLL', 'LG', 'LL', 'LLG']
        fault_values = ['SymRMS', 'Peak', 'AsymRMS']
        for fault_type in fault_types:
            for fault_value in fault_values:
                FL = net.GetAnalysisFL()

                FL.SetIValue(FL.FaultEngine, 0)
                FL.SetBValue(FL.FaultFlatStart, True)
                FL.SetIValue(FL.MaxFaultIterations, 5)
                FL.SetBValue(FL.FaultUse2ndHarmonic, True)
                # if fault_study_type == 'Fault levels on selected busbars':
                #     busbars = net.GetBusbarUIDs()
                #     k = min(6, len(busbars))
                #     random_ids = random.sample(list(busbars.keys()), k)
                #     FL.SetBusesToFault(random_ids)
                # FL.SetBValue(FL.FaultFlatStart, True)
                cdp = FL.GetBValue(FL.FaultUseCDPs)

                if find_fault_study_type_index(fault_study_type) != -1:
                    FL.SetIValue(FL.FaultStudyType, find_fault_study_type_index(fault_study_type))
                else:
                    error("Invalid Fault Level Study Input")

                if fault_value == 'SymRMS':
                    fault_time = 0.1
                    FL.SetDValue(FL.FaultTime, fault_time)
                else:
                    fault_time = 0.01
                    FL.SetDValue(FL.FaultTime, fault_time)

                if find_fault_type_index(fault_type) != -1:
                    FL.SetIValue(FL.FaultEngineType, find_fault_type_index(fault_type))
                else:
                    error("Invalid Fault Type Input")

                if find_fault_value_index(fault_value) != -1:
                    FL.SetIValue(FL.FaultEngineResultType, find_fault_value_index(fault_value))
                else:
                    error("Invalid Fault Engine Type Input")

                fault_level = net.DoFaultLevel()

                busbars_data = fetch_busbars_fault_data(net, fault_value, cdp)
                dict_fault = {
                    'fault_study_type': fault_study_type,
                    'fault type': fault_type,
                    'fault value': fault_value,
                    'fault time': fault_time,
                    'fault_success': fault_level,
                    'busbars_data': busbars_data
                }
                filtered_dict_fault = {k: v for k, v in dict_fault.items() if v is not False}
                fault_level_results_data.append(filtered_dict_fault)

        try:
            folder = os.path.dirname(cwd)
            folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
            folder_path.mkdir(parents=True, exist_ok=True)
            sub_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'Fault Analysis' / f'{fault_study_type}'
            sub_folder_path.mkdir(parents=True, exist_ok=True)
            file_path = sub_folder_path / f"{IPSA_file_name[:-4]}_{fault_study_type}_{ipsa_version}.xlsx"
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for fault in fault_level_results_data:
                    fault_type = fault['fault type']
                    fault_value = fault['fault value']
                    sheet_name = f"{fault_type}_{fault_value}"
                    
                    if fault_study_type == "Fault levels on all busbars" or fault_study_type == "Fault levels on selected busbars":
                        df = pd.DataFrame(fault['busbars_data'])
                        
                        if fault_study_type == "Fault levels on selected busbars":
                            columns_to_check = ['AC Mag. (kA)', 'DC Mag. (kA)']
                            df = df[~(df[columns_to_check] == 0).all(axis=1)]
                        
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            return file_path
                    # elif fault_study_type == 'Fault along a line':
                    #     df = pd.DataFrame(fault['busbars_data'])
                    #     df.to_excel(writer, sheet_name=sheet_name, index=False)

        except Exception as e:
            error(e)
            error("Close the excel file before running script")

    elif fault_study_type in ['Fault on single busbar', 'Fault along a line']:
        # folder_path = Path(cwd) / f"{IPSA_file_name[:-4]}_{fault_study_type}"
        # folder_path.mkdir(parents=True, exist_ok=True)
        folder = os.path.dirname(cwd)
        folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
        folder_path.mkdir(parents=True, exist_ok=True)
        sub_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'Fault Analysis' / f'{fault_study_type}'
        sub_folder_path.mkdir(parents=True, exist_ok=True)
        
        fault_level_results_data = []
        fault_types = ['LLL', 'LG', 'LL', 'LLG']
        fault_values = ['SymRMS', 'Peak', 'AsymRMS']
        # fault_time = 0.01
        for fault_type in fault_types:
            for fault_value in fault_values:
                FL = net.GetAnalysisFL()
                FL.SetIValue(FL.FaultEngine, 0)
                FL.SetBValue(FL.FaultFlatStart, True)
                FL.SetIValue(FL.MaxFaultIterations, 5)
                FL.SetBValue(FL.FaultUse2ndHarmonic, True)
                cdp = FL.GetBValue(FL.FaultUseCDPs)
                if find_fault_study_type_index(fault_study_type) != -1:
                    FL.SetIValue(FL.FaultStudyType, find_fault_study_type_index(fault_study_type))
                else:
                    error("Invalid Fault Level Study Input")

                if fault_value == 'SymRMS':
                    fault_time = 0.1
                    FL.SetDValue(FL.FaultTime, fault_time)
                else:
                    fault_time = 0.01
                    FL.SetDValue(FL.FaultTime, fault_time)

                if find_fault_type_index(fault_type) != -1:
                    FL.SetIValue(FL.FaultEngineType, find_fault_type_index(fault_type))
                else:
                    error("Invalid Fault Type Input")

                if find_fault_value_index(fault_value) != -1:
                    FL.SetIValue(FL.FaultEngineResultType, find_fault_value_index(fault_value))
                else:
                    error("Invalid Fault Engine Type Input")

                if fault_study_type == 'Fault along a line':
                    FL.SetDValue(FL.DistanceAlongBranch, 0.5)

                fault_level = net.DoFaultLevel()
                if fault_study_type == 'Fault along a line':
                    busbars_data=fetch_busbars_fault_data(net, fault_value, cdp)
                if fault_study_type == 'Fault on single busbar':
                    busbars_data = fault_on_single_busbar_data(net, fault_value, cdp)
                generators_data = fault_on_single_generator_data(net, fault_value)
                grid_infeeds_data = fault_on_single_grid_infeed_data(net, fault_value)
                induction_machine_data=fault_on_single_induction_machine_data(net, fault_value)
                lines_data=fault_on_single_line_data(net, fault_value)
                transformers_data=fault_on_single_transformer_data(net, fault_value)
                ThreeWtransformers_data=fault_on_single_3Wtransformer_data(net, fault_value)

                dict_fault = {
                    'fault_study_type': fault_study_type,
                    'fault type': fault_type,
                    'fault value': fault_value,
                    'fault time': fault_time,
                    'fault_success': fault_level,
                    'Busbars': busbars_data,
                    'Generators': generators_data,
                    'Grid infeed':grid_infeeds_data,
                    'Induction machine':induction_machine_data,
                    'Lines and cables':lines_data,
                    'Transformers':transformers_data,
                    'Three Winding Transformers':ThreeWtransformers_data
                }

                filtered_dict_fault = {k: v for k, v in dict_fault.items() if v is not False}
                fault_level_results_data.append(filtered_dict_fault)

        try:
            file_paths = []
            data = ['fault_study_type', 'fault type', 'fault value', 'fault time', 'fault_success']
            excel = {}
            for fault in fault_level_results_data:
                fault_type = fault['fault type']
                fault_value = fault['fault value']
                sheet_name = f"{fault_type}_{fault_value}"
                for key, value in fault.items():
                    if key in data:
                        continue
                    file_name = (f"{IPSA_file_name[:-4]}_{fault_study_type}_{key}_{ipsa_version}.xlsx")
                    file_path = sub_folder_path / file_name
                    if key not in excel:
                        excel[key] = pd.ExcelWriter(file_path, engine='openpyxl')
                        file_paths.append(file_path)
                    df = pd.DataFrame(value)
                    df.to_excel(excel[key], sheet_name=sheet_name, index=False)
            
            for w in excel.values():
                w.close()
            return file_paths
        except Exception as e:
            error(e)
            error("Close the excel file before running script")
