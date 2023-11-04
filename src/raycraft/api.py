from typing import Any
from ray.serve import deployment
from types import MethodType


class RayServeDeployment:
    def __init__(self, **serve_deployment_kwargs):
        self._serve_deployment_kwargs = serve_deployment_kwargs
        self._initializers = {}
        self._methods = {}

    def init(self, func) -> None:
        self._initializers[func.__name__] = func

    def remote(self, func) -> None:
        self._methods[func.__name__] = func

    def post(self, func):
        self._methods["__call__"] = func

    def __call__(out, *args: Any, **kwds: Any) -> Any:
        @deployment(**out._serve_deployment_kwargs)
        class RayServeDeploymentWrapper:
            def __init__(self):
                for (
                    initializer_name,
                    initializer,
                ) in out._initializers.items():
                    print(f"setting {initializer_name}")
                    setattr(self, initializer_name, initializer())

                for method_name, method in out._methods.items():
                    print(f"setting {method_name}")
                    # use MethodType to bind the method to the class
                    setattr(self, method_name, MethodType(method, self))
                    # setattr(self, method_name, method)

        app = RayServeDeploymentWrapper.bind()
        return app
