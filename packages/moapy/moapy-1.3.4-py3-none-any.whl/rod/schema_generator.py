from typing import Dict, Union, Any, Type, Callable, get_type_hints
from dataclasses import is_dataclass, fields
from pydantic import BaseModel
import inspect

# # 데이터 클래스 예시
# @dataclass
# class Person:
#     """
#     Person details.
#     """
#     name: str = Field(default="", metadata={"description": "The person's full name."})
#     age: int = Field(default=0, metadata={"description": "The person's age."})
#     email: str = Field(default='', metadata={"description": "The person's email address."})  # 기본값 설정

# # Pydantic 모델 예시
# class Contact(BaseModel):
#     """
#     Contact details.
#     """
#     phone: str = Field(default="", description="The contact's phone number.")
#     address: str = Field(default='', description="The contact's address.")


# def my_function(person: Person, contacts: List[Contact], settings: Dict[str,  Union[int, str]] = {}) -> bool:
#     """
#     Processes person and their contacts with given settings.
    
#     Args:
#         person: The person details.
#         contacts: List of contact details.
#         settings: Miscellaneous settings.
    
#     Returns:
#         bool: True if successful, False otherwise.
#     """
#     return True

def python_type_to_json_type(python_type: Type) -> str:
    """
    Converts Python types to JSON Schema compatible type names.
    """
    if python_type in {str, 'str'}:
        return 'string'
    elif python_type in {int, 'int'}:
        return 'integer'
    elif python_type in {bool, 'bool'}:
        return 'boolean'
    elif python_type in {float, 'float'}:
        return 'number'
    elif python_type in {list, 'list'}:
        return 'array'
    return 'object'  # Default to object for custom classes or unknown types


def create_schema_for_class(cls: Type) -> Dict[str, Any]:
    if is_dataclass(cls):
        return {
            'type': 'object',
            'properties': {
                field.name: {
                    'type': python_type_to_json_type(field.type),
                    'default' : field.default,
                    'description': field.metadata.get('description', 'No description provided')
                } for field in fields(cls)
            }
        }
    elif issubclass(cls, BaseModel):
        return {
            'type': 'object',
            'properties': {
                field_name: {
                    'type':  python_type_to_json_type(field_type),
                    'default' : field_type.default,
                    'description': cls.model_fields[field_name].description
                } for field_name, field_type in cls.__annotations__.items()
            }
        }
    return {}

def create_schema_from_function(fn) -> Dict[str, Any]:
    annotations = get_type_hints(fn)
    docstring = inspect.getdoc(fn)
    summary = ''
    if docstring is not None:
        summary, *description = docstring.split('\n\n', 1)
        params_desc = {}

        if description:
            for line in description[0].split('\n'):
                if ':' in line:
                    param, desc = line.split(':', 1)
                    params_desc[param.strip()] = desc.strip()

    classPath = fn.__module__ + "." + fn.__qualname__
    schema = {
        'path': classPath,
        'name': fn.__name__,
        'description': summary,
        'parameters': {}
    }

    properties = {}

    for param, param_type in annotations.items():
        if param == 'return':
            continue
        origin = getattr(param_type, '__origin__', None)

        type_str = "object"
        if origin is None:
            type_str = python_type_to_json_type(param_type)
        else:
            type_str = python_type_to_json_type(origin)

        param_details = {
            'type': type_str,
            'description': params_desc.get(param, 'No description provided')
        }

        if origin is list:  # List 처리
            item_type = param_type.__args__[0]
            if is_dataclass(item_type) or issubclass(item_type, BaseModel):
                param_details['items'] = create_schema_for_class(item_type)
            else:
                param_details['items'] = {'type': python_type_to_json_type(item_type) }
        elif origin is dict:  # Dict 처리
            key_type, value_type = param_type.__args__
            # value_type 이 Union인 경우 처리
            if getattr(value_type, '__origin__', None) is Union:
                param_details['additionalProperties'] = { 'anyOf': [python_type_to_json_type(t) for t in value_type.__args__] }
            else:
                param_details['additionalProperties'] = {'type': python_type_to_json_type(value_type) }
        elif is_dataclass(param_type) or issubclass(param_type, BaseModel):
            param_details.update(create_schema_for_class(param_type))

        properties[param] = param_details

    # if properties has sumitem, add it to schema
    if properties:
        schema['parameters'] = {
            'type': 'object',
            'properties': properties,
            'required': [param for param in annotations if param != 'return']  # all parameters except the return type
        }
    return schema


# # Generate and print the schema
# function_schema = create_schema_from_function(my_function)
# print(function_schema)

def SchemaInterface(func: Callable[..., Any]) -> str:
    """
    Return the schema of the function.

    Args:
        func: The function to wrap.

    Returns:
        None: The function does not return anything.
    """

    schema = create_schema_from_function(func)
    # schema = add_descriptions_to_schema(schema, func)
    # res = function_calling.convert_to_openai_tool(func)["function"]
    # res = function_calling.convert_to_openai_function(func)
    # res = FunctionWrapper(func).schema

    return schema
