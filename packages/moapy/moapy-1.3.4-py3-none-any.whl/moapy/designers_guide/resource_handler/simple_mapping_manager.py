from moapy.designers_guide.resource_handler.content_component import Component
from moapy.designers_guide.resource import components

__NOT_DEFINED_ID__ = "not_defined"

__symbol_mappings = {}
__simple_to_comp_id = {}
__temp_symbol_mappings = {} # TODO : resource&mapping data 관리 구조 구축 후 삭제 필요
__temp_simple_to_comp_id = {} # TODO : resource&mapping data 관리 구조 구축 후 삭제 필요
__temp_symbol_idx = 0

# Func Desc. Make simple symbols and map
__INITIAL_SYMBOL_MAPPINGS = {
    ("\\mathit{NA}", "G0_COMP_ESCAPE"): "I_1",
}

def generate_mapping_data(
    comp_list: list[Component] | None = None
):
    global __temp_symbol_idx
    global __symbol_mappings
    global __simple_to_comp_id
    global __temp_symbol_mappings
    global __temp_simple_to_comp_id

    __temp_symbol_idx = 0

    inner_server = False
    if comp_list is None:
        inner_server = True
        __symbol_mappings = {}
        __simple_to_comp_id = {}
        comp_list = components
    else:
        __temp_symbol_mappings = {}
        __temp_simple_to_comp_id = {}
    for i, item in enumerate(comp_list):
        simple_symbol = f'S_{{{i + 1}}}'
        if inner_server:
            __symbol_mappings[(item['latexSymbol'], item['id'])] = simple_symbol
            __simple_to_comp_id[simple_symbol] = item['id']
        else:
            __temp_symbol_mappings[(item['latexSymbol'], item['id'])] = simple_symbol
            __temp_simple_to_comp_id[simple_symbol] = item['id']
    if inner_server:
        __symbol_mappings = {**__INITIAL_SYMBOL_MAPPINGS, **__symbol_mappings}
        __symbol_mappings = {k: v for k, v in sorted(__symbol_mappings.items(), key=lambda item: len(item[0][0]), reverse=True)}
    else:
        __temp_symbol_mappings = {**__INITIAL_SYMBOL_MAPPINGS, **__temp_symbol_mappings}
        __temp_symbol_mappings = {k: v for k, v in sorted(__temp_symbol_mappings.items(), key=lambda item: len(item[0][0]), reverse=True)}

def append_mapping_data_only_symbol(symbols:list[str]):
    global __temp_symbol_idx
    global __temp_symbol_mappings
    global __temp_simple_to_comp_id

    for i, sym in enumerate(symbols):
        if (sym, __NOT_DEFINED_ID__) in __temp_symbol_mappings:
            continue
        __temp_symbol_idx += 1
        simple_symbol = f'T_{{{__temp_symbol_idx}}}'
        __temp_symbol_mappings[(sym, __NOT_DEFINED_ID__)] = simple_symbol
        __temp_simple_to_comp_id[simple_symbol] = __NOT_DEFINED_ID__

    __temp_symbol_mappings = {**__INITIAL_SYMBOL_MAPPINGS, **__temp_symbol_mappings}
    __temp_symbol_mappings = {k: v for k, v in sorted(__temp_symbol_mappings.items(), key=lambda item: len(item[0][0]), reverse=True)}

def get_symbol_mappings():
    global __symbol_mappings
    global __temp_symbol_mappings
    if __temp_symbol_mappings is not None and __temp_symbol_mappings != {}:
        return __temp_symbol_mappings
    elif __symbol_mappings == {}:
        generate_mapping_data() 
    return __symbol_mappings

def get_simple_symbol_to_component_id():
    global __simple_to_comp_id
    global __temp_simple_to_comp_id
    if __temp_simple_to_comp_id is not None and __temp_simple_to_comp_id != {}:
        return __temp_simple_to_comp_id
    elif __simple_to_comp_id == {}:
        generate_mapping_data()
    return __simple_to_comp_id

def reset_temp_mapping_data():
    global __temp_symbol_mappings
    global __temp_simple_to_comp_id
    __temp_symbol_mappings = None
    __temp_simple_to_comp_id = None