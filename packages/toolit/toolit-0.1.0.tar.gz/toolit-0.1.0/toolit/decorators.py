"""
Decorator to tell if a function is a tool.
"""
from typing import Callable, TypeVar, Any
from .constants import MARKER_TOOL, ToolitTypesEnum


T = TypeVar("T", bound=Callable[..., Any])

def tool(func: T) -> T:
    """Decorator marking a function as a tool."""
    setattr(func, MARKER_TOOL, ToolitTypesEnum.TOOL)
    return func

def sequencial_group_of_tools(func: T) -> T:
    """
    Decorator to a function that returns a list of callable tools.
    """
    setattr(func, MARKER_TOOL, ToolitTypesEnum.SEQUENCIAL_GROUP)
    return func

def parallel_group_of_tools(func: T) -> T:
    """
    Decorator to a function that returns a list of callable tools.
    """
    setattr(func, MARKER_TOOL, ToolitTypesEnum.PARALLEL_GROUP)
    return func