from copy import deepcopy
from typing import Optional

from moapy.designers_guide.resource_handler.content_component import (
    Component,
    Content,
    DataTable,
)
from moapy.designers_guide.resource.content_component import (
    SERVER_URL,
    binary_operators,
    relation_operators,
    function_operators,
)


class DictContentComponentManager:
    def __init__(self):
        self._component: dict[str, Component] = {}
        self._content: dict[str, Content] = {}

    def _add_content(self, content: Content) -> None:
        if not content["id"]:
            raise ValueError("Content id is required")
        if content["id"] in self._content:
            raise ValueError(f"Content with id {content['id']} already exists")
        self._content[content["id"]] = deepcopy(content)

    def add_content(self, content: Content | list[Content]) -> None:
        for cont in content:
            self._add_content(cont)

    def _add_component(self, component: Component) -> None:
        if not component["id"]:
            raise ValueError("Component id is required")
        if component["id"] in self._component:
            raise ValueError(f"Component with id {component['id']} already exists")
        self._component[component["id"]] = deepcopy(component)

    def add_component(self, component: Component | list[Component]) -> None:
        for comp in component:
            self._add_component(comp)

    def copy(self) -> 'DictContentComponentManager':
        return deepcopy(self)
      
    @property
    def component_list(self) -> list[Component]:
        return deepcopy(list(self._component.values()))

    @property
    def content_list(self) -> list[Content]:
        return deepcopy(list(self._content.values()))

    def find_component_by_id(self, id: str) -> Optional[Component]:
        return self._component.get(id, None)

    def find_content_by_id(self, id: str) -> Optional[Content]:
        return self._content.get(id, None)

    def update_component(self, id: str, component: Component) -> None:
        if id not in self._component:
            raise ValueError(f"Component with id {id} not found")
        self._component[id] = component

    def find_by_latex_symbol(self, target_latex_symbol: str) -> Optional[Component]:
        for comp in self._component.values():
            if comp["latexSymbol"] == target_latex_symbol:
                return comp
        return None

    def find_comp(
        self, latexSymbol: str, code_name: str, reference: str
    ) -> Optional[Component]:
        for comp in self._component.values():
            if (
                comp["latexSymbol"] == latexSymbol
                and comp["codeName"] == code_name
                and comp["reference"] == reference
            ):
                return comp
        return None

    def get_table_type(self, comp: Component) -> str:
        if "table" in comp:
            return comp["table"]
        elif "compType" in comp:
            component_type = comp["compType"]
            if component_type.startswith("table(") and component_type.endswith(")"):
                table_type = component_type[6:-1]
                if table_type == "formula":
                    if "abstractedSymbols" in comp:
                        abstracted = comp["abstractedSymbols"]
                        abstracted.remove(comp["latexSymbol"])
                        if len(abstracted) == 0:
                            return "text"
                        table_data = self.get_table_data_by_component(comp)
                        if table_data is not None:
                            for row in table_data:
                                if isinstance(row, list):
                                    for col in row:
                                        for symbol in abstracted:
                                            if symbol in col:
                                                return "text"
                                else:
                                    for symbol in abstracted:
                                        if symbol in row:
                                            return "text"
                            return "text"
                    else:
                        return "formula"
                else:
                    return table_type
            else:
                return "None"
        else:
            return "None"

    def get_table_by_component(self, comp: Component) -> Optional[DataTable]:
        if "tableDetail" in comp:
            return comp.get("tableDetail", None)
        return None

    def get_table_enum_by_component(self, comp: Component) -> Optional[list[dict]]:
        table = self.get_table_data_by_component(comp)
        if table is None:
            return None
        if "label" in table[0]:
            enum_table = []
            for row, row_data in enumerate(table):
                if row == 0:
                    continue
                enum_table.append(row_data[0])
            return enum_table
        return None

    def get_table_criteria_by_component(self, comp: Component) -> Optional[list[dict]]:
        table = self.get_table_by_component(comp)
        if table and "criteria" in table:
            return table["criteria"]
        return None

    def get_table_data_by_component(self, comp: Component) -> Optional[list[str]] | Optional[list[list[str]]]:
        table = self.get_table_by_component(comp)
        if table and "data" in table:
            return table["data"]
        return None

    def convert_enum_table_to_detail(
        self, comp: Component
    ) -> Optional[list[list[str]]]:
        table = self.get_table_by_component(comp)
        if table is None or "data" not in table or "point" in table or "criteria" in table:
            return None
        data_table = table["data"]
        if isinstance(data_table[0][0], str) is False or "label" not in data_table[0]:
            return None
        if "description" not in data_table[0] and "Description" not in data_table[0]:
            return None

        detail_table = []
        for row, row_data in enumerate(data_table):
            if row == 0: # header
                haeder = []
                for col, col_data in enumerate(row_data):
                    if col == 0:
                        haeder.append(f"$${comp['latexSymbol']}$$")
                    elif col_data == "description" or col_data == "Description":
                        haeder.append("Description")
                    else:
                        haeder.append(str(col_data))
                detail_table.append(haeder)
            else:
                detail_table.append(row_data)

        return detail_table

    def get_ref_type(self, id) -> str:
        comp = self.find_component_by_id(id)
        if 'refType' in comp:
            return comp['refType']
        
        if 'table' in comp and comp['table'] == 'dropdown':
            return 'string'
        else:
            return 'number'
    
    def get_component_type(self, comp: Component) -> str:
        if 'compType' in comp:
            return comp['compType']
        else:
            if "table" in comp:
                table_type = comp["table"]
                if table_type == "dropdown":
                    return "table(dropdown)"
                elif table_type == "result":
                    return "table(result)"
                elif table_type == 'formula':
                    criteria_list = self.get_table_by_component(comp)["criteria"]
                    if criteria_list is not None:
                        if len(criteria_list) == 1 or (len(criteria_list) == 2 and criteria_list[1][0] == ""):
                            return "table(formula)"
                        else:
                            return "table(matrix)"
                elif table_type == 'text':
                    return "table(text)"
                elif table_type == "interpolation":
                    return "table(interpolation)"
                elif table_type == "bi-interpolation":
                    return "table(bi-interpolation)"
            else:
                if "default" in comp:
                    if "const" in comp and comp["const"] is True:
                        return "number(const)"
                    else:
                        return "number"
                if "latexEquation" in comp:
                    return "formula"
        return None
    
    def get_figure_server_url(self) -> str:
        return SERVER_URL

    @property
    def binary_operators(self) -> list[str]:
        return binary_operators

    @property
    def relation_operators(self) -> list[str]:
        return relation_operators

    @property
    def function_operators(self) -> list[str]:
        return function_operators


def create_dict_content_component_manager(
    *,
    content_list: list[Content],
    component_list: list[Component],
) -> DictContentComponentManager:
    manager = DictContentComponentManager()
    manager.add_content(content_list)
    manager.add_component(component_list)
    return manager
