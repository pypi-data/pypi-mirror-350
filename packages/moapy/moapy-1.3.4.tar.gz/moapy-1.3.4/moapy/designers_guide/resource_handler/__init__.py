from moapy.designers_guide.resource_handler.content_component import (
    Content,
    Component,
    ContentComponentManager,
)
from moapy.designers_guide.resource_handler.dict_content_component import (
    create_dict_content_component_manager,
)

def create_content_component_manager(
    *,
    content_list: list[Content] | None = None,
    component_list: list[Component] | None = None,
) -> ContentComponentManager:
    if content_list is None:
        content_list = []
    if component_list is None:
        component_list = []

    return create_dict_content_component_manager(
        content_list=content_list,
        component_list=component_list,
    )

# def create_simple_mapping_manager():
#     return {}

__all__ = ["create_content_component_manager", "ContentComponentManager"]
