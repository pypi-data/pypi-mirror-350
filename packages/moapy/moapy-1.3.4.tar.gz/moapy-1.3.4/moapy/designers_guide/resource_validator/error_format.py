from enum import Enum
from dataclasses import dataclass, field

class ErrorType(Enum):
    def to_string(self):
        return self.value
    ERROR = "ERROR"
    WARNING = "WARNING"

class ErrorCode(Enum):
    def to_string(self):
        return self.value[0]
    def to_description(self):
        return self.value[1]
    
    UNDEFINED_WARNING = ("W-00-00", "정의 되지 않은 Warning")
    UNDEFINED_ERROR = ("E-00-00", "정의 되지 않은 Error")

    ISOLATED_COMPONENTS = ("W-01-00", "미사용 component. 현재 컨텐츠에서 사용되지 않음")
    REDUNDANT_COMPONENTS = ("E-01-01", "중복 정의 component")

    MISSING_CONTENT_ESSENTIAL = ("E-02-00", "content 필수 요소 누락")
    MISSING_COMPONENT_ESSENTIAL = ("E-02-01", "component 필수 요소 누락")
    EXCEED_COMPONENT_INPUT_RANGE = ("E-02-02", "component 입력 범위 초과")
    MISSING_INPUT_VALUES = ("E-02-04", "Input 값 누락")

    MISSING_REQUIRED_COMPONENTS = ("E-03-00", "연산에 필요한 required symbol 누락")
    UNUSED_REQUIRED_SYMBOLS = ("W-03-01", "미사용 required symbol")
    CYCLIC_REQUIRED_COMPONENTS = ("E-03-02", "component 순환 참조")
    FAULTY_REQUIRED_COMPONENTS = ("E-03-03", "참조 component 연결 오류")
    INVALID_REQUIRED_COMPONENTS = ("E-03-04", "미정의 component 참조 오류")

    LATEX_SYNTAX_ERROR = ("E-04-00", "수식 구문 에러")
    LATEX_UNCALCULABLE = ("E-04-01", "연산 불가능 수식")
    NOT_MATCHED_CONDITION = ("E-04-02", "연산 조건 매칭 실패")

@dataclass
class ErrorWarning:
    type: ErrorType = ErrorType.ERROR
    error_code: ErrorCode = ErrorCode.UNDEFINED_ERROR
    invalid_required: str = ''
    occurred_property: str = ''
    occurred_equation: str = ''
    occurred_condition: str = ''
    occurred_point: str = ''
    occurred_value: str = ''

    def __init__(self, error_type: ErrorType, error_code: ErrorCode):
        self.type = error_type
        self.error_code = error_code

    def __str__(self):
        return f"{self.type.to_string()}\t{self.error_code}\n"

    def __repr__(self):
        return self.__str__()

    # TODO : detail 형식 추가 논의 필요
    def to_dict(self):
        details = {}
        if self.occurred_property != '':
            details['property'] = self.occurred_property
        elif self.invalid_required != '':
            details['required'] = self.invalid_required
        elif self.occurred_equation != '':
            details['equation'] = self.occurred_equation
        elif self.occurred_condition != '':
            details['condition'] = self.occurred_condition
        elif self.occurred_point != '':
            details['point'] = self.occurred_point
        elif self.occurred_value != '':
            details['value'] = self.occurred_value
        
        return {
            'type': self.type.to_string(),
            'code': self.error_code.to_string(),
            'description': self.error_code.to_description(),
            'detail': details
        }

    def define_error_warning(self, error_code: ErrorCode):
        error_type = ErrorType.ERROR if error_code.startswith('E') else ErrorType.WARNING
        return self.__init__(error_type, error_code)
    
def append_error_warning(error_warnings: dict, id: str, new_data: ErrorWarning):
    def convert_to_dict(data):
        if isinstance(data, dict):
            return data
        elif isinstance(data, ErrorWarning):
            return data.to_dict()
        else:
            return None

    if isinstance(new_data, list):
        for data in new_data:
            if id in error_warnings:
                error_warnings[id].append(convert_to_dict(data))
            else:
                error_warnings[id] = [convert_to_dict(data)]
    else:
        if id in error_warnings:
            error_warnings[id].append(convert_to_dict(new_data))
        else:
            error_warnings[id] = [convert_to_dict(new_data)]