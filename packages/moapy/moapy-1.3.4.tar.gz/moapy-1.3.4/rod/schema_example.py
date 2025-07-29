import unittest
# from typing import List, Dict, Union, Any, Type, Callable, get_type_hints
# from dataclasses import dataclass, is_dataclass, fields, field as Field
# from pydantic import BaseModel, Field
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
#
#     Args:
#         person: The person details.
#         contacts: List of contact details.
#         settings: Miscellaneous settings.
#
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
                    'description': cls.model_fields[field_name].description
                } for field_name, field_type in cls.__annotations__.items()
            }
        }
    return {}

def create_schema_from_function(fn) -> Dict[str, Any]:
    annotations = get_type_hints(fn)
    docstring = inspect.getdoc(fn)
    summary, *description = docstring.split('\n\n', 1)
    params_desc = {}

    if description:
        for line in description[0].split('\n'):
            if ':' in line:
                param, desc = line.split(':', 1)
                params_desc[param.strip()] = desc.strip()

    schema = {
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

def ExpectedInterface(obj: Any) -> str:
    """
    Return the string of schema expected object.

    Args:
        obj: The object to json string.

    Returns:
        str: The json string of the object.
    """
    return obj

class SchemaExampleWithTests(unittest.TestCase):

    def SchemaAssertEqual(self, obj: Any, func: Callable[..., Any])->None:
        """
        Assert that the schema of the function is equal to the expected object.

        Args:
            func: The function to wrap.
            obj: The expected object.

        Returns:
            None: The function does not return anything.
        """
        expected = ExpectedInterface(obj)
        result = SchemaInterface(func)
        self.assertDictEqual(expected, result)

    def setUp(self):
        """Call before every test case."""
        self.maxDiff = None

    def tearDown(self):
        """Call after every test case."""

    # test case for the function annotation.

    # https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
    # complex 타입 현재 지원 안됨
    def test_builtin_numeric_types(self):
        def builtin_numeric_types(int :int, float :float)->None:
            """
            Return the built-in numeric types.

            Args:
                int: An integer.
                float: A floating point number.

            Returns:
                None: The function does not return anything.
            """
            return

        expect = {
            "name": "builtin_numeric_types",
            "description": "Return the built-in numeric types.",
            "parameters": {
                "type": "object",
                "properties": {
                    "int": {
                        "type": "integer",
                        "description": "An integer."
                    },
                    "float": {
                        "type": "number",
                        "description": "A floating point number."
                    }
                },
                "required": ["int", "float"]
            }
        }

        self.SchemaAssertEqual(expect, builtin_numeric_types)

    # https://docs.python.org/3/library/stdtypes.html#boolean-type-bool
    def test_builtin_boolean_types(self):
        def builtin_boolean_types(bool :bool)->None:
            """
            Return the built-in boolean types.

            Args:
                bool: A boolean.

            Returns:
                None: The function does not return anything.
            """
            return

        expect = {
            "name": "builtin_boolean_types",
            "description": "Return the built-in boolean types.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bool": {
                        "type": "boolean",
                        "description": "A boolean."
                    }
                },
                "required": ["bool"]
            }
        }

        self.SchemaAssertEqual(expect, builtin_boolean_types)

    # https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
    # 다음과 같이 sequence 타입의 실제 타입 없이 사용 안됨
    # def test_builtin_sequence_types(self):

    def test_textsequence_types(self):
        def textsequence_types(str:str)->None:
            """
            Return the text sequence types.

            Args:
                str: A string.

            Returns:
                None: The function does not return anything.
            """
            return

        expect = {
            "name": "textsequence_types",
            "description": "Return the text sequence types.",
            "parameters": {
                "type": "object",
                "properties": {
                    "str": {
                        "type": "string",
                        "description": "A string."
                    }
                },
                "required": ["str"]
            }
        }

        self.SchemaAssertEqual(expect, textsequence_types)

    # https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview
    # bytes, bytearray, memoryview 타입 현재 지원 안됨
    # def test_binarysequence_types(self):

    # https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
    # 다음과 같이 set 타입의 실제 타입 없이 사용 안됨
    # def test_builtin_set_types(self):

    # https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
    # 다음과 같이 dict 타입의 실제 타입 없이 사용 안됨
    # def builtin_mapping_types(dict:dict)->None:

    def test_builtin_sequence_list_with_other_types(self):
        def builtin_sequence_list_with_other_types(list_int: list[int], list_float: list[float], list_bool: list[bool], list_str: list[str])->None:
            """
            Return the built-in sequence list with other types.

            Args:
                list_int: A list of integers.
                list_float: A list of floating point numbers.
                list_bool: A list of booleans.
                list_str: A list of strings.

            Returns:
                None : The function does not return anything.
            """
            return

        expect = {
            "name": "builtin_sequence_list_with_other_types",
            "description": "Return the built-in sequence list with other types.",
            "parameters": {
                "type": "object",
                "properties": {
                    "list_int": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "description": "A list of integers."
                    },
                    "list_float": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "A list of floating point numbers."
                    },
                    "list_bool": {
                        "type": "array",
                        "items": {
                            "type": "boolean"
                        },
                        "description": "A list of booleans."
                    },
                    "list_str": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of strings."
                    }
                },
                "required": ["list_int", "list_float", "list_bool", "list_str"]
            }
        }

        self.SchemaAssertEqual(expect, builtin_sequence_list_with_other_types)

    def test_builtin_sequence_list_with_other_types_fixed_length(self):
        def builtin_sequence_list_with_other_types_fixed_length(list_int :list[int,3], list_float: list[float, 3], list_bool: list[bool, 3], list_str: list[str, 3])->None:
            """
            Return the built-in sequence list with other types.

            Args:
                list_int: A list of integers.
                list_float: A list of floating point numbers.
                list_bool: A list of booleans.
                list_str: A list of strings.

            Returns:
                None : The function does not return anything.
            """
            return

        expect = {
            "name": "builtin_sequence_list_with_other_types_fixed_length",
            "description": "Return the built-in sequence list with other types.",
            "parameters": {
                "type": "object",
                "properties": {
                    "list_int": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        # "minItems": 3,
                        # "maxItems": 3,
                        "description": "A list of integers."
                    },
                    "list_float": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        # "minItems": 3,
                        # "maxItems": 3,
                        "description": "A list of floating point numbers."
                    },
                    "list_bool": {
                        "type": "array",
                        "items": {
                            "type": "boolean"
                        },
                        # "minItems": 3,
                        # "maxItems": 3,
                        "description": "A list of booleans."
                    },
                    "list_str": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        # "minItems": 3,
                        # "maxItems": 3,
                        "description": "A list of strings."
                    }
                },
                "required": ["list_int", "list_float", "list_bool", "list_str"]
            }
        }

        # TODO: fixed length list 지원 안됨
        # python 자체가 fixed length list 개념이 지만, json schema는 이를 지원하므로 방법을 검토
        self.SchemaAssertEqual(expect, builtin_sequence_list_with_other_types_fixed_length)
    # def test_builtin_sequence_tuple_with_other_types(self):
    #     def builtin_sequence_tuple_with_other_types(tuple_all: tuple[int, float, bool, str])->None:
    #         """
    #         Return the built-in sequence tuple with other types.

    #         Args:
    #             tuple_all: A tuple of integers, floating point numbers, booleans, and strings.

    #         Returns:
    #             None: The function does not return anything.
    #         """
    #         return
    #     expect = {
    #         "name": "builtin_sequence_tuple_with_other_types",
    #         "description": "Return the built-in sequence tuple with other types.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "tuple_all": {
    #                     "type": "array",
    #                     "items": [
    #                         {
    #                             "type": "integer"
    #                         },
    #                         {
    #                             "type": "number"
    #                         },
    #                         {
    #                             "type": "boolean"
    #                         },
    #                         {
    #                             "type": "string"
    #                         }
    #                     ],
    #                     "description": "A tuple of integers, floating point numbers, booleans, and strings."
    #                 }
    #             },
    #             "required": ["tuple_all"]
    #         }
    #     }
    #     # tuple json.dumps?
    #     # thistuple = ("apple", 1, "cherry")
    #     # print(thistuple)
    #     # print(json.dumps(thistuple))
    #     # TODO: tuple 지원 안됨cl
    #     self.SchemaAssertEqual(builtin_sequence_tuple_with_other_types, expect)
    # range 는 List 또는 Tuple로 대체 가능    
    # def test_builtin_sequence_tuple_with_other_types(self):


if __name__ == '__main__':

    unittest.main()
