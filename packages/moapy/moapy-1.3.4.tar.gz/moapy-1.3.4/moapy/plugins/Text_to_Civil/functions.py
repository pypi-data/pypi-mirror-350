import inspect
import pathlib
import importlib
import json
import requests
import datetime
import os

from rod.schema_generator import SchemaInterface

from openai_functions import FunctionWrapper
from docstring_parser import parse
# https://openai-functions.readthedocs.io/en/latest/introduction.html

# import ast

# 0. information

# json schema of function example
# {
#     "name": "get_current_weather",
#     "description": "Get the current weather for a city",
#     "arguments": {
#         "city": {
#             "type": "string",
#             "description": "The city to get the weather for",
#         },
#         "country": {
#             "type": "string",
#             "description": "The country to get the weather for",
#         },
#     },
#     "returns": {
#         "type": "object",
#         "properties": {
#             "temperature": {
#                 "type": "number",
#                 "description": "The current temperature in the city",
#             },
#             "conditions": {
#                 "type": "string",
#                 "description": "The current weather conditions",
#             },
#         },
#     },
# }

'''
docstring annotation parameter type can be one of the following
- "int"
- "float"
- "str"
- "bool"
- "list[int]"
- "list[float]"
- "list[str]"
- "list[bool]"
- class
'''

# 1. select the file to function-knowledge
# basecode_path = "D:\\MIDAS\\source\\engineers-api-python_2\\base\\engineers.py"
# target_file_name = "element_divide.py"
pwd = pathlib.Path(__file__).parent.absolute()
basecode_path = str(pwd) + "\\simple_base.py"
target_file_name = "textImage.py"

# 2. extract the function code and schema from the file
def derive_module_name(file_name):
    return file_name.split(".")[0]

target_moduel_name = derive_module_name(target_file_name)
target_module = importlib.import_module(target_moduel_name)

def get_functions_from_moduel(module):
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            # filter out functions that are imported from other modules
            if obj.__module__ == module.__name__:
                functions.append(obj)
    return functions

target_functions = get_functions_from_moduel(target_module)

codes = []
schemas = []

for function in target_functions:
    schema = SchemaInterface(function)
    schemas.append(schema)
    codes.append(inspect.getsource(function))
    # pretty_json = json.dumps(inspect.getsource(function), indent=2)
    # print(pretty_json)

#print pretty json
pretty_json = json.dumps(schemas, indent=2)
print(pretty_json)
# about usign moa-gpt api
# - API spec : https://moa.rpm.kr-dv-midasit.com/backend/gpt/swagger
# - to use api you need to get access token
#   - 1. open browser and login to https://moa.rpm.kr-dv-midasit.com/gpt
#   - 2. open developer tool and go to network tab
#   - 3. click on the request and get the access token from the request header(X-Auth-Token)

# 3. create function-knowledge or get function-knowledge id
#   - create function-knowledge : POST https://moa.rpm.kr-dv-midasit.com/backend/gpt/function-knowledges
#   - get function-knowledge id : GET https://moa.rpm.kr-dv-midasit.com/backend/gpt/function-knowledges

# members API
# 파싱서버 https://url.midasuser.com/ensol-api.json 로부터 url 을 가져오는 방식으롭 변경 예정
url_members_login = 'https://members.midasuser.com/auth/api/v1/login'
body = {
    'email': os.environ.get('MIDAS_USER_EMAIL'),
    'password': os.environ.get('MIDAS_USER_PASSWORD')
}
login_response = requests.post(url_members_login, json=body)
login_info = login_response.json()  # JSON 응답을 파싱
token = login_info['token']

headers = {
    "X-Auth-Token": "Bearer " + token
}

# get basecode content from file basecode_path
basecode_content = ""
with open(basecode_path, "r") as file:
    basecode_content = file.read()

# get current time stamp
fixed_time_stamp_for_path = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
title_prefix = "function knowledge from plugin_"
title = title_prefix + fixed_time_stamp_for_path

# select function language
language = "python"

# # create function-knowledge
# url_create_function_knowledge = "https://moa.rpm.kr-dv-midasit.com/backend/gpt/function-knowledges"
# function_knowledge = {
#     "title": title,
#     "functionLanguage": language,
#     "refCode": basecode_content
# }
# response = requests.post(url_create_function_knowledge, headers=headers, json=function_knowledge)
# function_knowledge_id = response.json()["threadId"]
function_knowledge_id = "01HVK86H606EGJ2SC8VXSV9AGJ"

# get function-knowledge id
# url_get_function_knowledge = "https://moa.rpm.kr-dv-midasit.com/backend/gpt/function-knowledges"
# response = requests.get(url_get_function_knowledge, headers=headers)
# function_knowledges = response.json()
# print(function_knowledges)

function_id= []
# 4. save the function code and schema
# - save the function code and schema : POST https://moa.rpm.kr-dv-midasit.com/backend/gpt/function-knowledges/{function_knowledge_id}/functions
url_create_function_item = "http://127.0.0.1:7152/backend/gpt/function-knowledges/" + function_knowledge_id + "/functions"
for i in range(len(codes)):
    function_item = {
        "schema": schemas[i],
        "function": codes[i],
        "functionLanguage": language
    }
    response = requests.post(url_create_function_item, headers=headers, json=function_item)
    print(response.json())
    function_id.append(response.json()["functionId"])

url_get_function_item = "https://moa.rpm.kr-dv-midasit.com/backend/gpt/function-knowledges/" + function_knowledge_id + "/functions"

# 5. get function id for executing test


# 6. execute the function with selected arguments (server)
# https://til.simonwillison.net/deno/pyodide-sandbox
# 아직 swagger 가 없어서 서버 코드를 참고해 url 을 가져옴
# url_function_execute = "http://127.0.0.1:7162/backend/function-executor/function-execute"
url_function_execute = "https://moa.rpm.kr-dv-midasit.com/backend/function-executor/function-execute"
# headers_for_function_execute = {
#     "MAPI-Key": os.environ.get('MIDAS_USER_MAPI_KEY')
# }

# function_id = "5b8a5c53-e936-4f10-b837-58da8ec600c2"
# function_knowledge_id = "01HSWR1F1GSZ6B8XCB0DMDZVN5"

# function_execute_calculate_distance = {
#     "functionId": function_id[0],
#     "threadId": function_knowledge_id,
#     "function" : {
#         "name": "calculate_distance",
#         "arguments": {
#             "lat1": 37.5665,
#             "lon1": 126.9780,
#             "lat2": 40.7128,
#             "lon2": -74.0060
#         },
#     },
#     "functionLanguage" : language
# }

# function_execute_get_sum_coordinates = {
#     "functionId": function_id[0],
#     "threadId": function_knowledge_id,
#     "function" : {
#         "name": "get_sum_coordinates",
#         "arguments": {
#             "start_coord": [1.1, 2.2, 3.3],
#             "end_coord": [2.2, 3.3, 4.4]
#         },
#     },
#     "functionLanguage" : language
# }

function_execute_get_sum_node_coordinates = {
    "functionId": function_id[0],
    "threadId": function_knowledge_id,
    "function" : {
        "name": "get_sum_node_coordinates",
        "arguments": {
            "nodes": [1, 2, 3]
        },
    },
    "functionLanguage" : language
}

function_execute_get_sum_node_coordinates_headers = {
    "MAPI-Key": "eyJ1ciI6ImhqYW5nQG1pZGFzaXQuY29tIiwicGciOiJjaXZpbCIsImNuIjoicVI0d0FYNUNTZyJ9.78fdf94142d3acefdecbf2a61d411126a6e1d1bd0acb37799d328270141725eb",
}

# function_execute = {
#     "functionId": function_id,
#     "threadId": function_knowledge_id,
#     "function" : {
#         "name": "get_sum_coordinates",
#         "arguments": {
#             "start_coord": 1.1,
#             "end_coord": 2.2
#         },
#     },
#     "functionLanguage" : language
# }
    
# response = requests.post(url_function_execute, headers={}, json=function_execute_calculate_distance)
# response = requests.post(url_function_execute, headers={}, json=function_execute_get_sum_coordinates)
response = requests.post(url_function_execute, headers=function_execute_get_sum_node_coordinates_headers, json=function_execute_get_sum_node_coordinates)
print(response.json())

# 7. execute the function with selected arguments (client)
# - 이건 프론트, 플러그인 개발(김현님)의 기술지원 및 협업이 필요함

# 다음 스텝
# civil api 연동된 함수 사용
# - civil 인스톨 API 연결
# - MAPI 키 연결 방식 설명

# civil 인스톨
# - common 파일 복사 : \\nas_midasitdev\Planmaster\100_Dev\Pub\MidasWin\Civil\NX\CVLw_master\x64\Common
# - solver 파일 복사(하위 폴더는 복사 하지 않음) : \\nas_midasitdev\Planmaster\100_Dev\Pub\MidasWin\CVLw945_Renew\x64\FES_Solver
# - DBase 폴더 복사 : \\nas_midasitdev\Planmaster\100_Dev\Pub\MidasWin\DBase\Gen-Civil_950
#  - 복사후 폴더 이름 DBase 로 변경
# - civil 파일 복사 : \\nas_midasitdev\Planmaster\100_Dev\Pub\MidasWin\Civil\NX\CVLw_master\x64\x64_CivilRelease_D240402_T1546_N578_r_b3_MR
# >> 컨플루언스에 정리 예정


# 아래는 importlib를 사용하지 않고 ast를 사용하여 파일을 텍스트로 읽어 파싱으로 진행하는 방식 참고용
# 좀 더 나은 방법이지만, 바닥부터 직접 파싱을 해야하는 단점으로 시간이 오래 걸릴 것 판단해 빠른 결과를 볼 수 있는 방향으로 선택
# print(target_file_path)
# with open(target_file_path) as file:
#     file_content = file.read()
#     node = ast.parse(file_content)
#     # get function body
#     for elem in node.body:
#         if isinstance(elem, ast.FunctionDef):
#             function_schema = {}
#             function_code = ast.get_source_segment(file_content, elem)
#             function_schema["name"] = elem.name
#             doc_string = ast.get_docstring(elem)
#             if doc_string:
#                 parsed_doc_string = parse(doc_string)
#                 function_schema["description"] = parsed_doc_string.short_description
#                 function_schema["arguments"] = {}
#                 for param in parsed_doc_string.params:
#                     function_schema["arguments"][param.arg_name] = {
#                         "type": param.type_name,
#                         "description": param.description
#                     }
#             function_schema["description"] = {}
#             print(ast.dump(elem))

# https://github.com/rr-/docstring_parser
# https://docs.python.org/ko/3/library/ast.html
            
        # print(elem)
