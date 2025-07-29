import os
import sys
from mypy.stubgen import generate_stubs
from mypy.stubgen import Options

def main():
    # base 디렉토리를 sys.path에 추가
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "base"))
    sys.path.insert(0, base_dir)

    # 모듈 이름
    module_name = "midasapi"
    
    # Options 객체 생성
    options = Options(
        pyversion=(3, 8),           # Python 버전
        no_import=False,            # 임포트 사용 여부
        inspect=False,              # 코드 검사 여부
        doc_dir="",                 # 문서 디렉터리 (빈 문자열로 설정)
        search_path=[],             # 모듈 검색 경로
        interpreter=sys.executable, # 현재 Python 인터프리터 경로
        parse_only=True,            # 코드 파싱만 할지 여부
        ignore_errors=False,        # 오류 무시 여부
        include_private=True,       # 프라이빗 멤버 포함 여부
        output_dir=base_dir,        # 출력 디렉터리
        modules=[module_name],      # 모듈 리스트
        packages=[],                # 패키지 리스트 (사용하지 않음)
        files=[],                   # 파일 리스트 (사용하지 않음)
        verbose=False,              # 상세 출력 여부
        quiet=False,                # 조용한 모드 여부
        export_less=False,          # 내보내기 적게
        include_docstrings=True     # docstring 포함 여부
    )

    # 스텁 파일 생성
    generate_stubs(options)


if __name__ == "__main__":
    main()
