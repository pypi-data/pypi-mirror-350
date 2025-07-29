import json
import moapy.plugins.Extrude_frame_offset.sub_function as sf
from moapy.auto_convert import auto_schema, MBaseModel
from pydantic import Field

class ExtrudeFrameOffset(MBaseModel):
    """Extrude Frame Offset Input Class

    Args:
        local_axis (str): local axis
        extrude_length (str): extrude length
        matl_id (int): matl_id
        sect_id (int): sect_id
    """
    local_axis: str = Field(default="+y", description="local axis")
    extrude_length: str = Field(default="4@1", description="extrude length")
    matl_id: int = Field(default=1, description="matl_id")
    sect_id: int = Field(default=1, description="sect_id")

@auto_schema(title="Extrude Frame Offset", description="Extrude Frame Offset")
def extrude_frame_offset(Input: ExtrudeFrameOffset)->str:
    """extrude_frame_offset

    Args:
        local_axis (str): local axis
        extrude_length (str): extrude length
        matl_id (int): matl_id
        sect_id (int): sect_id

    Returns:
        str: success or error message
    """
    local_axis = Input.local_axis
    extrude_length = Input.extrude_length
    matl_id = Input.matl_id
    sect_id = Input.sect_id

    # Check input - extrude_length
    extrude = sf.parse_unequal_value(extrude_length)
    if len(extrude) == 0:
        message = {"error": "Invalid extrude length."}
        return json.dumps(message)
    
    # Check input - local_axis
    if local_axis not in ["+y", "-y", "+z", "-z"]:
        message = {"error": "Invalid local axis."}
        return json.dumps(message)

    # Check input - matl_id
    check_id = sf.validate_integer_range(matl_id)
    if check_id["validation"] == False:
        message = {"error": check_id["message"]}
        return json.dumps(message)

    # Check input - sect_id
    check_id = sf.validate_integer_range(sect_id)
    if check_id["validation"] == False:
        message = {"error": check_id["message"]}
        return json.dumps(message)    

    # Get Seleteted Element List
    select_elem = sf.select_element_list()
    if select_elem == None:
        message = {"error": "No selected elements."}
        return json.dumps(message)
    
    # Check Selected Element Validation
    check_result = sf.continous_element_check(select_elem)
    if check_result["validation"] == False:
        return json.dumps(check_result)
    
    # Get Ordered node list from Selected Elements
    ordered_node_list = sf.ordered_node_list(select_elem)
    
    # Get Node Coordinates
    node_coords = sf.node_coordinates(ordered_node_list)
    
    # 3D Cubic Line Fitting
    local_vector_list = sf.Local_vector_from_CubicSpline(node_coords)

    # Local Angle list
    local_angle_list = sf.find_angle_from_vector(local_vector_list)

    # Assign Node Skew Angle to Selected Elements
    res_skew = sf.assign_skew_angle(ordered_node_list, local_angle_list)
    if not "SKEW" in res_skew.keys():
        return json.dumps(res_skew)

    # Check empty node ids in the model
    start_node_id = sf.check_empty_node_id(extrude, ordered_node_list)
    if start_node_id == 0:
        message = {"error": "Not enough node IDs."}
        return json.dumps(message)
    
    # Create New Nodes with Skew
    res_node, res_skew = sf.create_new_node_with_skew(extrude, local_axis, ordered_node_list, node_coords, start_node_id, local_vector_list, local_angle_list)
    if not "NODE" in res_node.keys():
        return json.dumps(res_node)
    if not "SKEW" in res_skew.keys():
        return json.dumps(res_skew)

    # Check empty element ids in the model
    start_elem_id = sf.check_empty_elem_id(extrude, ordered_node_list)
    if start_elem_id == 0:
        message = {"error": "Not enough element IDs."}
        return json.dumps(message)
    
    # Create New Elements
    res_elem = sf.create_new_element(extrude, ordered_node_list, res_node, start_elem_id, matl_id, sect_id)

    if not "ELEM" in res_elem.keys():
        return json.dumps(res_elem)

    return json.dumps({"success": "Extrude Success"})

# Test
return_message = extrude_frame_offset(**{"Input":{"local_axis":"+y","extrude_length":"4@1","matl_id":1,"sect_id":1}})
