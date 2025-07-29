from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum
from pyscript import document as document

ENV: str
g_base_url: Incomplete
g_headers: Incomplete

class MidasAPI:
    base_url = g_base_url
    headers = g_headers
    class AnalysisType(Enum):
        ANALYSIS: str
        PUSHOVER: str
    @dataclass
    class tableFormat:
        '''
        Standard table format for the MIDAS API
        {
            "HEAD": ["Strain", "Stress"],
            "DATA": [[0.1, 2, 4, 4, 35], [0, 234235, 235, 235, 0]],
        }
        '''
        HEAD: list[str, 2]
        DATA: list[list[float, 2]]
    @classmethod
    def create_instance(cls, product, country: str = 'KR'): ...
    @classmethod
    def doc_open(cls, file_path): ...
    @classmethod
    def doc_anal(cls, AnalysisType: AnalysisType = ...):
        """
        Request the analysis of the current document

        Args:
            AnalysisType (AnalysisType): The type of the analysis (Analysis or Pushover)

        Returns:
            dict: The result of the analysis of the current document
            e.g. doc_anal() -> {'message': 'MIDAS CIVIL NX command complete'}
        """
    @classmethod
    def db_create(cls, item_name: str, items: dict) -> dict:
        '''
        Create the items to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            items: The items of the current document\'s collection with the name

        Returns:
            dict: created result of the current document\'s collection with the name
            e.g. db_create("NODE", {1: {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}) -> {\'NODE\': {1: {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}}
            e.g. db_create("ELEM", {1: {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}) -> {\'ELEM\': {1: {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}
        '''
    @classmethod
    def db_create_item(cls, item_name: str, item_id: int, item: dict) -> dict:
        '''
        Create the item to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection
            item: The item of the current document\'s collection with the name and id

        Returns:
            dict: created result of the current document\'s collection with the name and id
            e.g. db_create_item("NODE", 1, {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }) -> {\'NODE\': {\'1\': {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}}
            e.g. db_create_item("ELEM", 1, {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}) -> {\'ELEM\': {\'1\': {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}
        '''
    @classmethod
    def db_read(cls, item_name: str) -> dict:
        '''
        Requst(using api) All items from the specified name collection
        !!! don\'t use this function in the loop, it\'s too slow !!!

        Args:
            item_name: The collection name of the current document (NODE, ELEM, MATL, SECT, etc.)

        Returns:
            dict: The items of the current document\'s collection with the name
            e.g. db_read("NODE") -> {1: {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}
            e.g. db_read("ELEM") -> {1: {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}
        '''
    @classmethod
    def db_read_item(cls, item_name: str, item_id: int) -> dict:
        '''
        Requst(using api) the item from the current document
        !!! don\'t use this function in the loop, it\'s too slow !!!

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection

        Returns:
            dict: The item of the current document\'s collection with the name and id
            e.g. db_read_item("NODE", 1) -> {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }
            e.g. db_read_item("ELEM", 1) -> {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}
            e.g. db_read_item("MATL", 1) -> {\'MATL\': {\'1\': {\'TYPE\': \'CONC\', \'NAME\': \'C24\', \'HE_SPEC\': 0, \'HE_COND\': 0, \'PLMT\': 0, \'P_NAME\': \'\', \'bMASS_DENS\': False, \'DAMP_RAT\': 0.05, \'PARAM\': [{\'P_TYPE\': 1, \'STANDARD\': \'KS01-Civil(RC)\', \'CODE\': \'KCI-2007\', \'DB\': \'C24\', \'bELAST\': False, \'ELAST\': 26964000}]}}}
            
        '''
    @classmethod
    def db_update(cls, item_name: str, items: dict) -> dict:
        '''
        Update the items to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            items: The items of the current document\'s collection with the name

        Returns:
            dict: updated result of the current document\'s collection with the name
            e.g. db_update("NODE", {1: {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}) -> {\'NODE\': {1: {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}}
            e.g. db_update("ELEM", {1: {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}) -> {\'ELEM\': {1: {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}
        '''
    @classmethod
    def db_update_item(cls, item_name: str, item_id: int, item: dict) -> dict:
        '''
        Update the item to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection
            item: The item of the current document\'s collection with the name and id

        Returns:
            dict: updated result of the current document\'s collection with the name and id
            e.g. db_update_item("NODE", 1, {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }) -> {\'NODE\': {\'1\': {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}}
            e.g. db_update_item("ELEM", 1, {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}) -> {\'ELEM\': {\'1\': {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}
        '''
    @classmethod
    def db_delete(cls, item_name: str, item_id: int) -> dict:
        '''
        Delete the item from the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection

        Returns:
            dict: deleted result of the current document\'s collection with the name and id
            e.g. db_delete("NODE", 1) -> {\'NODE\': {\'1\': {\'X\': 0.0, \'Y\': 0.0, \'Z\': 0.0 }}}
            e.g. db_delete("ELEM", 1) -> {\'ELEM\': {\'1\': {\'TYPE\': \'BEAM\', \'MATL\': 1, \'SECT\': 1, \'NODE\': [1, 2, 0, 0, 0, 0, 0, 0], \'ANGLE\': 0, \'STYPE\': 0}}
        '''
    @classmethod
    def db_get_next_id(cls, item_name: str) -> int:
        """
        Get the next ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)

        Returns:
            int: The next ID
        """
    @classmethod
    def db_get_max_id(cls, item_name: str) -> int:
        """
        Get the max ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
        """
    @classmethod
    def db_get_min_id(cls, item_name: str) -> int:
        """
        Get the min ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
        """
    @classmethod
    def view_select_get(cls) -> dict:
        """
        Get the selected NODE/ELEM of the current document view

        Returns:
            dict: The selected NODE/ELEM of the current view
            e.g. view_select_get() -> {'NODE_LIST': [1, 2], 'ELEM_LIST': [1]}        
        """
    @classmethod
    def post_steelcodecheck(cls):
        """
        Request the steel code check

        Returns:
            dict: The result of the steel code check
            e.g. post_steelcodecheck() -> {'message': 'MIDAS CIVIL NX command complete'}, TODO: check the result
        """
    @staticmethod
    def select_by_subkey(value, dict, *subkey): ...
    @staticmethod
    def get_subitem_next_id(subitem_list: dict) -> int:
        """
        Get the next ID of the subitem list

        Args:
            subitem_list (dict): The subitem list

        Returns:
            int: The next ID
        """
