import inspect
import os
import sys
from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, Union, get_type_hints, ClassVar
from fastapi import APIRouter
from fastapi.routing import APIRoute
from pydantic import BaseModel, create_model, ConfigDict
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import (
    get_flat_dependant,
    create_body_model,
    create_model_field,
    ensure_multipart_is_installed
)
from pydantic import Field as ModelField
from typing import Optional, Type
from fastapi import params
from starlette.routing import request_response

def custom_get_body_field(*, dependant: Dependant, name: str) -> Optional[ModelField]:
    flat_dependant = get_flat_dependant(dependant)
    if not flat_dependant.body_params:
        return None
    first_param = flat_dependant.body_params[0]
    field_info = first_param.field_info
    embed = getattr(field_info, "embed", None)
    body_param_names_set = {param.name for param in flat_dependant.body_params}
    # if len(body_param_names_set) == 1 and not embed:
    #     ensure_multipart_is_installed(first_param)
    #     return first_param
    # If one field requires to embed, all have to be embedded
    # in case a sub-dependency is evaluated with a single unique body field
    # That is combined (embedded) with other body fields
    for param in flat_dependant.body_params:
        setattr(param.field_info, "embed", True)  # noqa: B010
    model_name = name
    # BodyModel = create_body_model(
    #     fields=flat_dependant.body_params, model_name=model_name
    # )
    fields = {param.name: (param.type_, param.field_info) for param in flat_dependant.body_params}

    # create_body_model 함수를 직접 구현
    BodyModel = create_model(model_name, **fields)
    
    required = any(True for f in flat_dependant.body_params if f.required)
    BodyFieldInfo_kwargs: Dict[str, Any] = {
        "annotation": BodyModel,
        "alias": "body",
    }
    if not required:
        BodyFieldInfo_kwargs["default"] = None
    if any(isinstance(f.field_info, params.File) for f in flat_dependant.body_params):
        BodyFieldInfo: Type[params.Body] = params.File
    elif any(isinstance(f.field_info, params.Form) for f in flat_dependant.body_params):
        BodyFieldInfo = params.Form
    else:
        BodyFieldInfo = params.Body

        body_param_media_types = [
            f.field_info.media_type
            for f in flat_dependant.body_params
            if isinstance(f.field_info, params.Body)
        ]
        if len(set(body_param_media_types)) == 1:
            BodyFieldInfo_kwargs["media_type"] = body_param_media_types[0]
    final_field = create_model_field(
        name="body",
        type_=BodyModel,
        required=required,
        alias="body",
        field_info=BodyFieldInfo(**BodyFieldInfo_kwargs),
    )
    # ensure_multipart_is_installed(final_field)
    return final_field

class CustomAPIRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body_field = custom_get_body_field(dependant=self.dependant, name=self.unique_id)
        self.app = request_response(self.get_route_handler())

# 라우터를 모듈별로 저장할 딕셔너리
module_routers: Dict[str, APIRouter] = {}

def get_router_for_module(module_name: str) -> APIRouter:
    if module_name not in module_routers:
        module_routers[module_name] = APIRouter()
    return module_routers[module_name]

def data_conv(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs).arguments

        for name, param in sig.parameters.items():
            param_class = param.annotation
            if name in bound_args:
                if isinstance(bound_args[name], dict):
                    if getattr(param_class, '__origin__', None) is Union:
                        for cls in param_class.__args__:
                            cls_fields = set(get_type_hints(cls).keys())
                            if cls_fields.issuperset(bound_args[name].keys()):
                                bound_args[name] = cls(**bound_args[name])
                                break
                    elif issubclass(param_class, BaseModel):
                        bound_args[name] = param_class(**bound_args[name])

        return func(*bound_args.values())

    return wrapper

def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])

class MBaseModel(BaseModel, ABC):
    model_config = ConfigDict(
        title=None,
        description=None,
        alias_generator=to_camel,
        populate_by_name=True
    )

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # 모듈과 클래스 이름 정보를 생성
        qualified_name_info = f"{cls.__module__}.{cls.__name__}"

        # 기존 schema_extra 병합 처리
        json_schema_extra = cls.model_config.get("json_schema_extra", {})
        if "x-component-detail" not in json_schema_extra:
            json_schema_extra["x-component-detail"] = {}
        json_schema_extra["x-component-detail"]["id"] = qualified_name_info

        # model_config 업데이트
        cls.model_config = ConfigDict(
            **{k: v for k, v in cls.model_config.items() if k != "json_schema_extra"},
            json_schema_extra=json_schema_extra,
        )

def auto_schema(title: str, description: str, std_type: str = "", design_code: str = "") -> Callable:
    def decorator(func: Callable) -> Callable:
        if os.getenv("SKIP_AUTO_SCHEMA") == "True":
            return func  # Skip the auto_schema logic

        func_name = func.__name__
        module = inspect.getmodule(func)
        if module is None:
            # 동적으로 생성된 함수 처리
            module = sys.modules[__name__]  # 현재 모듈로 설정

        module_name = module.__name__
        path = f"/execute?functionId={module_name.replace('.', '-')}-{func_name}"

        router = get_router_for_module(module_name + func_name)
        operation_id = func_name.replace('_', ' ')

        # x-content-info 기본 정보
        content_info = {
            "title": title,
            "description": description,
        }

        # design_code가 제공되었을 경우 추가 정보 포함
        if design_code:
            content_info.update({
                "standardType": std_type,
                "codeName": design_code
            })

        # API 경로에 route 추가
        router.add_api_route(
            path,
            func,
            methods=["POST"],
            operation_id=operation_id,
            route_class_override=CustomAPIRoute,
            summary=title,  # Title 추가
            description=description,  # Description 추가
            response_model_exclude_none=True,
            response_model_exclude_unset=True,
            response_model_exclude_defaults=True,
            openapi_extra={"x-content-info": content_info}
        )
        return data_conv(func)  # 데코레이터에서 원래 함수를 반환

    return decorator  # 내부 데코레이터 반환