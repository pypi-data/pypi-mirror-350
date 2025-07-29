import os
import ctypes
from moapy.data_post import ResultMD
from moapy.mdreporter import ReportUtil

# 공통 함수: DLL 로드
def load_dll():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')
    return ctypes.CDLL(dll_path)

# 공통 함수: JSON 데이터를 DLL 함수에 전달하고 결과 처리
def call_dll_function(dll, func_name, argtypes, restype, *json_objects):
    func = getattr(dll, func_name)
    func.argtypes = argtypes
    func.restype = restype

    # json_objects를 인코딩합니다.
    encoded_args = []
    for obj in json_objects:
        if isinstance(obj, str):  # 문자열인 경우만 인코딩
            encoded_args.append(obj.encode('utf-8'))
        elif obj is None:  # None인 경우 (nullptr)
            encoded_args.append(ctypes.c_void_p(0))  # nullptr을 표현
        else:  # 다른 객체인 경우
            encoded_args.append(obj)  # 직접 추가

    return func(*encoded_args)

def read_markdown_file(file_path):
    """Markdown 파일을 읽어 문자열로 반환 (UTF-16을 UTF-8로 변환)"""
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    try:
        # UTF-16으로 파일 읽기
        with open(file_path, 'r', encoding='utf-16') as file:
            content = file.read()
        
        # UTF-8로 변환
        return content.encode('utf-8').decode('utf-8')
        
    except FileNotFoundError:
        print(f"파일 '{file_path}' 을(를) 찾을 수 없습니다.")
        return None
    except IOError as e:
        print(f"파일 '{file_path}' 을(를) 읽는 도중 오류가 발생했습니다: {e}")
        return None

def read_file_as_binary(file_path: str) -> bytes:
    """
    주어진 경로의 파일을 바이너리 데이터로 읽어 반환합니다.

    :param file_path: 읽을 파일의 경로
    :return: 파일의 바이너리 데이터
    """
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        return binary_data
    except Exception as e:
        print(f"파일을 읽는 중 오류 발생: {e}")
        return None

# 리포트 생성 함수
def generate_report(dll, func_name, json_data_list):
    result = call_dll_function(dll, func_name, [ctypes.c_char_p] * len(json_data_list), ctypes.c_char_p, *json_data_list)
    util = ReportUtil("test.md")
    util.add_line(read_markdown_file(result))
    return ResultMD(md=util.get_md_text())

def call_func(dll, func_name, json_data_list):
    # 인수의 타입에 따라 argtypes를 설정합니다.
    argtypes = []

    for obj in json_data_list:
        if isinstance(obj, str):  # 문자열인 경우
            argtypes.append(ctypes.c_char_p)
        elif obj is None:  # None인 경우 (nullptr)
            argtypes.append(ctypes.POINTER(ctypes.c_void_p))
        else:  # 다른 객체인 경우
            argtypes.append(ctypes.c_void_p)  # 포인터로 처리

    # C++ DLL 함수 호출
    result = call_dll_function(dll, func_name, argtypes, ctypes.c_char_p, *json_data_list)

    return result