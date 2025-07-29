import moapy.plugins.flared_pier.flared_pier_modeling as fpm
import json

from moapy.engineers import MidasAPI, Product
from moapy.vector import VectorCalculation as vc
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel

class CreatePier(MBaseModel):
    """
    Create Pier Input Class
    
    Args:
        column_sect_ID (int): column section ID
        cap_bot_sect_ID (int): cap bottom section ID
        cap_top_sect_ID (int): cap top section ID
        column_matl_ID (int): column material ID
        cap_bot_matl_ID (int): cap bottom material ID
        cap_top_matl_ID (int): cap top material ID
        start_node_nb (int): start node number
        column_len (float): column length
        cap_bot_len (float): cap bottom length
        cap_top_len (float): cap top length
        grup_ID (int): group ID
        bngr_ID (int): boundary group ID
    """

    column_sect_ID: int = Field(default=2, description="column section ID")
    cap_bot_sect_ID: int = Field(default=4, description="cap bottom section ID")
    cap_top_sect_ID: int = Field(default=3, description="cap top section ID")
    column_matl_ID: int = Field(default=2, description="column material ID")
    cap_bot_matl_ID: int = Field(default=2, description="cap bottom material ID")
    cap_top_matl_ID: int = Field(default=2, description="cap top material ID")
    start_node_nb: int = Field(default=10000, description="start node number")
    column_len: float = Field(default=12, description="column length")
    cap_bot_len: float = Field(default=1.2, description="cap bottom length")
    cap_top_len: float = Field(default=0.5, description="cap top length")
    grup_ID: int = Field(default=4, description="group ID")
    bngr_ID: int = Field(default=1, description="boundary group ID")

@auto_schema(title="Create Pier", description="Create Pier")
def create_pier(input: CreatePier) -> str:
    """create_pier
    
    Args:
        input (CreatePier): Create Pier Input Class

    Returns:
        str: result
    """
    column_sect_ID = input.column_sect_ID
    cap_bot_sect_ID = input.cap_bot_sect_ID
    cap_top_sect_ID = input.cap_top_sect_ID
    column_matl_ID = input.column_matl_ID
    cap_bot_matl_ID = input.cap_bot_matl_ID
    cap_top_matl_ID = input.cap_top_matl_ID
    start_node_nb = input.start_node_nb
    column_len = input.column_len
    cap_bot_len = input.cap_bot_len
    cap_top_len = input.cap_top_len
    grup_ID = input.grup_ID
    bngr_ID = input.bngr_ID

    # Get selected node list from Civil 
    select_node = MidasAPI.view_select_get().get("NODE_LIST")

    if select_node == None or len(select_node) == 0:
        error_message = {"error":"Please select nodes"}
        return json.dumps(error_message)
    
    if len(select_node) <= 1:
        error_message = {"error":"Please select more than 2 nodes"}
        return json.dumps(error_message)

    # Check selected node has same local axis
    res_skew = MidasAPI.db_read("SKEW")

    if res_skew == None:
        same_local_axis = True
    else:
        skew_data = []
        for i in range(len(select_node)):
            if select_node[i] in res_skew.keys():
                skew_data.append(res_skew[select_node[i]])
            else:
                skew_data.append(0)
        same_local_axis = all(element == skew_data[0] for element in skew_data)

    if same_local_axis == False:
        error_message = {"error":"Please select nodes that have same local axis"}
        return json.dumps(error_message)

    # -------------------------------------------------------------------
    # Input from UI
    # -------------------------------------------------------------------
    res_grup = MidasAPI.db_read("GRUP")
    res_bngr = MidasAPI.db_read("BNGR")

    res_matl = MidasAPI.db_read("MATL")
    res_sect = MidasAPI.db_read("SECT")

    if not column_sect_ID in res_sect.keys():
        error_message = {"error":"There is no select section ID for column, please click the refresh button"}
        return json.dumps(error_message)
    elif not cap_bot_sect_ID in res_sect.keys():
        error_message = {"error":"There is no select section ID for cap bot, please click the refresh button"}
        return json.dumps(error_message)
    elif not cap_top_sect_ID in res_sect.keys():
        error_message = {"error":"There is no select section ID for cap top, please click the refresh button"}
        return json.dumps(error_message)

    if not column_matl_ID in res_matl.keys():
        error_message = {"error":"There is no select material ID for column, please click the refresh button"}
        return json.dumps(error_message)
    elif not cap_bot_matl_ID in res_matl.keys():
        error_message = {"error":"There is no select material ID for cap bot, please click the refresh button"}
        return json.dumps(error_message)
    elif not cap_top_matl_ID in res_matl.keys():
        error_message = {"error":"There is no select material ID for cap top, please click the refresh button"}
        return json.dumps(error_message)

    # -------------------------------------------------------------------
    # Create column
    # -------------------------------------------------------------------
    # x, y, z coordinate of selected nodes
    res_node = MidasAPI.db_read("NODE")
    mid_x, mid_y, mid_z = fpm.find_center_node(select_node, res_node)

    skew_info = MidasAPI.db_read_item("SKEW", select_node[0])
    node_normalz_vector = vc.nomarlz_vector_skew_info(skew_info)
    node_origin_coords = [mid_x, mid_y, mid_z]
    node_origin_angle = vc.find_angle_from_vector(node_normalz_vector)

    # Create Data 
    sect_ID = [column_sect_ID, cap_bot_sect_ID, cap_top_sect_ID]
    matl_ID = [column_matl_ID, cap_bot_matl_ID, cap_top_matl_ID]

    pier_node_body, pier_elem_body = fpm.create_flared_pier_data(start_node_nb, sect_ID, matl_ID, column_len, cap_bot_len, cap_top_len)

    # Create Pier Node
    for key, value in pier_node_body.items():
        pier_node_coords = [value["X"], value["Y"], value["Z"]]
        global_point = vc.convert_to_global_coordinates(node_origin_coords, node_normalz_vector, pier_node_coords)
        pier_node_body[key]["X"] = global_point[0]
        pier_node_body[key]["Y"] = global_point[1]
        pier_node_body[key]["Z"] = global_point[2]

    # Calculate element angle
    units_z = [0, 0, 1]
    node_vector_coords = vc.convert_to_global_coordinates(node_origin_coords, node_normalz_vector, units_z)
    pier_elem_vector = vc.local_vector_from_2points(node_origin_coords, node_vector_coords)
    elem_angle = vc.find_angle_to_fit_vector("+Z", pier_elem_vector, node_normalz_vector)

    # Update Pier Element Angle
    for key, value in pier_elem_body.items():
        pier_elem_body[key]["ANGLE"] = elem_angle

    # Create Pier Node Angle
    pier_anlge_body = {}
    for key, value in pier_node_body.items():
        pier_anlge_body[key] = {
            "iMETHOD": 1,
            "ANGLE_X": node_origin_angle[0],
            "ANGLE_Y": node_origin_angle[1],
            "ANGLE_Z": node_origin_angle[2],
        }
    
    # Check Node and Element Data
    res_node = MidasAPI.db_read("NODE")
    res_elem = MidasAPI.db_read("ELEM")

    exist_node_list = list(res_node.keys())
    exist_elem_list = list(res_elem.keys())

    new_node_list = list(pier_node_body.keys())
    new_elem_list = list(pier_elem_body.keys())

    combined_node_list = exist_node_list + new_node_list
    combined_elem_list = exist_elem_list + new_elem_list

    node_range = str(min(new_node_list)) + " ~ " + str(max(new_node_list))
    elem_range = str(min(new_elem_list)) + " ~ " + str(max(new_elem_list))
    
    if len(combined_node_list) != len(set(combined_node_list)):        
        error_message = {"error":"There are same node number (" + node_range + ")"}
        return json.dumps(error_message)

    if len(combined_elem_list) != len(set(combined_elem_list)):
        error_message = {"error":"There are same element number (" + elem_range + ")"}
        return json.dumps(error_message)

    # Create Pier
    MidasAPI.db_create("NODE", pier_node_body)
    MidasAPI.db_create("ELEM", pier_elem_body)
    MidasAPI.db_update("SKEW", pier_anlge_body)

    # Update Structure Group
    if grup_ID != 0:
        grup_body = fpm.create_structure_group(grup_ID, select_node, pier_node_body, pier_elem_body)
        MidasAPI.db_update("GRUP", grup_body)

    # Create Rigid Link
    res_rigd = MidasAPI.db_read("RIGD")
    if bngr_ID != 0:
        bngr_name = res_bngr[bngr_ID]["NAME"]
    else:
        bngr_name = ""
    top_node_nb = max(pier_node_body.keys())
    rigd_body = fpm.create_boundary_condtions(bngr_name, res_rigd, select_node, top_node_nb)

    MidasAPI.db_update("RIGD", rigd_body)

    result_message = {"success":"Flared pier modeling is completed"}
    return json.dumps(result_message)

# ===================================================================
# TEST FIELD
# ===================================================================
    
create_modeling = create_pier(CreatePier())
#     2, #column_sect_ID:int,
#     4, #cap_bot_sect_ID:int,
#     3, #cap_top_sect_ID:int,
#     2, #column_matl_ID:int,
#     2, #cap_bot_matl_ID:int, 
#     2, #cap_top_matl_ID:int,
#     10000, #start_node_nb:int,
#     12, #column_len:float,
#     1.2, #cap_bot_len:float,
#     0.5, #cap_top_len:float,
#     4, #grup_ID:int,
#     1, #bngr_ID:int,
# )

print(create_modeling)