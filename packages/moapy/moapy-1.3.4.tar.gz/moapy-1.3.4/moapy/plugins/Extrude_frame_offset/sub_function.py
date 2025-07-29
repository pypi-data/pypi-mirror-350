from moapy.engineers import MidasAPI
import numpy as np
import copy
from collections import Counter
from scipy.interpolate import CubicSpline

def select_element_list(
    ) -> list[int]:
    """
    Get the selected element list from the MIDAS API.

    Args:
        product (str): The product name.
        country (str): The country code.

    Returns:
        list[int]: The list of selected element IDs.
    """
    
    # Get Selected Elements
    res_select = MidasAPI.view_select_get()
    if res_select == None:
        return []
    
    return res_select.get("ELEM_LIST")

def continous_element_check(
        elem_list: list[int],
    )-> dict:
    """
    Check if the selected elements are continuous.

    Args:
        product (str): The product name.
        country (str): The country code.
        elem_list (list[int]): The list of selected element IDs.

    Returns:
        dict: A dictionary containing the validation result and message.
    """
    
    res_elem = MidasAPI.db_read("ELEM")
    
    # Get Node IDs from selected elements
    node_list = []
    for _, value in enumerate(elem_list):
        node_list.append([res_elem[value]["NODE"][0], res_elem[value]["NODE"][1]])

    # Flatten the node_list
    flat_node_list = [item for sublist in node_list for item in sublist]

    # Count the number of nodes
    counter = Counter(flat_node_list)

    # Count how many times each node appears
    once_node = [num for num, count in counter.items() if count == 1]
    # twice_node = [num for num, count in counter.items() if count == 2]
    more_than_twice_node = [num for num, count in counter.items() if count > 2]

    # Return value
    return_value = {
        "validation": True,
        "message": "Selected elements are valid."
    }

    # Check Validation
    if len(once_node) != 2 or len(more_than_twice_node) != 0:
        return_value["validation"] = False
        return_value["message"] = "The selected elements are not continuous."
        return return_value
    
    return return_value

def ordered_node_list(
        elem_list: list[int],
        start_option: str = "min",
    ):
    """
    Get the ordered node list from the selected element list.

    Args:
        elem_list (list[int]): The list of selected element IDs.
        start_option (str): The option to determine the starting node. The options are 'min' and 'max'.
        product (str): The product name.
        country (str): The country code.

    Returns:
        list[int]: The ordered node list.
    """
    
    res_elem = MidasAPI.db_read("ELEM")
    
    # Get Node IDs from selected elements
    node_list = []
    for _, value in enumerate(elem_list):
        node_list.append([res_elem[value]["NODE"][0], res_elem[value]["NODE"][1]])
    
    # Flatten the node_list
    flat_node_list = [item for sublist in node_list for item in sublist]

    # Count the number of nodes
    counter = Counter(flat_node_list)

    # Count how many times each node appears
    once_node = [num for num, count in counter.items() if count == 1]
    
    # Start node number
    if start_option == "min":
        start_node = min(once_node)
    elif start_option == "max":
        start_node = max(once_node)

    # Create ordered node list
    ordered_node_list = [start_node]
    all_node_list = copy.deepcopy(node_list)

    while len(all_node_list) > 0:
        for i in range(len(all_node_list)):
            if start_node in all_node_list[i]:
                if start_node == all_node_list[i][0]:
                    start_node = all_node_list[i][1]
                else:
                    start_node = all_node_list[i][0]
                ordered_node_list.append(start_node)
                all_node_list.pop(i)
                break
    
    return ordered_node_list

def node_coordinates(
        node_list: list[int],
    ):
    """
    Get the node coordinates from the node list.

    Args:
        node_list (list[int]): The list of node IDs.
        product (str): The product name.
        country (str): The country code.

    Returns:
        dict: A dictionary containing the node ID and coordinates.
    """
    res_node = MidasAPI.db_read("NODE")

    # Get Node Coordinates
    node_coordinates = []
    for _, value in enumerate(node_list):
        node_coordinates.append([
            res_node[value]["X"],
            res_node[value]["Y"],
            res_node[value]["Z"]
        ])

    return node_coordinates

def nomalize_vector(
        vector: list[float, float, float]
    )-> list[float, float, float]:
    """
    Normalize the vector.

    Args:
        vector (list[float, float, float]): The vector to be normalized.

    Returns:
        list[float, float, float]: The normalized vector.
    """
    normalz_vector = np.array(vector)
    if np.linalg.norm(normalz_vector) == 0:
        return normalz_vector
    else:
        normalz_vector = normalz_vector / np.linalg.norm(normalz_vector)
    return normalz_vector

def local_vector_from_2points(
        start_point: list[float, float, float],
        end_point: list[float, float, float]
    )-> list[float, float, float]:
    """
    Calculate the local coordinate system from two points.

    Args:
        start_point (list[float, float, float]): The starting point coordinates.
        end_point (list[float, float, float]): The ending point coordinates.
    
    Returns:
        list[float, float, float]: The local coordinate system.
    """

    start_point = np.array(start_point)
    end_point = np.array(end_point)

    line_vector = end_point - start_point

    local_x = nomalize_vector(line_vector)
    if np.allclose(local_x, np.array([0,0,1]), atol=1e-6):
        local_y = np.array([0,-1,0])
        local_z = np.array([1,0,0])
    elif np.allclose(local_x, np.array([0,0,-1]), atol=1e-6):
        local_y = np.array([0,1,0])
        local_z = np.array([1,0,0])
    elif np.allclose(local_x, np.array([0,1,0]), atol=1e-6):
        local_y = np.array([-1,0,0])
        local_z = np.array([0,0,1])
    elif np.allclose(local_x, np.array([0,-1,0]), atol=1e-6):
        local_y = np.array([1,0,0])
        local_z = np.array([0,0,1])
    elif np.allclose(local_x, np.array([1,0,0]), atol=1e-6):
        local_y = np.array([0,1,0])
        local_z = np.array([0,0,1])
    elif np.allclose(local_x, np.array([-1,0,0]), atol=1e-6):
        local_y = np.array([0,-1,0])
        local_z = np.array([0,0,1])
    else:
        local_y = np.cross(np.array([0,0,1]), local_x)
        local_y = nomalize_vector(local_y)
        local_z = np.cross(local_x, local_y)
        local_z = nomalize_vector(local_z)

    return local_x, local_y, local_z

def Local_vector_from_CubicSpline(
        node_coordinates: list[list[float, float, float]]
    )-> list[list[float, float, float]]:
    """
    Calculate the local coordinate system from the cubic spline.

    Args:
        node_coordinates (list[list[float, float, float]]): The list of node coordinates.

    Returns:
        list[list[float, float, float]]: The local coordinate system.
    """
    # Split the node_coordinates
    node_x = [sublist[0] for sublist in node_coordinates if sublist]
    node_y = [sublist[1] for sublist in node_coordinates if sublist]
    node_z = [sublist[2] for sublist in node_coordinates if sublist]
    
    # Distances between nodes and total distance
    distances = np.sqrt(np.diff(node_x)**2 + np.diff(node_y)**2 + np.diff(node_z)**2)
    t = np.insert(np.cumsum(distances), 0, 0)

    # Fitting Splines
    cs_x = CubicSpline(t, node_x)
    cs_y = CubicSpline(t, node_y)
    cs_z = CubicSpline(t, node_z)

    # Calculating derivatives at the original points for directions vectors
    dx_dt = cs_x(t, 1)
    dy_dt = cs_y(t, 1)
    dz_dt = cs_z(t, 1)

    # Normalizing the direction vectors
    norms = np.sqrt(dx_dt**2 + dy_dt**2 + dz_dt**2)
    dx_dt /= norms
    dy_dt /= norms
    dz_dt /= norms

    # Calculating local coordinate systems for each point
    local_vector_list = []
    for i in range(len(node_coordinates)):
        local_x, local_y, local_z = local_vector_from_2points(
            [node_coordinates[i][0], node_coordinates[i][1], node_coordinates[i][2]],
            [node_coordinates[i][0]+dx_dt[i], node_coordinates[i][1]+dy_dt[i], node_coordinates[i][2]+dz_dt[i]]
        )
        local_vector_list.append([local_x, local_y, local_z])
    
    return local_vector_list

def find_angle_from_vector(
        local_vector_list: list[list[float, float, float]]
    )-> list[list[float, float, float]]:
    """
    Calculate the angles from the local vectors.

    Args:
        local_vector_list (list[list[float, float, float]]): The list of local vectors.

    Returns:
        list[list[float, float, float]]: The list of angles.
    """

    local_angle_list = []
    for _, local_vector in enumerate(local_vector_list):
        local_x = local_vector[0]
        local_y = local_vector[1]
        local_z = local_vector[2]

        global_x = np.array([1,0,0])
        global_y = np.array([0,1,0])
        global_z = np.array([0,0,1])

        local_basis = np.column_stack((local_x, local_y, local_z))
        global_basis = np.column_stack((global_x, global_y, global_z))

        dcm = np.dot(local_basis, global_basis.T)

        angle_x = np.arctan2(dcm[2, 1], dcm[2, 2])
        angle_y = np.arctan2(-dcm[2, 0], np.sqrt(dcm[2, 1]**2 + dcm[2, 2]**2))
        angle_z = np.arctan2(dcm[1, 0], dcm[0, 0])

        angle_x_deg = np.degrees(angle_x)
        angle_y_deg = np.degrees(angle_y)
        angle_z_deg = np.degrees(angle_z)

        local_angle_list.append([angle_x_deg, angle_y_deg, angle_z_deg])

    return local_angle_list

def parse_unequal_value(
        value:str
    )-> list[float]:
    """
    Parse the extended format of the unequal_value string to create a list.
    The format can include both numbers and 'Integer@Real' pairs, separated by commas.

    Args:
        value (str): The string to be parsed.

    Returns:
        list[float]: The parsed list.
    """
    parsed_list = []
    elements = value.split(',')
    
    for element in elements:
        try:
            # Check if the element contains '@'
            if '@' in element:
                number, repeat_value = element.split('@')
                parsed_list.extend([float(repeat_value)] * int(number))
            else:
                parsed_list.append(float(element))
        except ValueError:
            # Return an empty list if there's a parsing error
            return []

    return parsed_list

def validate_integer_range(
        value: int
    ) -> int:
    """
    Validate the input value to check if it's an integer within the specified range.

    Args:
        value (int): The input value.

    Returns:
        dict: A dictionary containing the validation result and message.
    """
    # Return value
    return_value = {
        "validation": True,
        "message": ""
    }
    # Check if the input is an integer
    try:
        number = int(value)
    except ValueError:
        return_value["validation"] = False
        return_value["message"] = "Invalid input. Please enter an integer."
        return return_value
    # Check if the input is within the specified range
    if not 0 <= number <= 999999:
        return_value["validation"] = False
        return_value["message"] = "Invalid input. Please enter an integer between 0 and 999999."
        return return_value

    return return_value

def assign_skew_angle(
        node_list: list[int],
        angel_list: list[list[float, float, float]],
)->dict:

    skew_json = {}
    for i in range(len(node_list)):
        skew_json[node_list[i]] = {
            "iMETHOD":1,
            "ANGLE_X": angel_list[i][0],
            "ANGLE_Y": angel_list[i][1],
            "ANGLE_Z": angel_list[i][2]
        }

    res_skew = MidasAPI.db_update("SKEW", skew_json)

    return res_skew

def check_empty_node_id(
        extrude: list[float],
        node_list: list[int],
        product: str = "CIVIL",
        country: str = "KR"
    )->int:
    """
    Check if there are empty node IDs.

    Args:
        extrude (list[float]): The extrude length.
        node_list (list[int]): The list of node IDs.
        product (str): The product name.
        country (str): The country code.

    Returns:
        int: The starting node ID for the new nodes.
    """
    
    # Existing Node IDs
    res_node = MidasAPI.db_read("NODE")
    res_node_id = list(res_node.keys())

    # Number of new nodes
    nb_new_node = len(extrude) * len(node_list)
    
    # Find the starting node ID for the new nodes
    missing_ranges_with_values = []

    # A list of the first number is not 1
    if res_node_id[0] > 1:
        missing_ranges_with_values.append((0, 1, res_node_id[0] - 1))

    # Find the missing number range in the A list
    for i in range(len(res_node_id) - 1):
        if res_node_id[i] + 1 < res_node_id[i + 1]:
            # Calculate the start index, its value, and the length of the missing numbers
            start = i + 1
            start_value = res_node_id[i] + 1
            length = res_node_id[i + 1] - res_node_id[i] - 1
            missing_ranges_with_values.append((start, start_value, length))

    # If the last number in the A list is less than 999999
    if res_node_id[-1] < 999999:
        missing_ranges_with_values.append((len(res_node_id), res_node_id[-1] + 1, 999999 - res_node_id[-1]))

    # Check if there are empty node IDs
    missing_check = False
    for i in range(len(missing_ranges_with_values)):
        if missing_ranges_with_values[i][2] >= nb_new_node:
            missing_check = True
            new_node_start = missing_ranges_with_values[i][1]
            return new_node_start
    if missing_check == False:
        return 0

def create_new_node_with_skew(
        extrude: list[float],
        local_axis: str,
        node_list: list[int],
        node_coordinates: list[list[float, float, float]],
        start_node_id: int,
        local_vector_list: list[list[float, float, float]],
        local_angle_list: list[list[float, float, float]],
    )->dict:
    """
    Create new nodes with skew angles.

    Args:
        extrude (list[float]): The extrude length.
        local_axis (str): The local axis.
        node_list (list[int]): The list of node IDs.
        node_coordinates (list[list[float, float, float]]): The list of node coordinates.
        start_node_id (int): The starting node ID for the new nodes.
        local_vector_list (list[list[float, float, float]]): The list of local vectors.
        local_angle_list (list[list[float, float, float]]): The list of local angles.
        product (str): The product name.
        country (str): The country code.

    Returns:
        dict: The result of creating new nodes and skew angles.
    """

    # Extrude Length
    extrude = np.cumsum(extrude)

    # Split the node_coordinates
    node_x = [sublist[0] for sublist in node_coordinates if sublist]
    node_y = [sublist[1] for sublist in node_coordinates if sublist]
    node_z = [sublist[2] for sublist in node_coordinates if sublist]

    # Create New Nodes and Skew
    new_node_json = {}
    new_skew_json = {}
    for i in range(len(extrude)):
        for j in range(len(node_list)):
            origin = np.array([node_x[j], node_y[j], node_z[j]])
            if local_axis == "+y":
                coords = origin + local_vector_list[j][1]*extrude[i]
            elif local_axis == "-y":
                coords = origin + local_vector_list[j][1]*extrude[i]*-1
            elif local_axis == "+z":
                coords = origin + local_vector_list[j][2]*extrude[i]
            elif local_axis == "-z":
                coords = origin + local_vector_list[j][2]*extrude[i]*-1
            new_node_json[start_node_id] = {
                "X": coords[0],
                "Y": coords[1],
                "Z": coords[2],
            }
            new_skew_json[start_node_id] = {
                "iMETHOD":1,
                "ANGLE_X": local_angle_list[j][0],
                "ANGLE_Y": local_angle_list[j][1],
                "ANGLE_Z": local_angle_list[j][2]
            }
            start_node_id += 1
    
    res_create_node = MidasAPI.db_create("NODE", new_node_json)
    res_create_skew = MidasAPI.db_update("SKEW", new_skew_json)

    return res_create_node, res_create_skew

def check_empty_elem_id(
        extrude: list[float],
        node_list: list[int],
    )->int:
    """
    Check if there are empty element IDs.

    Args:
        extrude (list[float]): The extrude length.
        node_list (list[int]): The list of node IDs.
        product (str): The product name.
        country (str): The country code.

    Returns:
        int: The starting element ID for the new elements.
    """
    
    # Existing Node IDs
    res_elem = MidasAPI.db_read("ELEM")
    
    if "error" in res_elem.keys():
        return 1
    else:
        res_elem_id = list(res_elem.keys())
                # Find the starting node ID for the new nodes
        missing_ranges_with_values = []

        # A list of the first number is not 1
        if res_elem_id[0] > 1:
            missing_ranges_with_values.append((0, 1, res_elem_id[0] - 1))

        # Find the missing number range in the A list
        for i in range(len(res_elem_id) - 1):
            if res_elem_id[i] + 1 < res_elem_id[i + 1]:
                # Calculate the start index, its value, and the length of the missing numbers
                start = i + 1
                start_value = res_elem_id[i] + 1
                length = res_elem_id[i + 1] - res_elem_id[i] - 1
                missing_ranges_with_values.append((start, start_value, length))

        # If the last number in the A list is less than 999999
        if res_elem_id[-1] < 999999:
            missing_ranges_with_values.append((len(res_elem_id), res_elem_id[-1] + 1, 999999 - res_elem_id[-1]))

        # Check if there are empty node IDs
        missing_check = False
        for i in range(len(missing_ranges_with_values)):
            if missing_ranges_with_values[i][2] >=  len(extrude) * (len(node_list) - 1):
                missing_check = True
                new_node_start = missing_ranges_with_values[i][1]
                return new_node_start
        if missing_check == False:
            return 0
        
def create_new_element(
        extrude: list[float],
        node_list: list[int],
        new_node_json: dict,
        start_elem_id: int,
        matl_id: int,
        sect_id: int,
)->dict:
    """
    Create new elements.

    Args:
        extrude (list[float]): The extrude length.
        node_list (list[int]): The list of node IDs.
        new_node_json (dict): The dictionary containing the new node information.
        start_elem_id (int): The starting element ID for the new elements.
        matl_id (int): The material ID.
        sect_id (int): The section ID.
        product (str): The product name.
        country (str): The country code.

    Returns:
        dict: The result of creating new elements.
    """

    # Create New Elements
    node_id_for_plate = node_list + [int(key) for key in new_node_json["NODE"].keys()]

    divide_nb = len(node_list)
    new_elem_json = {}
    for i in range(len(extrude)):
        index_1 = i * divide_nb
        index_2 = (i+1) * divide_nb
        for j in range(len(node_list)-1):
            new_elem_json[start_elem_id] = {
                "TYPE": "PLATE",
                "MATL": matl_id,
                "SECT": sect_id,
                "NODE": [
                    node_id_for_plate[index_1 + j],
                    node_id_for_plate[index_1 + j + 1],
                    node_id_for_plate[index_2 + j + 1],
                    node_id_for_plate[index_2 + j]
                    ],
                "STYPE":1
            }
            start_elem_id += 1
    
    res_create_elem = MidasAPI.db_create("ELEM", new_elem_json)

    return res_create_elem