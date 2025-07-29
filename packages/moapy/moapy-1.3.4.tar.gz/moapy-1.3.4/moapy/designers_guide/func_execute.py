from moapy.designers_guide.core_engine.execute_calc_general import execute_calc_content, DG_Result_Reports

def calc_content_1(G4_COMP_1: str) -> DG_Result_Reports:
    target_components = ['G4_COMP_4', 'G4_COMP_5', 'G4_COMP_6', 'G4_COMP_7', 'G4_COMP_8', 'G4_COMP_9']
    inputs = {"G4_COMP_1": G4_COMP_1}
    return execute_calc_content(target_components, inputs)

def calc_content_10(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str, G10_COMP_3: float, G10_COMP_4: float, G10_COMP_5: float, G10_COMP_6: float) -> DG_Result_Reports:
    target_components = ['G10_COMP_1']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15, "G10_COMP_3": G10_COMP_3, "G10_COMP_4": G10_COMP_4, "G10_COMP_5": G10_COMP_5, "G10_COMP_6": G10_COMP_6}
    return execute_calc_content(target_components, inputs)

def calc_content_11(G11_COMP_1: str, G11_COMP_4: str, G11_COMP_5: float, G11_COMP_11: str, G11_COMP_14: str, G11_COMP_18: float, G11_COMP_19: float, G11_COMP_25: float, G11_COMP_26: float, G11_COMP_30: str, G11_COMP_33: float, G11_COMP_34: float) -> DG_Result_Reports:
    target_components = ['G11_COMP_2', 'G11_COMP_3']
    inputs = {"G11_COMP_1": G11_COMP_1, "G11_COMP_4": G11_COMP_4, "G11_COMP_5": G11_COMP_5, "G11_COMP_11": G11_COMP_11, "G11_COMP_14": G11_COMP_14, "G11_COMP_18": G11_COMP_18, "G11_COMP_19": G11_COMP_19, "G11_COMP_25": G11_COMP_25, "G11_COMP_26": G11_COMP_26, "G11_COMP_30": G11_COMP_30, "G11_COMP_33": G11_COMP_33, "G11_COMP_34": G11_COMP_34}
    return execute_calc_content(target_components, inputs)

def calc_content_12(G12_COMP_1: str, G12_COMP_2: str, G12_COMP_4: str, G12_COMP_5: float, G12_COMP_6: float) -> DG_Result_Reports:
    target_components = ['G12_COMP_15', 'G12_COMP_16', 'G12_COMP_17']
    inputs = {"G12_COMP_1": G12_COMP_1, "G12_COMP_2": G12_COMP_2, "G12_COMP_4": G12_COMP_4, "G12_COMP_5": G12_COMP_5, "G12_COMP_6": G12_COMP_6}
    return execute_calc_content(target_components, inputs)

def calc_content_13(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str, G13_COMP_2: float, G13_COMP_3: float, G13_COMP_8: str) -> DG_Result_Reports:
    target_components = ['G13_COMP_16']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15, "G13_COMP_2": G13_COMP_2, "G13_COMP_3": G13_COMP_3, "G13_COMP_8": G13_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_14(G14_COMP_1: float, G14_COMP_2: str, G14_COMP_3: str, G14_COMP_4: str) -> DG_Result_Reports:
    target_components = ['G14_COMP_15', 'G14_COMP_16', 'G14_COMP_17', 'G14_COMP_18', 'G14_COMP_19']
    inputs = {"G14_COMP_1": G14_COMP_1, "G14_COMP_2": G14_COMP_2, "G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4}
    return execute_calc_content(target_components, inputs)

def calc_content_15(G14_COMP_4: str, G15_COMP_1: float, G15_COMP_2: str, G15_COMP_7: float) -> DG_Result_Reports:
    target_components = ['G15_COMP_6', 'G15_COMP_8', 'G15_COMP_9']
    inputs = {"G14_COMP_4": G14_COMP_4, "G15_COMP_1": G15_COMP_1, "G15_COMP_2": G15_COMP_2, "G15_COMP_7": G15_COMP_7}
    return execute_calc_content(target_components, inputs)

def calc_content_16(G14_COMP_4: str, G15_COMP_2: str, G16_COMP_5: float, G16_COMP_6: float, G16_COMP_11: float, G16_COMP_12: float, G16_COMP_14: str, G16_COMP_23: float) -> DG_Result_Reports:
    target_components = ['G16_COMP_17', 'G16_COMP_19']
    inputs = {"G14_COMP_4": G14_COMP_4, "G15_COMP_2": G15_COMP_2, "G16_COMP_5": G16_COMP_5, "G16_COMP_6": G16_COMP_6, "G16_COMP_11": G16_COMP_11, "G16_COMP_12": G16_COMP_12, "G16_COMP_14": G16_COMP_14, "G16_COMP_23": G16_COMP_23}
    return execute_calc_content(target_components, inputs)

def calc_content_17(G14_COMP_4: str, G15_COMP_2: str, G16_COMP_11: float, G16_COMP_12: float, G16_COMP_14: str, G16_COMP_23: float, G17_COMP_11: float) -> DG_Result_Reports:
    target_components = ['G17_COMP_10', 'G17_COMP_16']
    inputs = {"G14_COMP_4": G14_COMP_4, "G15_COMP_2": G15_COMP_2, "G16_COMP_11": G16_COMP_11, "G16_COMP_12": G16_COMP_12, "G16_COMP_14": G16_COMP_14, "G16_COMP_23": G16_COMP_23, "G17_COMP_11": G17_COMP_11}
    return execute_calc_content(target_components, inputs)

def calc_content_18(G14_COMP_3: str, G18_COMP_1: float, G18_COMP_7: str) -> DG_Result_Reports:
    target_components = ['G18_COMP_3', 'G18_COMP_6', 'G18_COMP_10']
    inputs = {"G14_COMP_3": G14_COMP_3, "G18_COMP_1": G18_COMP_1, "G18_COMP_7": G18_COMP_7}
    return execute_calc_content(target_components, inputs)

def calc_content_19(G14_COMP_4: str, G19_COMP_1: str, G19_COMP_2: str, G19_COMP_8: str, G19_COMP_10: str, G19_COMP_15: str, G19_COMP_16: str, G19_COMP_17: str, G19_COMP_19: str, G19_COMP_23: str, G19_COMP_26: str, G19_COMP_28: str) -> DG_Result_Reports:
    target_components = ['G19_COMP_3', 'G19_COMP_7']
    inputs = {"G14_COMP_4": G14_COMP_4, "G19_COMP_1": G19_COMP_1, "G19_COMP_2": G19_COMP_2, "G19_COMP_8": G19_COMP_8, "G19_COMP_10": G19_COMP_10, "G19_COMP_15": G19_COMP_15, "G19_COMP_16": G19_COMP_16, "G19_COMP_17": G19_COMP_17, "G19_COMP_19": G19_COMP_19, "G19_COMP_23": G19_COMP_23, "G19_COMP_26": G19_COMP_26, "G19_COMP_28": G19_COMP_28}
    return execute_calc_content(target_components, inputs)

def calc_content_2(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str) -> DG_Result_Reports:
    target_components = ['G3_COMP_24']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15}
    return execute_calc_content(target_components, inputs)

def calc_content_20(G20_COMP_12: str, G20_COMP_14: str) -> DG_Result_Reports:
    target_components = ['G20_COMP_1', 'G20_COMP_8', 'G20_COMP_13', 'G20_COMP_15', 'G20_COMP_18']
    inputs = {"G20_COMP_12": G20_COMP_12, "G20_COMP_14": G20_COMP_14}
    return execute_calc_content(target_components, inputs)

def calc_content_21(G14_COMP_3: str, G14_COMP_4: str, G16_COMP_11: float, G21_COMP_3: float, G21_COMP_5: str, G21_COMP_11: float, G21_COMP_12: float) -> DG_Result_Reports:
    target_components = ['G21_COMP_1']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G16_COMP_11": G16_COMP_11, "G21_COMP_3": G21_COMP_3, "G21_COMP_5": G21_COMP_5, "G21_COMP_11": G21_COMP_11, "G21_COMP_12": G21_COMP_12}
    return execute_calc_content(target_components, inputs)

def calc_content_22(G6_COMP_2: str, G6_COMP_4: float, G6_COMP_9: float, G14_COMP_3: str, G14_COMP_4: str, G21_COMP_3: float, G22_COMP_14: float, G22_COMP_15: float, G22_COMP_16: float) -> DG_Result_Reports:
    target_components = ['G22_COMP_1', 'G22_COMP_2']
    inputs = {"G6_COMP_2": G6_COMP_2, "G6_COMP_4": G6_COMP_4, "G6_COMP_9": G6_COMP_9, "G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G21_COMP_3": G21_COMP_3, "G22_COMP_14": G22_COMP_14, "G22_COMP_15": G22_COMP_15, "G22_COMP_16": G22_COMP_16}
    return execute_calc_content(target_components, inputs)

def calc_content_23(G6_COMP_2: str, G6_COMP_4: float, G6_COMP_9: float, G14_COMP_3: str, G14_COMP_4: str, G18_COMP_1: float, G21_COMP_3: float, G22_COMP_14: float, G22_COMP_15: float, G22_COMP_16: float) -> DG_Result_Reports:
    target_components = ['G23_COMP_1', 'G23_COMP_8']
    inputs = {"G6_COMP_2": G6_COMP_2, "G6_COMP_4": G6_COMP_4, "G6_COMP_9": G6_COMP_9, "G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G18_COMP_1": G18_COMP_1, "G21_COMP_3": G21_COMP_3, "G22_COMP_14": G22_COMP_14, "G22_COMP_15": G22_COMP_15, "G22_COMP_16": G22_COMP_16}
    return execute_calc_content(target_components, inputs)

def calc_content_24(G14_COMP_3: str, G14_COMP_4: str, G18_COMP_1: float, G24_COMP_2: float, G24_COMP_5: str, G24_COMP_8: str, G24_COMP_11: str, G24_COMP_13: float, G24_COMP_16: float, G24_COMP_17: float, G24_COMP_22: str, G24_COMP_25: float, G24_COMP_26: str, G24_COMP_29: str, G24_COMP_33: float) -> DG_Result_Reports:
    target_components = ['G24_COMP_1', 'G24_COMP_9', 'G24_COMP_10']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G18_COMP_1": G18_COMP_1, "G24_COMP_2": G24_COMP_2, "G24_COMP_5": G24_COMP_5, "G24_COMP_8": G24_COMP_8, "G24_COMP_11": G24_COMP_11, "G24_COMP_13": G24_COMP_13, "G24_COMP_16": G24_COMP_16, "G24_COMP_17": G24_COMP_17, "G24_COMP_22": G24_COMP_22, "G24_COMP_25": G24_COMP_25, "G24_COMP_26": G24_COMP_26, "G24_COMP_29": G24_COMP_29, "G24_COMP_33": G24_COMP_33}
    return execute_calc_content(target_components, inputs)

def calc_content_25(G14_COMP_3: str, G14_COMP_4: str, G18_COMP_1: float, G24_COMP_2: float, G24_COMP_5: str, G24_COMP_8: str, G24_COMP_11: str, G24_COMP_13: float, G24_COMP_16: float, G24_COMP_17: float, G24_COMP_25: float, G24_COMP_26: str, G24_COMP_33: float, G25_COMP_5: float) -> DG_Result_Reports:
    target_components = ['G25_COMP_1', 'G25_COMP_2']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G18_COMP_1": G18_COMP_1, "G24_COMP_2": G24_COMP_2, "G24_COMP_5": G24_COMP_5, "G24_COMP_8": G24_COMP_8, "G24_COMP_11": G24_COMP_11, "G24_COMP_13": G24_COMP_13, "G24_COMP_16": G24_COMP_16, "G24_COMP_17": G24_COMP_17, "G24_COMP_25": G24_COMP_25, "G24_COMP_26": G24_COMP_26, "G24_COMP_33": G24_COMP_33, "G25_COMP_5": G25_COMP_5}
    return execute_calc_content(target_components, inputs)

def calc_content_26(G14_COMP_3: str, G14_COMP_4: str, G26_COMP_4: float, G26_COMP_5: float, G26_COMP_6: float, G26_COMP_10: float, G26_COMP_12: float, G26_COMP_13: float, G26_COMP_15: float, G26_COMP_16: float, G26_COMP_17: float, G26_COMP_18: float) -> DG_Result_Reports:
    target_components = ['G26_COMP_1', 'G26_COMP_23', 'G26_COMP_24']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G26_COMP_4": G26_COMP_4, "G26_COMP_5": G26_COMP_5, "G26_COMP_6": G26_COMP_6, "G26_COMP_10": G26_COMP_10, "G26_COMP_12": G26_COMP_12, "G26_COMP_13": G26_COMP_13, "G26_COMP_15": G26_COMP_15, "G26_COMP_16": G26_COMP_16, "G26_COMP_17": G26_COMP_17, "G26_COMP_18": G26_COMP_18}
    return execute_calc_content(target_components, inputs)

def calc_content_27(G14_COMP_3: str, G14_COMP_4: str, G27_COMP_1: str, G27_COMP_2: float, G27_COMP_3: float, G27_COMP_4: float, G27_COMP_5: float, G27_COMP_6: float, G27_COMP_7: float, G27_COMP_8: float, G27_COMP_9: float) -> DG_Result_Reports:
    target_components = ['G27_COMP_10', 'G27_COMP_11', 'G27_COMP_12', 'G27_COMP_24']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G27_COMP_1": G27_COMP_1, "G27_COMP_2": G27_COMP_2, "G27_COMP_3": G27_COMP_3, "G27_COMP_4": G27_COMP_4, "G27_COMP_5": G27_COMP_5, "G27_COMP_6": G27_COMP_6, "G27_COMP_7": G27_COMP_7, "G27_COMP_8": G27_COMP_8, "G27_COMP_9": G27_COMP_9}
    return execute_calc_content(target_components, inputs)

def calc_content_28(G14_COMP_3: str, G14_COMP_4: str, G27_COMP_2: float, G27_COMP_6: float, G27_COMP_7: float, G28_COMP_1: float, G28_COMP_3: float, G28_COMP_8: float, G28_COMP_11: float) -> DG_Result_Reports:
    target_components = ['G28_COMP_6', 'G28_COMP_7', 'G28_COMP_9']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G27_COMP_2": G27_COMP_2, "G27_COMP_6": G27_COMP_6, "G27_COMP_7": G27_COMP_7, "G28_COMP_1": G28_COMP_1, "G28_COMP_3": G28_COMP_3, "G28_COMP_8": G28_COMP_8, "G28_COMP_11": G28_COMP_11}
    return execute_calc_content(target_components, inputs)

def calc_content_29(G29_COMP_1: str, G29_COMP_3: float, G29_COMP_5: float, G29_COMP_7: float, G29_COMP_9: float) -> DG_Result_Reports:
    target_components = ['G29_COMP_2', 'G29_COMP_14', 'G29_COMP_15', 'G29_COMP_16']
    inputs = {"G29_COMP_1": G29_COMP_1, "G29_COMP_3": G29_COMP_3, "G29_COMP_5": G29_COMP_5, "G29_COMP_7": G29_COMP_7, "G29_COMP_9": G29_COMP_9}
    return execute_calc_content(target_components, inputs)

def calc_content_3(G1_COMP_1: str, G1_COMP_3: float, G1_COMP_4: float, G1_COMP_6: float, G1_COMP_7: float) -> DG_Result_Reports:
    target_components = ['G1_COMP_16', 'G1_COMP_17']
    inputs = {"G1_COMP_1": G1_COMP_1, "G1_COMP_3": G1_COMP_3, "G1_COMP_4": G1_COMP_4, "G1_COMP_6": G1_COMP_6, "G1_COMP_7": G1_COMP_7}
    return execute_calc_content(target_components, inputs)

def calc_content_30(G30_COMP_1: str, G30_COMP_6: float, G30_COMP_9: float, G30_COMP_13: float, G30_COMP_14: float, G30_COMP_16: float, G30_COMP_17: float, G30_COMP_18: float, G30_COMP_19: float, G30_COMP_20: float, G30_COMP_21: float, G30_COMP_22: float, G30_COMP_28: float) -> DG_Result_Reports:
    target_components = ['G30_COMP_23', 'G30_COMP_24', 'G30_COMP_25']
    inputs = {"G30_COMP_1": G30_COMP_1, "G30_COMP_6": G30_COMP_6, "G30_COMP_9": G30_COMP_9, "G30_COMP_13": G30_COMP_13, "G30_COMP_14": G30_COMP_14, "G30_COMP_16": G30_COMP_16, "G30_COMP_17": G30_COMP_17, "G30_COMP_18": G30_COMP_18, "G30_COMP_19": G30_COMP_19, "G30_COMP_20": G30_COMP_20, "G30_COMP_21": G30_COMP_21, "G30_COMP_22": G30_COMP_22, "G30_COMP_28": G30_COMP_28}
    return execute_calc_content(target_components, inputs)

def calc_content_31(G31_COMP_1: str, G31_COMP_2: float, G31_COMP_3: str, G31_COMP_6: str, G31_COMP_11: float, G31_COMP_19: str) -> DG_Result_Reports:
    target_components = ['G31_COMP_13', 'G31_COMP_14', 'G31_COMP_15', 'G31_COMP_16']
    inputs = {"G31_COMP_1": G31_COMP_1, "G31_COMP_2": G31_COMP_2, "G31_COMP_3": G31_COMP_3, "G31_COMP_6": G31_COMP_6, "G31_COMP_11": G31_COMP_11, "G31_COMP_19": G31_COMP_19}
    return execute_calc_content(target_components, inputs)

def calc_content_32(G31_COMP_2: float, G31_COMP_3: str, G31_COMP_6: str, G31_COMP_11: float, G32_COMP_8: str) -> DG_Result_Reports:
    target_components = ['G32_COMP_5', 'G32_COMP_6']
    inputs = {"G31_COMP_2": G31_COMP_2, "G31_COMP_3": G31_COMP_3, "G31_COMP_6": G31_COMP_6, "G31_COMP_11": G31_COMP_11, "G32_COMP_8": G32_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_33(G33_COMP_1: str, G33_COMP_2: str, G33_COMP_6: float, G33_COMP_7: float) -> DG_Result_Reports:
    target_components = ['G33_COMP_3']
    inputs = {"G33_COMP_1": G33_COMP_1, "G33_COMP_2": G33_COMP_2, "G33_COMP_6": G33_COMP_6, "G33_COMP_7": G33_COMP_7}
    return execute_calc_content(target_components, inputs)

def calc_content_34(G14_COMP_3: str, G14_COMP_4: str, G18_COMP_1: float, G33_COMP_1: str, G34_COMP_1: str, G34_COMP_2: float, G34_COMP_3: float, G34_COMP_4: float, G34_COMP_7: float, G34_COMP_8: float, G34_COMP_9: float, G34_COMP_10: float, G34_COMP_11: float, G34_COMP_12: float, G34_COMP_24: float) -> DG_Result_Reports:
    target_components = ['G34_COMP_16', 'G34_COMP_18', 'G34_COMP_25', 'G34_COMP_26']
    inputs = {"G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4, "G18_COMP_1": G18_COMP_1, "G33_COMP_1": G33_COMP_1, "G34_COMP_1": G34_COMP_1, "G34_COMP_2": G34_COMP_2, "G34_COMP_3": G34_COMP_3, "G34_COMP_4": G34_COMP_4, "G34_COMP_7": G34_COMP_7, "G34_COMP_8": G34_COMP_8, "G34_COMP_9": G34_COMP_9, "G34_COMP_10": G34_COMP_10, "G34_COMP_11": G34_COMP_11, "G34_COMP_12": G34_COMP_12, "G34_COMP_24": G34_COMP_24}
    return execute_calc_content(target_components, inputs)

def calc_content_35(G31_COMP_1: str, G31_COMP_2: float, G31_COMP_3: str, G31_COMP_6: str, G35_COMP_1: str, G35_COMP_5: float, G35_COMP_8: str, G35_COMP_10: float, G35_COMP_11: float) -> DG_Result_Reports:
    target_components = ['G35_COMP_2']
    inputs = {"G31_COMP_1": G31_COMP_1, "G31_COMP_2": G31_COMP_2, "G31_COMP_3": G31_COMP_3, "G31_COMP_6": G31_COMP_6, "G35_COMP_1": G35_COMP_1, "G35_COMP_5": G35_COMP_5, "G35_COMP_8": G35_COMP_8, "G35_COMP_10": G35_COMP_10, "G35_COMP_11": G35_COMP_11}
    return execute_calc_content(target_components, inputs)

def calc_content_36(G31_COMP_1: str, G31_COMP_2: float, G31_COMP_3: str, G31_COMP_6: str, G36_COMP_5: str, G36_COMP_10: float, G36_COMP_11: str, G36_COMP_12: float, G36_COMP_14: float, G36_COMP_16: float) -> DG_Result_Reports:
    target_components = ['G36_COMP_7', 'G36_COMP_8']
    inputs = {"G31_COMP_1": G31_COMP_1, "G31_COMP_2": G31_COMP_2, "G31_COMP_3": G31_COMP_3, "G31_COMP_6": G31_COMP_6, "G36_COMP_5": G36_COMP_5, "G36_COMP_10": G36_COMP_10, "G36_COMP_11": G36_COMP_11, "G36_COMP_12": G36_COMP_12, "G36_COMP_14": G36_COMP_14, "G36_COMP_16": G36_COMP_16}
    return execute_calc_content(target_components, inputs)

def calc_content_37(G37_COMP_1: str, G37_COMP_4: str, G37_COMP_11: float, G37_COMP_23: str, G37_COMP_27: str, G37_COMP_28: float) -> DG_Result_Reports:
    target_components = ['G37_COMP_9', 'G37_COMP_12', 'G37_COMP_16', 'G37_COMP_18', 'G37_COMP_25', 'G37_COMP_29', 'G37_COMP_32', 'G37_COMP_33']
    inputs = {"G37_COMP_1": G37_COMP_1, "G37_COMP_4": G37_COMP_4, "G37_COMP_11": G37_COMP_11, "G37_COMP_23": G37_COMP_23, "G37_COMP_27": G37_COMP_27, "G37_COMP_28": G37_COMP_28}
    return execute_calc_content(target_components, inputs)

def calc_content_38(G37_COMP_4: str, G37_COMP_27: str, G38_COMP_2: float, G38_COMP_3: float, G38_COMP_16: float, G38_COMP_18: float, G38_COMP_19: float, G38_COMP_24: float) -> DG_Result_Reports:
    target_components = ['G38_COMP_1', 'G38_COMP_4', 'G38_COMP_8']
    inputs = {"G37_COMP_4": G37_COMP_4, "G37_COMP_27": G37_COMP_27, "G38_COMP_2": G38_COMP_2, "G38_COMP_3": G38_COMP_3, "G38_COMP_16": G38_COMP_16, "G38_COMP_18": G38_COMP_18, "G38_COMP_19": G38_COMP_19, "G38_COMP_24": G38_COMP_24}
    return execute_calc_content(target_components, inputs)

def calc_content_39(G37_COMP_4: str, G37_COMP_27: str, G38_COMP_2: float, G38_COMP_16: float, G38_COMP_18: float, G38_COMP_19: float, G39_COMP_4: float, G39_COMP_8: float, G39_COMP_14: float) -> DG_Result_Reports:
    target_components = ['G39_COMP_1', 'G39_COMP_2', 'G39_COMP_3']
    inputs = {"G37_COMP_4": G37_COMP_4, "G37_COMP_27": G37_COMP_27, "G38_COMP_2": G38_COMP_2, "G38_COMP_16": G38_COMP_16, "G38_COMP_18": G38_COMP_18, "G38_COMP_19": G38_COMP_19, "G39_COMP_4": G39_COMP_4, "G39_COMP_8": G39_COMP_8, "G39_COMP_14": G39_COMP_14}
    return execute_calc_content(target_components, inputs)

def calc_content_4(G2_COMP_4: float, G2_COMP_7: float, G6_COMP_2: str) -> DG_Result_Reports:
    target_components = ['G2_COMP_1', 'G2_COMP_5', 'G2_COMP_6']
    inputs = {"G2_COMP_4": G2_COMP_4, "G2_COMP_7": G2_COMP_7, "G6_COMP_2": G6_COMP_2}
    return execute_calc_content(target_components, inputs)

def calc_content_40(G40_COMP_1: str, G40_COMP_4: str, G40_COMP_7: str, G40_COMP_9: str, G40_COMP_11: str, G40_COMP_13: str, G40_COMP_15: str, G40_COMP_17: str, G40_COMP_20: str, G40_COMP_22: float, G40_COMP_25: str, G40_COMP_26: str, G40_COMP_27: str) -> DG_Result_Reports:
    target_components = ['G40_COMP_2', 'G40_COMP_3', 'G40_COMP_5']
    inputs = {"G40_COMP_1": G40_COMP_1, "G40_COMP_4": G40_COMP_4, "G40_COMP_7": G40_COMP_7, "G40_COMP_9": G40_COMP_9, "G40_COMP_11": G40_COMP_11, "G40_COMP_13": G40_COMP_13, "G40_COMP_15": G40_COMP_15, "G40_COMP_17": G40_COMP_17, "G40_COMP_20": G40_COMP_20, "G40_COMP_22": G40_COMP_22, "G40_COMP_25": G40_COMP_25, "G40_COMP_26": G40_COMP_26, "G40_COMP_27": G40_COMP_27}
    return execute_calc_content(target_components, inputs)

def calc_content_5(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str, G5_COMP_6: float, G5_COMP_7: float, G5_COMP_8: str, G5_COMP_9: str, G5_COMP_11: float, G5_COMP_12: str, G5_COMP_17: float) -> DG_Result_Reports:
    target_components = ['G5_COMP_1', 'G5_COMP_13', 'G5_COMP_16']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15, "G5_COMP_6": G5_COMP_6, "G5_COMP_7": G5_COMP_7, "G5_COMP_8": G5_COMP_8, "G5_COMP_9": G5_COMP_9, "G5_COMP_11": G5_COMP_11, "G5_COMP_12": G5_COMP_12, "G5_COMP_17": G5_COMP_17}
    return execute_calc_content(target_components, inputs)

def calc_content_6(G6_COMP_2: str, G6_COMP_4: float, G6_COMP_6: str, G6_COMP_9: float, G6_COMP_10: float, G6_COMP_11: float) -> DG_Result_Reports:
    target_components = ['G6_COMP_1']
    inputs = {"G6_COMP_2": G6_COMP_2, "G6_COMP_4": G6_COMP_4, "G6_COMP_6": G6_COMP_6, "G6_COMP_9": G6_COMP_9, "G6_COMP_10": G6_COMP_10, "G6_COMP_11": G6_COMP_11}
    return execute_calc_content(target_components, inputs)

def calc_content_7(G7_COMP_3: float, G7_COMP_4: float, G7_COMP_8: float) -> DG_Result_Reports:
    target_components = ['G7_COMP_1', 'G7_COMP_2', 'G7_COMP_7', 'G7_COMP_9']
    inputs = {"G7_COMP_3": G7_COMP_3, "G7_COMP_4": G7_COMP_4, "G7_COMP_8": G7_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_8(G8_COMP_3: float, G8_COMP_4: float, G8_COMP_8: float) -> DG_Result_Reports:
    target_components = ['G8_COMP_1', 'G8_COMP_2', 'G8_COMP_10', 'G8_COMP_11', 'G8_COMP_12', 'G8_COMP_13']
    inputs = {"G8_COMP_3": G8_COMP_3, "G8_COMP_4": G8_COMP_4, "G8_COMP_8": G8_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_9(G8_COMP_8: float, G9_COMP_4: float, G9_COMP_5: str, G9_COMP_8: float, G9_COMP_17: float) -> DG_Result_Reports:
    target_components = ['G9_COMP_1', 'G9_COMP_2', 'G9_COMP_11', 'G9_COMP_13', 'G9_COMP_14']
    inputs = {"G8_COMP_8": G8_COMP_8, "G9_COMP_4": G9_COMP_4, "G9_COMP_5": G9_COMP_5, "G9_COMP_8": G9_COMP_8, "G9_COMP_17": G9_COMP_17}
    return execute_calc_content(target_components, inputs)

if __name__ == "__main__":
    inp = {
        "dgnsitu": "Persistent",
        "strenghtclass": "C30/37",
        "sectType": "Reinforced concrete section",
        "vEd": 350,
        "nEd": 1850,
        "phiSl": 32,
        "nSl": 4,
        "bW": 300,
        "d": 450,
        "aC": 35,
        "aV": 100
    }
    

