# flake8: noqa: E704
from typing import Optional, Protocol, TypeAlias
from typing_extensions import deprecated

Component: TypeAlias = dict[str, any]
DataTable: TypeAlias = dict[str, any]
Content: TypeAlias = dict[str, any]

WILL_DEPRECATED_NO_USE_METHODS = "사용 하는 곳이 없음"

class ContentManager(Protocol):
    def find_content_by_id(self, id: str) -> Optional[Component]: ...
    def content_list(self) -> list[Component]: ...


class ComponentManager(Protocol):
    """
    ComponentManager는 컴포넌트 목록과 데이터 테이블을 관리하는 프로토콜입니다.
    """
    @property  #TODO: replace to method
    def component_list(self) -> list[Component]: ...

    @property
    def binary_operators(self) -> list[str]: ...

    @property
    def relation_operators(self) -> list[str]: ...

    @property
    def function_operators(self) -> list[str]: ...

    def get_figure_server_url(self) -> str: ...

    def find_component_by_id(self, id: str) -> Optional[Component]: ...

    def update_component(self, id: str, component: Component) -> None: ...

    def get_table_type(self, comp: Component) -> str: ...
    
    def get_table_by_component(self, comp: Component) -> Optional[DataTable]: ...

    def get_table_enum_by_component(self, comp: Component) -> Optional[list[dict]]: ...

    def get_table_data_by_component(self, comp: Component) -> Optional[list[str]] | Optional[list[list[str]]]: ...

    def convert_enum_table_to_detail(
        self, comp: Component
    ) -> Optional[list[list[str]]]: ...

    def get_ref_type(self, id) -> str: ...
    
    def get_component_type(self, comp: Component) -> str: ...

    @deprecated(WILL_DEPRECATED_NO_USE_METHODS)
    def get_table_criteria_by_component(
        self, comp: Component
    ) -> Optional[list[dict]]: ...

    @deprecated(WILL_DEPRECATED_NO_USE_METHODS)
    def find_by_latex_symbol(self, target_latex_symbol: str) -> Optional[Component]: ...

    @deprecated(WILL_DEPRECATED_NO_USE_METHODS)
    def find_comp(
        self, latex_symbol: str, code_name: str, reference: str
    ) -> Optional[Component]: ...

class ContentComponentManager(ComponentManager, ContentManager): ...
