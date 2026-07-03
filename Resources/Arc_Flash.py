def find_arc_flash_type_index(arc_flash_type):
    match arc_flash_type:
        case 'arc_flash levels on all busbars':
            arc_flash_type = 1
        case 'arc_flash levels on selected busbars':
            arc_flash_type = 2
        case 'arc_flash on single busbar':
            arc_flash_type = 3
        case 'arc_flash along a line':
            arc_flash_type = 4
        case _:
            arc_flash_type = -1
    return arc_flash_type

def find_arc_flash_type_index(arc_flash_type):
    match arc_flash_type:
        case 'LG':
            arc_flash_type_index = 1
        case 'LL':
            arc_flash_type_index = 2
        case 'LLG':
            arc_flash_type_index = 3
        case 'LLL':
            arc_flash_type_index = 4
        case _:
            arc_flash_type_index = -1
    return arc_flash_type_index

def find_arc_flash_value_index(arc_flash_value):
    match arc_flash_value:
        case 'SymRMS':
            arc_flash_type_index = 1
        case 'Peak':
            arc_flash_type_index = 2
        case 'AsymRMS':
            arc_flash_type_index = 3
        case 'BusWave':
            arc_flash_type_index = 4
        case 'BranchWave':
            arc_flash_type_index = 5
        case _:
            arc_flash_type_index = -1
    return arc_flash_type_index

def fetch_busbars_arc_flash_data(net, arc_flash_value, cdp):
    dict_busbars = net.GetBusbars()
    if dict_busbars =={}:
        return False
    busbars_data_list = []

    for bus in dict_busbars.values():
        bus_name = bus.GetSValue(ipsa.IscBusbar.Name)
        ac_mag_ka = bus.Getarc_flashACComponentkA()
        dc_mag_ka = bus.Getarc_flashDCComponentkA()
        dc_percentage=bus.Getarc_flashDCPercentage()
        #dc_percentage=0
        second_harmonic_mag_ka = bus.Getarc_flash2HComponentkA()
        dc_x = bus.Getarc_flashDCTheveninX()
        dc_r = bus.Getarc_flashDCTheveninR()
        dc_xr = dc_x / dc_r if dc_r != 0 else 0
        red_mag_ka = bus.Getarc_flashRedComponentkA()
        red_angle_degree = bus.Getarc_flashRedComponentAngleDeg()
        yellow_mag_ka = bus.Getarc_flashYellowComponentkA()
        yellow_angle_degree = bus.Getarc_flashYellowComponentAngleDeg()
        blue_mag_ka = bus.Getarc_flashBlueComponentkA()
        blue_angle_degree = bus.Getarc_flashBlueComponentAngleDeg()
        positive_mag_ka = bus.Getarc_flashPositiveComponentkA()
        positive_angle_degree = bus.Getarc_flashPositiveComponentAngleDeg()
        negative_mag_ka = bus.Getarc_flashNegativeComponentkA()
        negative_angle_degree = bus.Getarc_flashNegativeComponentAngleDeg()
        zero_mag_ka = bus.Getarc_flashZeroComponentkA()
        zero_angle_degree = bus.Getarc_flashZeroComponentAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_busbar_data(net, arc_flash_value, cdp):
    dict_busbars = net.GetBusbars()
    if dict_busbars =={}:
        return False
    busbars_data_list = []

    for bus in dict_busbars.values():
        bus_name = bus.GetSValue(ipsa.IscBusbar.Name)
        red_phase_voltage = bus.Getarc_flashRedVoltagePU()
        red_phase_angle = bus.Getarc_flashRedVoltageAngleDeg()
        yellow_phase_voltage = bus.Getarc_flashYellowVoltagePU()
        yellow_phase_angle = bus.Getarc_flashYellowVoltageAngleDeg()
        blue_phase_voltage = bus.Getarc_flashBlueVoltagePU()
        blue_phase_angle = bus.Getarc_flashBlueVoltageAngleDeg()
        positive_seq_voltage = bus.Getarc_flashPositiveVoltagePU()
        positive_seq_angle = bus.Getarc_flashPositiveVoltageAngleDeg()
        negative_seq_voltage = bus.Getarc_flashNegativeVoltagePU()
        negative_seq_angle = bus.Getarc_flashNegativeVoltageAngleDeg()  
        zero_seq_voltage = bus.Getarc_flashZeroVoltagePU()
        zero_seq_angle = bus.Getarc_flashZeroVoltageAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_generator_data(net, arc_flash_value):
    dict_syn_machines = net.GetSynMachines()
    if dict_syn_machines =={}:
        return False
    generators_data_list = []

    for syn_machine in dict_syn_machines.values():
        generator_name = syn_machine.GetSValue(ipsa.IscSynMachine.Name)
        gen_ac_mag_ka = syn_machine.Getarc_flashACMagnitudekA()
        gen_dc_mag_ka = syn_machine.Getarc_flashDCMagnitudekA()
        gen_dc_percentage = syn_machine.Getarc_flashDCPC() 
        gen_second_harmonic_mag_ka = syn_machine.Getarc_flashSecondHarmonickA()
        gen_red_mag_ka = syn_machine.Getarc_flashRedMagnitudekA()
        gen_red_angle_degree = syn_machine.Getarc_flashRedAngleDeg()
        gen_yellow_mag_ka = syn_machine.Getarc_flashYellowMagnitudekA()
        gen_yellow_angle_degree = syn_machine.Getarc_flashYellowAngleDeg()
        gen_blue_mag_ka = syn_machine.Getarc_flashBlueMagnitudekA()
        gen_blue_angle_degree = syn_machine.Getarc_flashBlueAngleDeg()
        gen_pos_mag_ka = syn_machine.Getarc_flashPositiveMagnitudekA()
        gen_pos_angle_degree = syn_machine.Getarc_flashPositiveAngleDeg()
        gen_neg_mag_ka = syn_machine.Getarc_flashNegativeMagnitudekA()
        gen_neg_angle_degree = syn_machine.Getarc_flashNegativeAngleDeg()
        gen_zero_mag_ka = syn_machine.Getarc_flashZeroMagnitudekA()
        gen_zero_angle_degree = syn_machine.Getarc_flashZeroAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_grid_infeed_data(net, arc_flash_value):
    dict_grid_infeeds = net.GetGridInfeeds()
    if dict_grid_infeeds =={}:
        return False
    grid_infeeds_data_list = []

    for grid_infeed in dict_grid_infeeds.values():
        grid_name = grid_infeed.GetSValue(ipsa.IscGridInfeed.Name)
        grid_ac_mag_ka = grid_infeed.Getarc_flashACMagnitudekA()
        grid_dc_mag_ka = grid_infeed.Getarc_flashDCMagnitudekA()
        grid_dc_percentage = grid_infeed.Getarc_flashDCPC() 
        grid_second_harmonic_mag_ka = grid_infeed.Getarc_flashSecondHarmonickA()
        grid_red_mag_ka = grid_infeed.Getarc_flashRedMagnitudekA()
        grid_red_angle_degree = grid_infeed.Getarc_flashRedAngleDeg()
        grid_yellow_mag_ka = grid_infeed.Getarc_flashYellowMagnitudekA()
        grid_yellow_angle_degree = grid_infeed.Getarc_flashYellowAngleDeg()
        grid_blue_mag_ka = grid_infeed.Getarc_flashBlueMagnitudekA()
        grid_blue_angle_degree = grid_infeed.Getarc_flashBlueAngleDeg()
        grid_pos_mag_ka = grid_infeed.Getarc_flashPositiveMagnitudekA()
        grid_pos_angle_degree = grid_infeed.Getarc_flashPositiveAngleDeg()
        grid_neg_mag_ka = grid_infeed.Getarc_flashNegativeMagnitudekA()
        grid_neg_angle_degree = grid_infeed.Getarc_flashNegativeAngleDeg()
        grid_zero_mag_ka = grid_infeed.Getarc_flashZeroMagnitudekA()
        grid_zero_angle_degree = grid_infeed.Getarc_flashZeroAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_induction_machine_data(net, arc_flash_value):
    dict_induction_machines = net.GetIndMachines()
    if dict_induction_machines =={}:
        return False
    induction_machines_data_list = []

    for induction_machine in dict_induction_machines.values():
        ind_machine_name = induction_machine.GetSValue(ipsa.IscIndMachine.Name)
        ind_machine_ac_mag_ka = induction_machine.Getarc_flashACMagnitudekA()
        ind_machine_dc_mag_ka = induction_machine.Getarc_flashDCMagnitudekA()
        ind_machine_dc_percentage = induction_machine.Getarc_flashDCPC() 
        # ind_machine_second_harmonic_mag_ka = induction_machine.Getarc_flashSecondHarmonickA()
        ind_machine_red_mag_ka = induction_machine.Getarc_flashRedMagnitudekA()
        ind_machine_red_angle_degree = induction_machine.Getarc_flashRedAngleDeg()
        ind_machine_yellow_mag_ka = induction_machine.Getarc_flashYellowMagnitudekA()
        ind_machine_yellow_angle_degree = induction_machine.Getarc_flashYellowAngleDeg()
        ind_machine_blue_mag_ka = induction_machine.Getarc_flashBlueMagnitudekA()
        ind_machine_blue_angle_degree = induction_machine.Getarc_flashBlueAngleDeg()
        ind_machine_pos_mag_ka = induction_machine.Getarc_flashPositiveMagnitudekA()
        ind_machine_pos_angle_degree = induction_machine.Getarc_flashPositiveAngleDeg()
        ind_machine_neg_mag_ka = induction_machine.Getarc_flashNegativeMagnitudekA()
        ind_machine_neg_angle_degree = induction_machine.Getarc_flashNegativeAngleDeg()
        ind_machine_zero_mag_ka = induction_machine.Getarc_flashZeroMagnitudekA()
        ind_machine_zero_angle_degree = induction_machine.Getarc_flashZeroAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_line_data(net, arc_flash_value):
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
        branch_red_mag_ka = branch.Getarc_flashRedComponentkA()
        branch_red_angle_degree = branch.Getarc_flashRedComponentAngleDeg()
        branch_yellow_mag_ka = branch.Getarc_flashYellowComponentkA()
        branch_yellow_angle_degree = branch.Getarc_flashYellowComponentAngleDeg()
        branch_blue_mag_ka = branch.Getarc_flashBlueComponentkA()
        branch_blue_angle_degree = branch.Getarc_flashBlueComponentAngleDeg()
        branch_pos_mag_ka = branch.Getarc_flashPositiveComponentkA()
        branch_pos_angle_degree = branch.Getarc_flashPositiveComponentAngleDeg()
        branch_neg_mag_ka = branch.Getarc_flashNegativeComponentkA()
        branch_neg_angle_degree = branch.Getarc_flashNegativeComponentAngleDeg()
        branch_zero_mag_ka = branch.Getarc_flashZeroComponentkA()
        branch_zero_angle_degree = branch.Getarc_flashZeroComponentAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_transformer_data(net, arc_flash_value):
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
        transformer_red_from_mag_ka = transformer.Getarc_flashRedComponentFromkA()
        transformer_red_from_angle_degree = transformer.Getarc_flashRedComponentFromAngleDeg()
        transformer_yellow_from_mag_ka = transformer.Getarc_flashYellowComponentFromkA()
        transformer_yellow_from_angle_degree = transformer.Getarc_flashYellowComponentFromAngleDeg()
        transformer_blue_from_mag_ka = transformer.Getarc_flashBlueComponentFromkA()
        transformer_blue_from_angle_degree = transformer.Getarc_flashBlueComponentFromAngleDeg()
        transformer_red_to_mag_ka = transformer.Getarc_flashRedComponentTokA()
        transformer_red_to_angle_degree = transformer.Getarc_flashRedComponentToAngleDeg()
        transformer_yellow_to_mag_ka = transformer.Getarc_flashYellowComponentTokA()
        transformer_yellow_to_angle_degree = transformer.Getarc_flashYellowComponentToAngleDeg()
        transformer_blue_to_mag_ka = transformer.Getarc_flashBlueComponentTokA()
        transformer_blue_to_angle_degree = transformer.Getarc_flashBlueComponentToAngleDeg()
        transformer_pos_from_mag_ka = transformer.Getarc_flashPositiveComponentFromkA()
        transformer_pos_from_angle_degree = transformer.Getarc_flashPositiveComponentFromAngleDeg()
        transformer_neg_from_mag_ka = transformer.Getarc_flashNegativeComponentFromkA()
        transformer_neg_from_angle_degree = transformer.Getarc_flashNegativeComponentFromAngleDeg()
        transformer_zero_from_mag_ka = transformer.Getarc_flashZeroComponentFromkA()
        transformer_zero_from_angle_degree = transformer.Getarc_flashZeroComponentFromAngleDeg()
        transformer_pos_to_mag_ka = transformer.Getarc_flashPositiveComponentTokA()
        transformer_pos_to_angle_degree = transformer.Getarc_flashPositiveComponentToAngleDeg()
        transformer_neg_to_mag_ka = transformer.Getarc_flashNegativeComponentTokA()
        transformer_neg_to_angle_degree = transformer.Getarc_flashNegativeComponentToAngleDeg()
        transformer_zero_to_mag_ka = transformer.Getarc_flashZeroComponentTokA()
        transformer_zero_to_angle_degree = transformer.Getarc_flashZeroComponentToAngleDeg()
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        elif arc_flash_value in ['SymRMS']:
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
def arc_flash_on_single_3Wtransformer_data(net, arc_flash_value):
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
        ThreeWtransformer_red_primary_mag_ka = ThreeWtransformer.Getarc_flashRedMagnitudekA(1)
        ThreeWtransformer_red_primary_angle_degree = ThreeWtransformer.Getarc_flashRedAngleDeg(1)
        ThreeWtransformer_yellow_primary_mag_ka = ThreeWtransformer.Getarc_flashYellowMagnitudekA(1)
        ThreeWtransformer_yellow_primary_angle_degree = ThreeWtransformer.Getarc_flashYellowAngleDeg(1)
        ThreeWtransformer_blue_primary_mag_ka = ThreeWtransformer.Getarc_flashBlueMagnitudekA(1)
        ThreeWtransformer_blue_primary_angle_degree = ThreeWtransformer.Getarc_flashBlueAngleDeg(1)
        ThreeWtransformer_red_secondary_mag_ka = ThreeWtransformer.Getarc_flashRedMagnitudekA(2)
        ThreeWtransformer_red_secondary_angle_degree = ThreeWtransformer.Getarc_flashRedAngleDeg(2)
        ThreeWtransformer_yellow_secondary_mag_ka = ThreeWtransformer.Getarc_flashYellowMagnitudekA(2)
        ThreeWtransformer_yellow_secondary_angle_degree = ThreeWtransformer.Getarc_flashYellowAngleDeg(2)
        ThreeWtransformer_blue_secondary_mag_ka = ThreeWtransformer.Getarc_flashBlueMagnitudekA(2)
        ThreeWtransformer_blue_secondary_angle_degree = ThreeWtransformer.Getarc_flashBlueAngleDeg(2)
        ThreeWtransformer_red_tertiary_mag_ka = ThreeWtransformer.Getarc_flashRedMagnitudekA(3)
        ThreeWtransformer_red_tertiary_angle_degree = ThreeWtransformer.Getarc_flashRedAngleDeg(3)
        ThreeWtransformer_yellow_tertiary_mag_ka = ThreeWtransformer.Getarc_flashYellowMagnitudekA(3)
        ThreeWtransformer_yellow_tertiary_angle_degree = ThreeWtransformer.Getarc_flashYellowAngleDeg(3)
        ThreeWtransformer_blue_tertiary_mag_ka = ThreeWtransformer.Getarc_flashBlueMagnitudekA(3)
        ThreeWtransformer_blue_tertiary_angle_degree = ThreeWtransformer.Getarc_flashBlueAngleDeg(3)
        ThreeWtransformer_positive_primary_mag_ka = ThreeWtransformer.Getarc_flashPositiveMagnitudekA(1)
        ThreeWtransformer_positive_primary_angle_degree = ThreeWtransformer.Getarc_flashPositiveAngleDeg(1)
        ThreeWtransformer_negative_primary_mag_ka = ThreeWtransformer.Getarc_flashNegativeMagnitudekA(1)
        ThreeWtransformer_negative_primary_angle_degree = ThreeWtransformer.Getarc_flashNegativeAngleDeg(1)
        ThreeWtransformer_zero_primary_mag_ka = ThreeWtransformer.Getarc_flashZeroMagnitudekA(1)
        ThreeWtransformer_zero_primary_angle_degree = ThreeWtransformer.Getarc_flashZeroAngleDeg(1)
        ThreeWtransformer_positive_secondary_mag_ka = ThreeWtransformer.Getarc_flashPositiveMagnitudekA(2)
        ThreeWtransformer_positive_secondary_angle_degree = ThreeWtransformer.Getarc_flashPositiveAngleDeg(2)
        ThreeWtransformer_negative_secondary_mag_ka = ThreeWtransformer.Getarc_flashNegativeMagnitudekA(2)
        ThreeWtransformer_negative_secondary_angle_degree = ThreeWtransformer.Getarc_flashNegativeAngleDeg(2)
        ThreeWtransformer_zero_secondary_mag_ka = ThreeWtransformer.Getarc_flashZeroMagnitudekA(2)
        ThreeWtransformer_zero_secondary_angle_degree = ThreeWtransformer.Getarc_flashZeroAngleDeg(2)
        ThreeWtransformer_positive_tertiary_mag_ka = ThreeWtransformer.Getarc_flashPositiveMagnitudekA(3)
        ThreeWtransformer_positive_tertiary_angle_degree = ThreeWtransformer.Getarc_flashPositiveAngleDeg(3)
        ThreeWtransformer_negative_tertiary_mag_ka = ThreeWtransformer.Getarc_flashNegativeMagnitudekA(3)
        ThreeWtransformer_negative_tertiary_angle_degree = ThreeWtransformer.Getarc_flashNegativeAngleDeg(3)
        ThreeWtransformer_zero_tertiary_mag_ka = ThreeWtransformer.Getarc_flashZeroMagnitudekA(3)
        ThreeWtransformer_zero_tertiary_angle_degree = ThreeWtransformer.Getarc_flashZeroAngleDeg(3)
        if arc_flash_value in ['Peak', 'AsymRMS']:
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
        elif arc_flash_value in ['SymRMS']:
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

def run_arc_flash_level(net, cwd, ipsa_version, IPSA_file_name, arc_flash_study_type):
    # print("arc_flash study type:", arc_flash_study_type)
    if arc_flash_study_type in ['arc_flash levels on all busbars', 'arc_flash levels on selected busbars']:
        arc_flash_level_results_data = []
        arc_flash_types = ['LLL', 'LG', 'LL', 'LLG']
        arc_flash_values = ['SymRMS', 'Peak', 'AsymRMS']
        for arc_flash_type in arc_flash_types:
            for arc_flash_value in arc_flash_values:
                FL = net.GetAnalysisFL()

                FL.SetIValue(FL.arc_flashEngine, 0)
                FL.SetBValue(FL.arc_flashFlatStart, True)
                FL.SetIValue(FL.Maxarc_flashIterations, 5)
                FL.SetBValue(FL.arc_flashUse2ndHarmonic, True)
                # if arc_flash_study_type == 'arc_flash levels on selected busbars':
                #     busbars = net.GetBusbarUIDs()
                #     k = min(6, len(busbars))
                #     random_ids = random.sample(list(busbars.keys()), k)
                #     FL.SetBusesToarc_flash(random_ids)
                # FL.SetBValue(FL.arc_flashFlatStart, True)
                cdp = FL.GetBValue(FL.arc_flashUseCDPs)

                if find_arc_flash_study_type_index(arc_flash_study_type) != -1:
                    FL.SetIValue(FL.arc_flashStudyType, find_arc_flash_study_type_index(arc_flash_study_type))
                else:
                    print("Invalid arc_flash Level Study Input")

                if arc_flash_value == 'SymRMS':
                    arc_flash_time = 0.1
                    FL.SetDValue(FL.arc_flashTime, arc_flash_time)
                else:
                    arc_flash_time = 0.01
                    FL.SetDValue(FL.arc_flashTime, arc_flash_time)

                if find_arc_flash_type_index(arc_flash_type) != -1:
                    FL.SetIValue(FL.arc_flashEngineType, find_arc_flash_type_index(arc_flash_type))
                else:
                    print("Invalid arc_flash Type Input")

                if find_arc_flash_value_index(arc_flash_value) != -1:
                    FL.SetIValue(FL.arc_flashEngineResultType, find_arc_flash_value_index(arc_flash_value))
                else:
                    print("Invalid arc_flash Engine Type Input")

                arc_flash_level = net.Doarc_flashLevel()

                busbars_data = fetch_busbars_arc_flash_data(net, arc_flash_value, cdp)
                dict_arc_flash = {
                    'arc_flash_study_type': arc_flash_study_type,
                    'arc_flash type': arc_flash_type,
                    'arc_flash value': arc_flash_value,
                    'arc_flash time': arc_flash_time,
                    'arc_flash_success': arc_flash_level,
                    'busbars_data': busbars_data
                }
                filtered_dict_arc_flash = {k: v for k, v in dict_arc_flash.items() if v is not False}
                arc_flash_level_results_data.append(filtered_dict_arc_flash)

        try:
            folder = os.path.dirname(cwd)
            folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
            folder_path.mkdir(parents=True, exist_ok=True)
            sub_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'arc_flash Analysis' /f'{arc_flash_study_type}'
            sub_folder_path.mkdir(parents=True, exist_ok=True)
            file_path = sub_folder_path / f"{IPSA_file_name[:-4]}_{arc_flash_study_type}_{ipsa_version}.xlsx"
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for arc_flash in arc_flash_level_results_data:
                    arc_flash_type = arc_flash['arc_flash type']
                    arc_flash_value = arc_flash['arc_flash value']
                    sheet_name = f"{arc_flash_type}_{arc_flash_value}"
                    
                    if arc_flash_study_type == "arc_flash levels on all busbars" or arc_flash_study_type == "arc_flash levels on selected busbars":
                        df = pd.DataFrame(arc_flash['busbars_data'])
                        
                        if arc_flash_study_type == "arc_flash levels on selected busbars":
                            columns_to_check = ['AC Mag. (kA)', 'DC Mag. (kA)']
                            df = df[~(df[columns_to_check] == 0).all(axis=1)]
                        
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            return file_path
                    # elif arc_flash_study_type == 'arc_flash along a line':
                    #     df = pd.DataFrame(arc_flash['busbars_data'])
                    #     df.to_excel(writer, sheet_name=sheet_name, index=False)

        except Exception:
            print("Close the excel file before running script")

    elif arc_flash_study_type in ['arc_flash on single busbar', 'arc_flash along a line']:
        # folder_path = Path(cwd) / f"{IPSA_file_name[:-4]}_{arc_flash_study_type}"
        # folder_path.mkdir(parents=True, exist_ok=True)
        folder = os.path.dirname(cwd)
        folder_path = Path(folder) / 'Test Results' / f"{ipsa_version}"
        folder_path.mkdir(parents=True, exist_ok=True)
        sub_folder_path = folder_path / f"{IPSA_file_name[:-4]}" / 'arc_flash Analysis' / f'{arc_flash_study_type}'
        sub_folder_path.mkdir(parents=True, exist_ok=True)
        
        arc_flash_level_results_data = []
        arc_flash_types = ['LLL', 'LG', 'LL', 'LLG']
        arc_flash_values = ['SymRMS', 'Peak', 'AsymRMS']
        # arc_flash_time = 0.01
        for arc_flash_type in arc_flash_types:
            for arc_flash_value in arc_flash_values:
                FL = net.GetAnalysisFL()
                FL.SetIValue(FL.arc_flashEngine, 0)
                FL.SetBValue(FL.arc_flashFlatStart, True)
                FL.SetIValue(FL.Maxarc_flashIterations, 5)
                FL.SetBValue(FL.arc_flashUse2ndHarmonic, True)
                cdp = FL.GetBValue(FL.arc_flashUseCDPs)
                if find_arc_flash_study_type_index(arc_flash_study_type) != -1:
                    FL.SetIValue(FL.arc_flashStudyType, find_arc_flash_study_type_index(arc_flash_study_type))
                else:
                    print("Invalid arc_flash Level Study Input")

                if arc_flash_value == 'SymRMS':
                    arc_flash_time = 0.1
                    FL.SetDValue(FL.arc_flashTime, arc_flash_time)
                else:
                    arc_flash_time = 0.01
                    FL.SetDValue(FL.arc_flashTime, arc_flash_time)

                if find_arc_flash_type_index(arc_flash_type) != -1:
                    FL.SetIValue(FL.arc_flashEngineType, find_arc_flash_type_index(arc_flash_type))
                else:
                    print("Invalid arc_flash Type Input")

                if find_arc_flash_value_index(arc_flash_value) != -1:
                    FL.SetIValue(FL.arc_flashEngineResultType, find_arc_flash_value_index(arc_flash_value))
                else:
                    print("Invalid arc_flash Engine Type Input")

                if arc_flash_study_type == 'arc_flash along a line':
                    FL.SetDValue(FL.DistanceAlongBranch, 0.5)

                arc_flash_level = net.Doarc_flashLevel()
                if arc_flash_study_type == 'arc_flash along a line':
                    busbars_data=fetch_busbars_arc_flash_data(net, arc_flash_value, cdp)
                if arc_flash_study_type == 'arc_flash on single busbar':
                    busbars_data = arc_flash_on_single_busbar_data(net, arc_flash_value, cdp)
                generators_data = arc_flash_on_single_generator_data(net, arc_flash_value)
                grid_infeeds_data = arc_flash_on_single_grid_infeed_data(net, arc_flash_value)
                induction_machine_data=arc_flash_on_single_induction_machine_data(net, arc_flash_value)
                lines_data=arc_flash_on_single_line_data(net, arc_flash_value)
                transformers_data=arc_flash_on_single_transformer_data(net, arc_flash_value)
                ThreeWtransformers_data=arc_flash_on_single_3Wtransformer_data(net, arc_flash_value)

                dict_arc_flash = {
                    'arc_flash_study_type': arc_flash_study_type,
                    'arc_flash type': arc_flash_type,
                    'arc_flash value': arc_flash_value,
                    'arc_flash time': arc_flash_time,
                    'arc_flash_success': arc_flash_level,
                    'Busbars': busbars_data,
                    'Generators': generators_data,
                    'Grid infeed':grid_infeeds_data,
                    'Induction machine':induction_machine_data,
                    'Lines and cables':lines_data,
                    'Transformers':transformers_data,
                    'Three Winding Transformers':ThreeWtransformers_data
                }

                filtered_dict_arc_flash = {k: v for k, v in dict_arc_flash.items() if v is not False}
                arc_flash_level_results_data.append(filtered_dict_arc_flash)

        try:
            file_paths = []
            data = ['arc_flash_study_type', 'arc_flash type', 'arc_flash value', 'arc_flash time', 'arc_flash_success']
            excel = {}
            for arc_flash in arc_flash_level_results_data:
                arc_flash_type = arc_flash['arc_flash type']
                arc_flash_value = arc_flash['arc_flash value']
                sheet_name = f"{arc_flash_type}_{arc_flash_value}"
                for key, value in arc_flash.items():
                    if key in data:
                        continue
                    file_name = (f"{IPSA_file_name[:-4]}_{arc_flash_study_type}_{key}_{ipsa_version}.xlsx")
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
            print(e)
            print("Close the excel file before running script")