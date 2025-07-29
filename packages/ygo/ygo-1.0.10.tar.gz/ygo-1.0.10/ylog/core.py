# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2025/5/14 16:04
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

import sys
from pathlib import Path
from threading import Lock
from typing import Optional

from loguru import logger


class _Logger:
    """
    企业级日志类，基于Loguru封装

    特性：
    1. 高性能：异步写入日志，避免阻塞主线程
    2. 易于管理：多级别日志分离存储，按日期和大小轮转
    3. 分级明确：支持 TRACE/DEBUG/INFO/WARNING/ERROR/CRITICAL 级别
    4. 结构化日志：支持 JSON 格式日志输出
    5. 全局异常捕获：自动记录未处理异常
    """

    def __new__(cls, *args, **kwargs):
        """移除单例限制，允许自由创建多个实例"""
        return super().__new__(cls)

    def __init__(
            self,
            log_dir: str = "logs",
            app_name: str|None = None,
            retention_days: int = 7,
            error_retention_days: int = 30,
            enable_console: bool = True,
            enable_file: bool = True,
            debug_mode: bool = False
    ):
        """初始化日志系统"""
        # 避免重复初始化
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        # 初始化参数
        self.log_dir = Path(log_dir)
        self.app_name = app_name
        self.debug_mode = debug_mode
        self._error_retention_days = error_retention_days
        self._retention_days = retention_days

        # 创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 移除默认sink
        logger.remove()

        # 配置控制台日志
        if enable_console:
            self._setup_console_logging()

        # 配置文件日志
        if enable_file:
            self._setup_file_logging(retention_days, error_retention_days)

        # 全局异常捕获
        self._setup_global_exception_handling()

    def _setup_console_logging(self):
        """配置控制台日志"""
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

        logger.add(
            sys.stderr,
            level="DEBUG" if self.debug_mode else "INFO",
            format=console_format,
            colorize=True,
            backtrace=self.debug_mode,
            diagnose=self.debug_mode,
            # enqueue=True  # 异步写入
        )

    def _setup_file_logging(self, retention_days: int, error_retention_days: int):
        """配置文件日志"""
        # 通用日志格式
        common_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} - {message}"
        )

        # 日志级别配置
        levels = {
            "TRACE": {"level": "TRACE", "retention": f"{retention_days} days", "rotation": "daily"},
            "DEBUG": {"level": "DEBUG", "retention": f"{retention_days} days", "rotation": "daily"},
            "INFO": {"level": "INFO", "retention": f"{retention_days} days", "rotation": "daily"},
            "WARNING": {"level": "WARNING", "retention": f"{error_retention_days} days", "rotation": "daily"},
            "ERROR": {"level": "ERROR", "retention": f"{error_retention_days} days", "rotation": "daily"},
            "CRITICAL": {"level": "CRITICAL", "retention": f"{error_retention_days} days", "rotation": "daily"}
        }

        # 错误级别以上的日志
        error_levels = ("WARNING", "ERROR", "CRITICAL")
        _error_log_file = f"{self.app_name}_{{time:YYYY-MM-DD}}.err.log" if self.app_name is not None else f"{{time:YYYY-MM-DD}}.err.log"
        error_log_file = self.log_dir / _error_log_file
        info_levels = ("INFO", "DEBUG", "TRACE")
        _info_log_file = f"{self.app_name}_{{time:YYYY-MM-DD}}.log" if self.app_name is not None else f"{{time:YYYY-MM-DD}}.log"
        info_log_file = self.log_dir / _info_log_file
        # 错误级别以上的日志
        logger.add(
            str(error_log_file),
            level="ERROR",
            format=common_format,
            rotation=levels["ERROR"]["rotation"],
            retention=levels["ERROR"]["retention"],
            compression="zip",
            backtrace=True,
            diagnose=self.debug_mode,
            # enqueue=True,  # 异步写入
            filter=lambda record: record["level"].name in error_levels,
            catch=True  # 捕获格式化异常
        )
        # 错误级别以下的日志
        logger.add(
            str(info_log_file),
            level="INFO",
            format=common_format,
            rotation=levels["INFO"]["rotation"],
            retention=levels["INFO"]["retention"],
            compression="zip",
            backtrace=True,
            diagnose=self.debug_mode,
            # enqueue=True,  # 异步写入
            filter=lambda record: record["level"].name in info_levels,
            catch=True  # 捕获格式化异常
        )



    def _setup_global_exception_handling(self):
        """配置全局异常捕获"""

        def handle_exception(exc_type, exc_value, exc_traceback):
            """全局异常处理函数"""
            logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical(
                "Unhandled exception occurred"
            )

        sys.excepthook = handle_exception

    def _msgs_to_str(self, *msg: str) -> str:
        return " ".join([str(m) for m in msg])

    def trace(self, *msg: str, **kwargs) -> None:
        """TRACE级别日志"""
        logger.opt(depth=1).trace(self._msgs_to_str(*msg), **kwargs)

    def debug(self, *msg: str, **kwargs) -> None:
        """DEBUG级别日志"""
        logger.opt(depth=1).debug(self._msgs_to_str(*msg), **kwargs)

    def info(self, *msg: str, **kwargs) -> None:
        """INFO级别日志"""
        logger.opt(depth=1).info(self._msgs_to_str(*msg), **kwargs)

    def warning(self, *msg: str, **kwargs) -> None:
        """WARNING级别日志"""
        logger.opt(depth=1).warning(self._msgs_to_str(*msg), **kwargs)

    def error(self, *msg: str, exc_info: Optional[BaseException] = None, **kwargs) -> None:
        """ERROR级别日志"""
        if exc_info:
            logger.opt(depth=1, exception=exc_info).error(self._msgs_to_str(*msg), **kwargs)
        else:
            logger.opt(depth=1).error(self._msgs_to_str(*msg), **kwargs)

    def critical(self, *msg: str, exc_info: Optional[BaseException] = None, **kwargs) -> None:
        """CRITICAL级别日志"""
        if exc_info:
            logger.opt(depth=1, exception=exc_info).critical(self._msgs_to_str(*msg), **kwargs)
        else:
            logger.opt(depth=1).critical(self._msgs_to_str(*msg), **kwargs)

    def update_config(
            self,
            log_dir: str = None,
            app_name: str = None,
            retention_days: int = None,
            error_retention_days: int = None,
            enable_console: bool = None,
            enable_file: bool = None,
            debug_mode: bool = None
    ):
        """
        动态更新日志配置并重新加载日志系统
        注意：这会清除已有的sink并重新创建日志文件
        """

        # 更新配置
        if log_dir is not None:
            self.log_dir = Path(log_dir)
        if app_name is not None:
            self.app_name = app_name
        if retention_days is not None:
            self._retention_days = retention_days
        if error_retention_days is not None:
            self._error_retention_days = error_retention_days
        if debug_mode is not None:
            self.debug_mode = debug_mode

        # 重建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 清除现有sink
        logger.remove()

        # 重新配置控制台和文件日志
        if enable_console is not False:
            self._setup_console_logging()
        if enable_file is not False:
            self._setup_file_logging(self._retention_days, self._error_retention_days)

# 初始化默认实例
_default_logger = _Logger()

# 将日志方法绑定到模块级别
trace = _default_logger.trace
debug = _default_logger.debug
info = _default_logger.info
warning = _default_logger.warning
error = _default_logger.error
critical = _default_logger.critical
update_config = _default_logger.update_config

def get_logger(app_name: str,
               log_dir: str = "logs",
               retention_days: int = 7,
               error_retention_days: int = 30,
               enable_console: bool = True,
               enable_file: bool = True,
               debug_mode: bool = False):
    """获取指定应用的日志实例"""
    return _Logger(
        app_name=app_name,
        log_dir=log_dir,
        retention_days=retention_days,
        error_retention_days=error_retention_days,
        enable_console=enable_console,
        enable_file=enable_file,
        debug_mode=debug_mode
    )

