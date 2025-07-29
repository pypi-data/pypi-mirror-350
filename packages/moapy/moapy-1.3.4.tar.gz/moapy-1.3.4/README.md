![banner](https://patch.midasit.com/00_MODS/kr/80_WebResource/engineers/moapy_banner.png)

[![made-with-python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## Midas API: 엔지니어링의 혁신 🚀
Midas API와 함께 엔지니어링의 미래로 오신 것을 환영합니다! 🌟 이 최첨단 저장소는 전통적인 엔지니어링 방법론을 초월하기 위해 설계되었습니다. 혁신의 금광인 Midas API는 여러분의 기여를 기다리고 있습니다. 함께 가능성의 경계를 넘어서 봅시다! 😊

## 목차
- [소개](#소개)
- [시작하기](#시작하기)
- [코딩 규칙](#코딩-규칙)
- [규칙](#규칙)
- [사용법](#사용법)
- [기여하기](#기여하기)
- [라이선스](#라이선스)
- [연락처](#연락처)

## 소개
Midas API는 엔지니어링 분야를 혁신하기 위해 설계된 최첨단 도구입니다. 강력하고 확장 가능하며 효율적인 솔루션을 제공하여 엔지니어들이 복잡한 문제를 쉽게 해결할 수 있도록 합니다. 숙련된 전문가든 초보자든 Midas API는 여러분의 엔지니어링 여정을 지원합니다.

## 시작하기
### 사전 준비
1. **VSCode 설치**: [공식 Visual Studio Code 웹사이트](https://code.visualstudio.com/download)에서 Visual Studio Code를 다운로드하고 설치하세요.
2. **Python 설치**: [공식 Python 웹사이트](https://www.python.org/downloads/release/python-3121/)에서 Python 3.12.1을 다운로드하고 설치하세요. 설치 중에 Python을 PATH에 추가하는 것을 잊지 마세요.
3. **Pipenv 설치**: Pip을 사용하여 Pipenv를 설치하세요.
    ```bash
    pip install pipenv
    ```
    - 문서: [Pipenv: Python Dev Workflow for Humans](https://pipenv.pypa.io/en/latest/)
4. **프로젝트 종속성 설치**: 프로젝트 디렉토리로 이동하여 Pipenv를 사용하여 필요한 모듈을 설치하세요.
    - 실행 환경:
    ```bash
    pipenv install
    ```
    - 개발 환경:
    ```bash
    pipenv install --dev
    ```
5. **Midas API 사용 준비**: 자세한 내용은 [Midas API Documentation](https://midas-support.atlassian.net/wiki/spaces/MAW/overview)을 참조하세요.

## 코딩 규칙
### 프로젝트 구조
- **project/**: 각 플러그인을 이 폴더 내에서 개발합니다.
- **base/**: 공유 유틸리티 함수 및 기본 모듈을 포함합니다. 계산 기본 함수를 위해 이 폴더를 사용하세요.
- **tests/**: 회귀 테스트를 위한 테스트 파일을 포함합니다.
- **rod/**: 이 저장소에서 JSON 스키마를 추출합니다.
- **docs/**: Sphinx 문서 폴더입니다.

### 스타일 가이드
포괄적인 코딩 규칙을 위해 [Google Python 스타일 가이드](https://yosseulsin-job.github.io/styleguide/pyguide.html)를 따르세요.

- **Flake8 사용**: 개발 중 코딩 규칙을 자동으로 확인하고 적용하기 위해 `flake8`을 설치하세요.
    ```bash
    pip install flake8
    ```
    ![flake8 Visual Studio Code extension](./resources/flake8_install.png)
- **개발 환경**: 개발 환경을 `flake8`을 사용하도록 구성하세요. `flake8`이 지적하는 문제는 신속하게 수정해야 합니다.

### 문서화 가이드
적절한 문서화는 유지 관리에 필수적입니다. 특히 `base` 모듈의 모든 함수는 잘 문서화되어야 합니다.

- **autoDocstring 사용**: docstring 작성을 돕기 위해 `autoDocstring`을 설치하세요.(ctrl + shift + 2)
    ![autoDocstring Visual Studio Code extension](./resources/autoDocstring_install.png)
- **Docstrings**: Google 스타일의 docstring을 사용하세요. docstring 작성을 돕기 위해 필요한 확장 기능을 설치하세요.
    - **예시**: docstring을 사용한 데이터 클래스:
        ```python
        from dataclasses import dataclass, field as dataclass_field

        @dataclass
        class Person:
            """
            Person details.
            """
            name: str = dataclass_field(default="", metadata={"description": "The person's full name."})
            age: int = dataclass_field(default=0, metadata={"description": "The person's age."})
            email: str = dataclass_field(default='', metadata={"description": "The person's email address."})
        ```

    - **예시**: docstring을 사용한 Pydantic 모델:
        ```python
        from pydantic import BaseModel, Field
        from typing import List, Dict, Union

        class Contact(BaseModel):
            """
            Contact details.
            """
            phone: str = Field(default="", description="The contact's phone number.")
            address: str = Field(default='', description="The contact's address.")

        def my_function(person: Person, contacts: List[Contact], settings: Dict[str, Union[int, str]] = {}) -> bool:
            """
            Processes person and their contacts with given settings.

            Args:
                person: The person details.
                contacts: List of contact details.
                settings: Miscellaneous settings.

            Returns:
                bool: True if successful, False otherwise.
            """
            return True
        ```

### 테스트
새로운 코드의 신뢰성을 보장하기 위해 포괄적인 테스트를 작성하세요.

- **회귀 테스트**: `base` 모듈에 대한 추가 사항이 있을 경우, `pytest`를 사용하여 해당 회귀 테스트를 추가하세요.
- **테스트 파일**: `tests` 폴더에 `test_*.py` 명명 규칙을 사용하여 테스트 파일을 저장하세요.
  
  - **예시 테스트**:
    ```python
    import json
    import pytest
    import moapy.plugins.baseplate_KDS41_30_2022.baseplate_KDS41_30_2022_calc

    def test_baseplate_KDS41_30_2022_calc():
        input = {  
            'B' : 240, 'H' : 240, 'Fc' : 24, 'Fy' : 400,  
            'Ec' : 25811.006260943130, 'Es' : 210000,  
            'bolt' : [  
              { 'X' : 90, 'Y' : 0, 'Area' : 314.15926535897933 },  
              { 'X' : -90, 'Y' : 0, 'Area' : 314.15926535897933 } ],  
            'P' : -3349.9999999999964, 'Mx' : 0, 'My' : 51009999.999999985 
        }

        JsonData = json.dumps(input)
        result = moapy.plugins.baseplate_KDS41_30_2022.baseplate_KDS41_30_2022_calc.calc_ground_pressure(JsonData)
        
        assert pytest.approx(result['bolt'][0]['Load']) == 0.0
        assert pytest.approx(result['bolt'][1]['Load']) == -269182.84245616524
    ```

### 요약
- **코딩 규칙**: Google Python 스타일 가이드를 따르고 `flake8`을 사용하여 적용합니다.
- **문서화**: 모든 함수에 대해 적절한 docstring을 작성하고 유지합니다.
- **테스트**: 새 함수에 대한 테스트 케이스를 개발하여 회귀 테스트를 가능하게 합니다.

이 규칙과 관례를 따르면 코드베이스의 품질, 일관성 및 신뢰성을 유지할 수 있습니다.



---

For further details, refer to the complete documentation and get started on your journey with Midas API today!
