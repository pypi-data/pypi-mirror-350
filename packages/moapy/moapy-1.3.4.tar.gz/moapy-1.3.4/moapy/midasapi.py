import os
from dataclasses import dataclass
from typing import List, Optional, Union

# pyscript 환경 감지
try:
    from pyscript import document  # noqa: F401
    ENV = 'pyscript'
except ImportError:
    ENV = os.getenv('ENV', 'local')  # 기본값은 'local'입니다.


# # server 환경에서 실행
# export ENV=server
# python script.py
if ENV == 'server':
    from moapy.midasutil_server import midas_util, Product
elif ENV == 'pyscript':
    from moapy.midasutil_web import midas_util, Product
else:
    from moapy.midasutil import midas_util, Product

from enum import Enum

global g_base_url, g_headers
g_base_url = midas_util.get_base_url(Product.CIVIL)
g_headers = {
    'MAPI-Key': midas_util.get_MAPI_Key(Product.CIVIL),
    'Content-Type': 'application/json'
}


class MidasAPI:
    base_url = g_base_url
    headers = g_headers

    class AnalysisType(Enum):
        ANALYSIS = "Analysis"
        PUSHOVER = "Pushover"

    @dataclass
    class tableFormat:
        """
        Standard table format for the MIDAS API
        {
            "HEAD": ["Strain", "Stress"],
            "DATA": [[0.1, 2, 4, 4, 35], [0, 234235, 235, 235, 0]],
        }
        """
        HEAD: list[str , 2]
        DATA: list[list[float , 2]]

    @classmethod
    def create_instance(cls, product, country="KR"):
        cls.base_url = midas_util.get_base_url(product, country)
        cls.headers = {
            'MAPI-Key': midas_util.get_MAPI_Key(product, country),
            'Content-Type': 'application/json'
        }
        return cls()

    @classmethod
    def doc_open(cls, file_path):
        url = f'{cls.base_url}/doc/open'
        return midas_util.post(url, headers=cls.headers, json={'Argument': file_path})

    @classmethod
    def doc_close(self):
        url = f'{self.base_url}/doc/close'
        return midas_util.post(url, headers=self.headers, json={})

    @classmethod
    def doc_save(self, file_path: str = ''):
        if file_path:
            url = f'{self.base_url}/doc/saveas'
            return midas_util.post(url, headers=self.headers, json={'Argument': file_path})
        else :
            url = f'{self.base_url}/doc/save'
            return midas_util.post(url, headers=self.headers)

    @classmethod
    def doc_anal(cls, AnalysisType: AnalysisType = AnalysisType.ANALYSIS):
        """
        Request the analysis of the current document

        Args:
            AnalysisType: The type of the analysis (Analysis or Pushover)

        Returns:
            dict: The result of the analysis of the current document
            e.g. doc_anal() -> {'message': 'MIDAS CIVIL NX command complete'}
        """
        url = f'{cls.base_url}/doc/anal'
        json_body = {}
        if AnalysisType == cls.AnalysisType.PUSHOVER:
            json_body = {'Argument': {'TYPE': AnalysisType.value}}

        return midas_util.post(url, headers=cls.headers, json=json_body)

    # db #############################################################################################################
    @classmethod
    def db_create(cls, item_name: str, items: dict) -> dict:
        """
        Create the items to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            items: The items of the current document's collection with the name

        Returns:
            dict: created result of the current document's collection with the name
            e.g. db_create("NODE", {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}) -> {'NODE': {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_create("ELEM", {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}) -> {'ELEM': {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """
        url = f'{cls.base_url}/db/{item_name}'
        return midas_util.post(url, headers=cls.headers, json={'Assign': items})

    @classmethod
    def db_create_item(cls, item_name: str, item_id: int, item: dict) -> dict:
        """
        Create the item to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection
            item: The item of the current document's collection with the name and id

        Returns:
            dict: created result of the current document's collection with the name and id
            e.g. db_create_item("NODE", 1, {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }) -> {'NODE': {'1': {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_create_item("ELEM", 1, {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}) -> {'ELEM': {'1': {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """

        url = f'{cls.base_url}/db/{item_name}/{item_id}'
        return midas_util.post(url, headers=cls.headers, json={'Assign': item})

    @classmethod
    def db_read(cls, item_name: str) -> dict:
        """
        Requst(using api) All items from the specified name collection
        !!! don't use this function in the loop, it's too slow !!!

        Args:
            item_name: The collection name of the current document (NODE, ELEM, MATL, SECT, etc.)

        Returns:
            dict: The items of the current document's collection with the name
            e.g. db_read("NODE") -> {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}
            e.g. db_read("ELEM") -> {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """
        url = f'{cls.base_url}/db/{item_name}'
        responseJson = midas_util.get(url, headers=cls.headers)
        # check response.json()[item_name] is Exist
        if item_name not in responseJson:
            print(f"Error: Unable to find the registry key or value for {item_name}")
            return None
            # return midas_util.ERROR_DICT(message=f"Unable to find the registry key or value for {item_name}")
        keyVals = responseJson[item_name]
        return {int(k): v for k, v in keyVals.items()}

    @classmethod
    def db_read_item(cls, item_name: str, item_id: int) -> dict:
        """
        Requst(using api) the item from the current document
        !!! don't use this function in the loop, it's too slow !!!

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection

        Returns:
            dict: The item of the current document's collection with the name and id
            e.g. db_read_item("NODE", 1) -> {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }
            e.g. db_read_item("ELEM", 1) -> {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}
            e.g. db_read_item("MATL", 1) -> {'MATL': {'1': {'TYPE': 'CONC', 'NAME': 'C24', 'HE_SPEC': 0, 'HE_COND': 0, 'PLMT': 0, 'P_NAME': '', 'bMASS_DENS': False, 'DAMP_RAT': 0.05, 'PARAM': [{'P_TYPE': 1, 'STANDARD': 'KS01-Civil(RC)', 'CODE': 'KCI-2007', 'DB': 'C24', 'bELAST': False, 'ELAST': 26964000}]}}}
        """
        item_id_str = str(item_id)
        url = f'{cls.base_url}/db/{item_name}/{item_id_str}'
        responseJson = midas_util.get(url, headers=cls.headers)
        # check response.json()[item_name] is Exist
        if item_name not in responseJson:
            print(f"Error: Unable to find the registry key or value for {item_name}")
            return None
            # return midas_util.ERROR_DICT(message=f"Unable to find the registry key or value for {item_name}")
        if item_id_str not in responseJson[item_name]:
            print(
                f"Error: Unable to find the registry key or value for {item_id}")
            return None
            # return midas_util.ERROR_DICT(message=f"Unable to find the registry key or value for {item_id}")
        return responseJson[item_name][item_id_str]

    @classmethod
    def db_update(cls, item_name: str, items: dict) -> dict:
        """
        Update the items to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            items: The items of the current document's collection with the name

        Returns:
            dict: updated result of the current document's collection with the name
            e.g. db_update("NODE", {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}) -> {'NODE': {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_update("ELEM", {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}) -> {'ELEM': {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """

        url = f'{cls.base_url}/db/{item_name}'
        return midas_util.put(url, headers=cls.headers, json={'Assign': items})

    @classmethod
    def db_update_item(cls, item_name: str, item_id: int, item: dict) -> dict:
        """
        Update the item to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection
            item: The item of the current document's collection with the name and id

        Returns:
            dict: updated result of the current document's collection with the name and id
            e.g. db_update_item("NODE", 1, {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }) -> {'NODE': {'1': {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_update_item("ELEM", 1, {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}) -> {'ELEM': {'1': {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """

        url = f'{cls.base_url}/db/{item_name}/{item_id}'
        return midas_util.put(url, headers=cls.headers, json={'Assign': item})

    @classmethod
    def db_delete(cls, item_name: str, item_id: int) -> dict:
        """
        Delete the item from the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection

        Returns:
            dict: deleted result of the current document's collection with the name and id
            e.g. db_delete("NODE", 1) -> {'NODE': {'1': {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_delete("ELEM", 1) -> {'ELEM': {'1': {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """
        url = f'{cls.base_url}/db/{item_name}/{item_id}'
        return midas_util.delete(url, headers=cls.headers)

    @classmethod
    def db_get_next_id(cls, item_name: str) -> int:
        """
        Get the next ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)

        Returns:
            int: The next ID
        """

        res_all = cls.db_read(item_name)
        if not res_all:
            return 1
        next_id = max(map(int, res_all.keys()))
        return next_id + 1

    @classmethod
    def db_get_max_id(cls, item_name: str) -> int:
        """
        Get the max ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
        """

        res_all = cls.db_read(item_name)
        if not res_all:
            return 0
        return max(map(int, res_all.keys()))

    @classmethod
    def db_get_min_id(cls, item_name: str) -> int:
        """
        Get the min ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
        """

        res_all = cls.db_read(item_name)
        if not res_all:
            return 1
        return min(map(int, res_all.keys()))

    @dataclass
    class Unit:
        """
        The unit of the result table
        """

        FORCE: str  # KGF, TONF, N, KN, LBF, KIPS
        DIST: str  # MM, CM, M, IN, FT

    @dataclass
    class ResultTableStyles:
        """
        The styles of the result table
        """
        FORMAT: str  # Default, Fixed, Scientific, General
        PLACE : int  # 0~15

    @dataclass
    class NodeElemsKeys:
        # Style 1: Directly specifying KEY values
        KEYS: List[int]  # Example: KEYS=[1, 2, 3]

    @dataclass
    class NodeElemsTo:
        # Style 2: Specifying KEY values using "to" delimiter
        TO: str  # Example: TO="1 to 3"

    @dataclass
    class NodeElemsStructureGroupName:
        # Style 3: Specifying KEY values using Structure Group Name
        STRUCTURE_GROUP_NAME: str  # Example: STRUCTURE_GROUP_NAME="S1"

    # NodeElems can be one of the three styles above
    NodeElems = Union[NodeElemsKeys, NodeElemsTo, NodeElemsStructureGroupName]

    class TableType(Enum):
        REACTIONG = "Reaction(Global)"
        REACTIONL = "Reaction(Local)"
        REACTIONLSURFACESPRING = "Reaction(Local-Surface Spring)"
        DISPLACEMENTG = "Displacements(Global)"
        DISPLACEMENTL = "Displacements(Local)"
        BEAMFORCE = "Beam Force"
        BEAMFORCESTP = "Beam Forces (Static Prestress)"
        BEAMSTRESS = "Beam Stress"
        BEAMSTRESSDETAIL = "Beam Stress(Equivalent)"
        BEAMSTRESSPSC = "Beam Stress(PSC)"
        BEAMSTRESS7DOF = "Beam Stress(7th DOF)"
        BEAMSTRESS7DOFPSC = "Beam Stress(7th DOF)(PSC)"
        TRUSSFORCE = "Truss Force"
        TRUSSSTRESS = "Truss Stress"
        PLATEFORCEL = "Plate Force (Local)"
        PLATEFORCEG = "Plate Force (Global)"
        PLATEFORCEUL = "Plate Force (UL:Local)"
        PLATEFORCEUG = "Plate Force (UL:UCS)"
        PLATEFORCEWA = "Plate Force (UL:W - A Moment)"
        PLATESTRESSL = "Plate Stress (Local)"
        PLATESTRESSG = "Plate Stress (Global)"
        PLATESTRAINTL = "Plate Total Stress (Local)"
        PLATESTRAINPL = "Plate Plastic Stress (Local)"
        PLATESTRAINTG = "Plate Total Stress (Global)"
        PLATESTRAINPG = "Plate Plastic Stress (Global)"
        PLANESTRESSFL = "Plane Force (Local)"
        PLANESTRESSFG = "Plane Force (Global)"
        PLANESTRESSSL = "Plane Stress (Local)"
        PLANESTRESSSG = "Plane Stress (Global)"
        PLANESTRAINFL = "Plate Force (Local)"
        PLANESTRAINFG = "Plate Force (Global)"
        PLANESTRAINSL = "Plane Stress (Local)"
        PLANESTRAINSG = "Plane Stress (Global)"
        AXISYMMETRICFL = "Axisymmetric Force(Local)"
        AXISYMMETRICFG = "Axisymmetric Force(Global)"
        AXISYMMETRICSL = "Axisymmetric Stress(Local)"
        AXISYMMETRICSG = "Axisymmetric Stress(Global)"
        SOLIDFL = "Solid Force(Local)"
        SOLIDFG = "Solid Force(Global)"
        SOLIDSL = "Solid Stress(Local)"
        SOLIDSG = "Solid Stress(Global)"
        ELASTICLINK = "Elastic Link"
        CABLEFORCE = "Cable Force"
        CABLECONFIG = "Cable Configuration"
        CABLEEFFICIENCY = "Cable Efficiency"

    class TableQuery(Enum):
        MIN = "min"
        MAX = "max"
        ABSMAX = "absmax"

    @classmethod
    def build_payload(cls, table_type: TableType, unit: Optional[Unit], styles: Optional[ResultTableStyles], components: Optional[list], node_elems: Optional[NodeElems], load_case_names: Optional[list], query_component: Optional[str] = None, query_type: Optional[TableQuery] = None) -> dict:
        payload = {
            "TABLE_NAME": 'temp_table_name',
            "TABLE_TYPE": table_type.name
        }

        query = ''
        if query_component and query_type:
            query = f"{query_type.value}({query_component})"

        if unit:
            payload["UNIT"] = unit
        if styles:
            payload["STYLES"] = styles
        if components:
            payload["COMPONENTS"] = components
        if node_elems:
            payload["NODE_ELEMS"] = node_elems
        if load_case_names:
            payload["LOAD_CASE_NAMES"] = load_case_names

        return payload, query

    @classmethod
    def _post_table(cls, payload: dict, query: str) -> dict:
        url = f'{MidasAPI.base_url}/post/table'
        if query:
            url += f'?{query}'

        response_json = midas_util.post(url, headers=MidasAPI.headers, json={'Argument': payload})
        return response_json['temp_table_name']

    @classmethod
    def get_result_table(cls, table_type: TableType, unit: Optional[Unit] = None, styles: Optional[ResultTableStyles] = None, components: Optional[list] = None, node_elems: Optional[NodeElems] = None, load_case_names: Optional[list] = None) -> dict:
        """
        Get the result table of the current document

        Args:
            table_type: The table type of the current document
            unit: The unit of the table
            styles: The styles of the table
            components: The components of the table
            node_elems: The node elements of the table
            load_case_names: The load case names of the table

        Returns:
            dict: The result table of the current document
            e.g. get_result_table("DISPLACEMENTG") -> {'FORCE': 'kN', 'DIST': 'm', 'HEAD': ['Index', 'Node', 'Load', 'DX', 'DY', 'DZ', 'RX', 'RY', 'RZ'], 'DATA': [['1', '1', '자중', '0.000000', '-0.000015', '-0.000262', '0.000006', '0.000000', '0.000000']}
        """
        payload, query = cls.build_payload(table_type, unit, styles, components, node_elems, load_case_names)
        return cls._post_table(payload, query)

    @classmethod
    def get_result_table_query_component(cls, table_type: TableType, query_component: str = None, query_type: TableQuery = None, unit: Optional[Unit] = None, styles: Optional[ResultTableStyles] = None, components: Optional[list] = None, node_elems: Optional[NodeElems] = None, load_case_names: Optional[list] = None) -> dict:
        """
        Get the TableQuery value of the result table of the current document

        Args:
            table_type: The table type of the current document
            unit: The unit of the table
            styles: The styles of the table
            components: The components of the table
            node_elems: The node elements of the table
            load_case_names: The load case names of the table

        Returns:
            dict: The max value of the result table of the current document
            e.g. get_result_table_max("DISPLACEMENTG", 'DX') -> {'FORCE': 'kN', 'DIST': 'm', 'HEAD': ['Index', 'Node', 'Load', 'DX', 'DY', 'DZ', 'RX', 'RY', 'RZ'], 'DATA': [['1', '1', '자중', '0.000000', '-0.000015', '-0.000262', '0.000006', '0.000000', '0.000000']}
        """
        payload, query = cls.build_payload(table_type, unit, styles, components, node_elems, load_case_names, query_component, query_type)
        return cls._post_table(payload, query)

    @classmethod
    def get_result_table_query_components(cls, table_type: str, components: list, query_type: TableQuery , selectedIds: list = None) -> dict:
        """
        Get the MIN/MAX/ABSMAX displacement of the selected nodes

        Args:
            table_type: The table type of the current document
            query_type: The query type of the table
                MIN: Get the min value
                MAX: Get the max value
                ABSMAX: Get the max absolute value
            components: The components of the table
            node_elems: The node elements of the table

        Returns:
            dict: The max displacement of the selected nodes
            e.g. get_max_displacement_selected_nodes() -> {'HEAD': ['Index', 'Node', 'Load', 'DX', 'DY', 'DZ', 'RX', 'RY', 'RZ'], 'DATA': [['1', '1', '자중', '0.000000', '-0.000015', '-0.000262', '0.000006', '0.000000', '0.000000'], ['2', '2', '자 중', '0.000000', '-0.000014', '-0.000257', '0.000006', '0.000000', '0.000000'], ['3', '3', '자중', '0.000000', '-0.000010', '-0.000244', '0.000003', '0.000000', '0.000000']}"""

        result_talbe_all = {'HEAD': [], 'DATA': []}
        for index, component in enumerate(components):
            results_table = cls.get_result_table_query_component(table_type, component, query_type, node_elems={'KEYS' : selectedIds})
            if 'error' in results_table:
                return {'error': results_table['error']}
            results_table['DATA'][0].extend([component])

            if index == 0:
                result_talbe_all = results_table
                result_talbe_all['HEAD'].extend([query_type.value])
            else:
                result_talbe_all['DATA'].extend(results_table['DATA'])
        return result_talbe_all

    # view ############################################################################################################
    @classmethod
    def view_select_get(cls) -> dict:
        """
        Get the selected NODE/ELEM of the current document view

        Returns:
            dict: The selected NODE/ELEM of the current view
            e.g. view_select_get() -> {'NODE_LIST': [1, 2], 'ELEM_LIST': [1]}
        """
        url = f'{cls.base_url}/view/select'
        responseJson = midas_util.get(url, headers=cls.headers)
        if 'error' in responseJson:
            return responseJson
        else:
            return responseJson['SELECT']
        
    # operation ########################################################################################################
    @classmethod
    def ope_section_coord(cls, section_id: int, position: float) -> dict:
        """
        Request the section coordinate

        Args:
            section_id: The section ID
            position: The position of the section

        Returns:
            dict: The result of the section coordinate
            e.g. ope_section_coord(1, 0.5) -> {'message': 'MIDAS CIVIL NX command complete'}
        """
        url = f'{cls.base_url}/ope/sectcord'
        return midas_util.post(url, headers=cls.headers, json={'Argument': {'SECT': section_id, 'POS': position}})
    
    @classmethod
    def ope_elem_tendon(cls, elem_id: int, position: float) -> dict:
        """
        Request the element tendon

        Args:
            elem_id: The element ID

        Returns:
            dict: The result of the element tendon
            e.g. ope_elem_tendon(1) -> {'message': 'MIDAS CIVIL NX command complete'}
        """
        url = f'{cls.base_url}/ope/elemtdnt'
        return midas_util.post(url, headers=cls.headers, json={'Argument': {'ELEM': elem_id, 'POS': position}})

    # Steel Code Check (Gen Only) ########################################################################################################
    @classmethod
    def post_steelcodecheck(cls):
        """
        Request the steel code check

        Returns:
            dict: The result of the steel code check
            e.g. post_steelcodecheck() -> {'message': 'MIDAS CIVIL NX command complete'}, TODO: check the result
        """
        url = f'{cls.base_url}/post/steelcodecheck'
        return midas_util.post(url, headers=cls.headers, json={})

    # static function ##########################################################################################################
    @staticmethod
    def select_by_subkey(value, dict, *subkey):
        ret = []
        if (len(subkey) == 1):
            ret = [key for key in dict.keys() if dict[key][subkey[0]] == value]
        if (len(subkey) == 2):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]] == value]
        if (len(subkey) == 3):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]][subkey[2]] == value]
        if (len(subkey) == 4):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]][subkey[2]][subkey[3]] == value]
        if (len(subkey) == 5):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]][subkey[2]][subkey[3]][subkey[4]] == value]

        if (len(subkey) > 5):
            print("Error: Please check the subkey length")
            # return None
            return midas_util.ERROR_DICT(message="Please check the subkey length")
        if (len(ret) == 0):
            print("Error: Please check the subkey value")
            # return None
            return midas_util.ERROR_DICT(message="Please check the subkey value")
        return ret[0]

    @staticmethod
    def get_subitem_next_id(subitem_list: dict) -> int:
        """
        Get the next ID of the subitem list

        Args:
            subitem_list (dict): The subitem list

        Returns:
            int: The next ID
        """

        if 'ITEMS' not in subitem_list:
            return 1
        return max(map(lambda x: x['ID'], subitem_list['ITEMS'])) + 1
