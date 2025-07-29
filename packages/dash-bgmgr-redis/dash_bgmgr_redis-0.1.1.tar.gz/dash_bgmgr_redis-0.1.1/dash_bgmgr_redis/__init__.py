"""
Redis-based background callback manager for Dash applications.
"""

__version__ = "0.1.0"
__author__ = "RazgrizHsu"
__email__ = "dev@raz.tw"

from .redis import (
    RedisCache,
    RedisBgManager,
    NewRedisBgManager,
)

__all__ = [
    "RedisCache",
    "RedisBgManager",
    "NewRedisBgManager",
]
