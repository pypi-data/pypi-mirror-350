# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2025/5/14 15:37
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

from .core import trace, debug, info, warning, error, critical, update_config, get_logger

__version__ = "v0.0.1"

__all__ = [
    "trace",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "update_config",
    "get_logger",
]