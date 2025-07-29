# easyremote/__init__.py
from .nodes.server import Server
from .nodes.compute_node import ComputeNode
from .decorators import remote
from .core.utils.exceptions import (
    EasyRemoteError,
    NodeNotFoundError,
    FunctionNotFoundError,
    ConnectionError,
    SerializationError,
    RemoteExecutionError,
)
from .core.utils.performance import get_performance_monitor

__version__ = "0.1.2"

__all__ = [
    'Server',
    'ComputeNode',
    'remote',
    'EasyRemoteError',
    'NodeNotFoundError',
    'FunctionNotFoundError',
    'ConnectionError',
    'SerializationError',
    'RemoteExecutionError',
    'get_performance_monitor',
]