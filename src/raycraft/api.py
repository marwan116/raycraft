from ray.serve import deployment, ingress
from varname import varname
from fastapi import FastAPI
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
)

from fastapi import routing
from fastapi.datastructures import Default
from fastapi.params import Depends
from fastapi.types import DecoratedCallable
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

IncEx = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any]]


def to_camel_case(text: str) -> str:
    text = text.replace("_", " ")
    return "".join(x for x in text.title() if not x.isspace())


class RayCraftAPI:
    def __init__(self, **serve_deployment_kwargs: Any) -> None:
        self._serve_deployment_kwargs = serve_deployment_kwargs
        self._deployment_name = varname()
        self._initializers: Dict[str, Callable[..., Any]] = {}
        self._remote_methods: Dict[str, Callable[..., Any]] = {}
        self._http_methods: Dict[str, Dict[str, Any]] = {}

    def init(self, func: DecoratedCallable) -> None:
        self._initializers[func.__name__] = func

    def remote(self, func: DecoratedCallable) -> None:
        self._remote_methods[func.__name__] = func

    def get(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def put(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def post(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def delete(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def options(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def head(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def patch(
        self,
        path: str,
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: Optional[str] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[[DecoratedCallable], None]:
        def decorator(func: DecoratedCallable) -> None:
            self._http_methods[func.__name__] = {
                "args": [path],
                "kwargs": {
                    "response_model": response_model,
                    "status_code": status_code,
                    "tags": tags,
                    "dependencies": dependencies,
                    "summary": summary,
                    "description": description,
                    "response_description": response_description,
                    "responses": responses,
                    "deprecated": deprecated,
                    "operation_id": operation_id,
                    "response_model_include": response_model_include,
                    "response_model_exclude": response_model_exclude,
                    "response_model_by_alias": response_model_by_alias,
                    "response_model_exclude_unset": response_model_exclude_unset,
                    "response_model_exclude_defaults": response_model_exclude_defaults,
                    "response_model_exclude_none": response_model_exclude_none,
                    "include_in_schema": include_in_schema,
                    "response_class": response_class,
                    "name": name,
                    "callbacks": callbacks,
                    "openapi_extra": openapi_extra,
                    "generate_unique_id_function": generate_unique_id_function,
                },
                "func": func,
            }

        return decorator

    def __call__(self) -> Any:
        app = FastAPI()

        def constructor(obj: Any) -> None:
            for (
                initializer_name,
                initializer,
            ) in self._initializers.items():
                setattr(obj, initializer_name, initializer())

            # for method_name, method in self._remote_methods.items():
            #     # use MethodType to bind the method to the class
            #     setattr(obj, method_name, MethodType(method, obj))

            # for method_name, method_dict in self._http_methods.items():
            #     # use the fastpi app to add the method as a route
            #     app.post(method_dict["path"])(MethodType(method_dict["func"], obj))

        cls_ = type(
            to_camel_case(self._deployment_name),
            (object,),
            {
                "__init__": constructor,
                **{
                    method_name: method
                    for method_name, method in self._remote_methods.items()
                },
                **{
                    method_name: method_dict["func"]
                    for method_name, method_dict in self._http_methods.items()
                },
            },
        )

        obj = cls_()
        for method_name, method_dict in self._http_methods.items():
            # use the fastpi app to add the method as a route
            app.post(*method_dict["args"], **method_dict["kwargs"])(
                getattr(obj, method_name)
            )

        deloyment_decorator = deployment(**self._serve_deployment_kwargs)
        deployment_ = deloyment_decorator(ingress(app)(type(obj)))
        deployment_handle = deployment_.bind()
        return deployment_handle
