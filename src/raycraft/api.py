from typing import Any
from ray.serve import deployment, ingress
from types import MethodType
from varname import varname
from fastapi import FastAPI


def to_camel_case(text):
    text = text.replace("_", " ")
    return "".join(x for x in text.title() if not x.isspace())


class RayCraftAPI:
    def __init__(self, **serve_deployment_kwargs):
        self._serve_deployment_kwargs = serve_deployment_kwargs
        self._deployment_name = varname()
        self._initializers = {}
        self._remote_methods = {}
        self._http_methods = {}

    def init(self, func) -> None:
        self._initializers[func.__name__] = func

    def remote(self, func) -> None:
        self._remote_methods[func.__name__] = func

    def post(self, path: str) -> Any:
        def decorator(func):
            self._http_methods[func.__name__] = {
                "path": path,
                "func": func,
            }

        return decorator

    def __call__(self) -> Any:
        app = FastAPI()

        def constructor(obj):
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
            app.post(method_dict["path"])(getattr(obj, method_name))

        deloyment_decorator = deployment(**self._serve_deployment_kwargs)
        deployment_ = deloyment_decorator(ingress(app)(type(obj)))
        deployment_handle = deployment_.bind()
        return deployment_handle
