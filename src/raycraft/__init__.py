from .api import RayCraftAPI
from typing import Protocol, Any

class App(Protocol):
    """A very generic application interface."""
    
    # to avoid attribute errors
    def __getattr__(self, name: str) -> Any:
        ...

__all__ = ["App", "RayCraftAPI"]
