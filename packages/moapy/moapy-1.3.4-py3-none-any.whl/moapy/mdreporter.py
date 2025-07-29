import json
from mdutils.mdutils import MdUtils
from moapy.enum_pre import enUnitLength, enUnitArea, enUnitVolume, enUnitInertia, enUnitForce, enUnitMoment, enUnitLoad, enUnitStress, enUnitThermalExpansion
from enum import Enum

# 단위계 enum 이거 지워야함... 언제 리팩토링해야되는데
class enUnit(Enum):
    NONE = 0
    LENGTH = 1
    MEMBERLENGTH = 2
    AREA = 3
    FORCE = 4
    MOMENT = 5
    STRESS = 6
    INERTIA = 7
    VOLUME = 8

class ReportUtil(MdUtils):
    def __init__(self, file_name, title=""):
        super().__init__(file_name=file_name, title=title)
        self.__header_count = 0
        self.__paragraph_count = 0

    def get_md_text(self):
        file = super().create_md_file()
        return super().read_md_file(file.file_name)

    def add_chapter(self, text):
        self.__header_count += 1
        self.__paragraph_count = 0
        self.new_header(level=1, title=f"{self.__header_count}. {text}")

    def add_paragraph(self, text):
        self.__paragraph_count += 1
        self.new_paragraph(f"({self.__paragraph_count}) {text}")

    def add_image(self, path, image_text=""):
        self.new_line(self.new_inline_image(text=image_text, path=path))

    def add_line_svu(self, str, value, unit):
        self.new_line(f"{str} {value} {self.get_str_unit(unit)}")

    def add_line_fvu(self, formula, value, unit):
        self.new_line(f"{self.add_formula(formula)} = {value :.2f} {unit}")

    def add_line(self, text):
        self.new_line(text)

    def add_formula(self, text):
        return f"${text}$"

def get_data_from_file(file_name):
    with open(file_name, "r", encoding='utf-8') as file:
        return json.load(file)

def find_data(data, key_to_find):
    # 데이터가 딕셔너리일 경우
    if isinstance(data, dict):
        for key, value in data.items():
            if key == key_to_find:
                return value
            # 값이 딕셔너리나 리스트(튜플 포함)일 경우 재귀적으로 탐색
            if isinstance(value, (dict, list, tuple)):
                result = find_data(value, key_to_find)
                if result is not None:
                    return result
    # 데이터가 리스트(또는 튜플)일 경우 각 원소에 대해 재귀적으로 탐색
    elif isinstance(data, (list, tuple)):
        for item in data:
            result = find_data(item, key_to_find)
            if result is not None:
                return result
    # 찾는 키가 없을 경우 None 반환
    return None
