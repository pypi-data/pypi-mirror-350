# import pathlib
# import importlib
# import inspect
# import json

# from rod.schema_generator import SchemaInterface


# # 1. select the file to function-knowledge
# pwd = pathlib.Path(__file__).parent.absolute()
# target_file_name = "wgsd_flow.py"

# # 2. extract the function code and schema from the file
# def derive_module_name(file_name):
#     return file_name.split(".")[0]

# target_moduel_name = derive_module_name(target_file_name)
# target_module = importlib.import_module(target_moduel_name)

# def get_functions_from_moduel(module):
#     functions = []
#     for name, obj in inspect.getmembers(module):
#         if inspect.isfunction(obj):
#             # filter out functions that are imported from other modules
#             if obj.__module__ == module.__name__:
#                 functions.append(obj)
#     return functions

# target_functions = get_functions_from_moduel(target_module)

# codes = []
# schemas = []

# for function in target_functions:
#     schema = SchemaInterface(function)
#     schemas.append(schema)
#     codes.append(inspect.getsource(function))
#     # pretty_json = json.dumps(inspect.getsource(function), indent=2)
#     # print(pretty_json)

# # write the schema to a json file
# # schema_json = [schema.to_dict() for schema in schemas]
# schema_json_file = pwd / "wgsd_schema.json"
# with open(schema_json_file, "w") as f:
#     json.dump(schemas, f, indent=2)
    