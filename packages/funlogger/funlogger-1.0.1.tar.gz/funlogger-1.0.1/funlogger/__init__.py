#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2025 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import logging
import os
import re
import sys
import threading
import weakref
from logging.handlers import RotatingFileHandler

from colorama import Fore, Style, init

from funlogger.config import config


class Singleton(type):
    """单例模式"""

    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Singleton.__instance = None
        # 初始化存放实例地址
        self._cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        # 提取类初始化时的参数
        kargs = "".join([f"{key}" for key in args]) if args else ""
        kkwargs = "".join([f"{key}" for key in kwargs]) if kwargs else ""
        # 判断相同参数的实例师否被创建
        if kargs + kkwargs not in self._cache:  # 存在则从内存地址中取实例
            with Singleton._instance_lock:
                Singleton.__instance = super().__call__(*args, **kwargs)
                self._cache[kargs + kkwargs] = Singleton.__instance
        # 不存在则新建实例
        else:
            Singleton.__instance = self._cache[kargs + kkwargs]
        return Singleton.__instance


class logger(metaclass=Singleton):
    def __init__(self):
        logger._custom_tag = config.TAG
        logging.root.handlers = []
        level = config.LOG_LEVEL
        log_name = config.LOG_FILE_NAME
        log_path = config.LOG_FILE_PATH
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logfile = os.path.join(log_path, log_name)

        try:
            self.ip_end = re.findall(r"\d+.\d+.\d+.(\d+)", f"{config.HOST_IP}")[0]
            self.ip_flag = f"-{self.ip_end}"
        except IndexError:
            self.ip_flag = ""
        self.sys_arch = config.SYS_ARCH
        self.date_format = "%m/%d %H:%M:%S"
        self.log_format = (
            f"{self.sys_arch}{self.ip_flag}: "
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        self.logger.addFilter(IgnoreFilter())

        _fh = RotatingFileHandler(
           logfile,
           mode="a+",
           maxBytes=10*1024*1024,  # 每个日志文件最大 10MB
           backupCount=5  # 保留 5 个备份文件
       )
        _fh.setLevel(logging.DEBUG)
        _fh.addFilter(IgnoreFilter())
        _fh.setFormatter(
            logging.Formatter(self.log_format, datefmt=self.date_format)
        )
        self.logger.addHandler(_fh)

        _ch = logging.StreamHandler(sys.stdout)
        _ch.setLevel(level)
        _ch.addFilter(IgnoreFilter())
        formatter = _ColoredFormatter(
            f"{Fore.GREEN}{self.sys_arch}{self.ip_flag}: {Style.RESET_ALL}"
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt=f"{Fore.RED}{self.date_format}{Style.RESET_ALL}",
        )
        _ch.setFormatter(formatter)
        self.logger.addHandler(_ch)


    @staticmethod
    def _build_prefix(autoadd=True):
        """
        构建日志前缀，格式为 [<custom_tag>][文件名][函数名]

        Args:
            autoadd (bool): 是否添加文件名和函数名，默认为 True

        Returns:
            str: 格式化的前缀
        """
        prefix = f"[{logger._custom_tag}]" if logger._custom_tag else ""
        if autoadd:
            current_frame = sys._getframe(2) if hasattr(sys, "_getframe") else None  # 调整为 sys._getframe(2)
            if current_frame:
                file_name = os.path.basename(current_frame.f_code.co_filename)
                func_name = current_frame.f_code.co_name
                prefix += f"[{file_name}][{func_name}]"
            else:
                prefix += "[unknown][unknown]"
        return prefix

    @staticmethod
    def info(message, autoadd=True):
        """记录 INFO 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        logging.info(formatted_message)

    @staticmethod
    def debug(message, autoadd=True):
        """记录 DEBUG 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        try:
            current_frame1 = sys._getframe(2) if hasattr(sys, "_getframe") else None
            if current_frame1 and current_frame1.f_code.co_name.startswith("test_"):
                logging.info(formatted_message)
            else:
                logging.debug(formatted_message)
        except ValueError:
            logging.debug(formatted_message)

    @staticmethod
    def error(message, autoadd=True):
        """记录 ERROR 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        logging.error(formatted_message)

    @staticmethod
    def warning(message, autoadd=True):
        """记录 WARNING 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        logging.warning(formatted_message)


init(autoreset=True) 

class _ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        "INFO": Fore.WHITE,
        "DEBUG": Fore.BLUE,
        "ERROR": Fore.RED,
        "WARNING": Fore.YELLOW
    }

    def formatMessage(self, record: logging.LogRecord) -> str:
        clean_message = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', record.message)
        level_color = self.LEVEL_COLORS.get(record.levelname, Fore.WHITE)
        lines = clean_message.splitlines()
        colored_lines = []
        for line in lines:
            prefix_match = re.match(r'(\[[^\]]+\])(\[[^\]]+\])(\[[^\]]+\])(.*)', line)
            if prefix_match:
                custom_tag, file_name, func_name, content = prefix_match.groups()
                colored_line = (
                    f"{Fore.GREEN}{custom_tag}{Style.RESET_ALL}"
                    f"{Fore.CYAN}{file_name}{Style.RESET_ALL}"
                    f"{Fore.CYAN}{func_name}{Style.RESET_ALL}"
                    f"{level_color}{content}{Style.RESET_ALL}"
                )
            else:
                colored_line = f"{level_color}{line}{Style.RESET_ALL}"
            colored_lines.append(colored_line)
        colored_message = "\n".join(colored_lines)
        colored_level = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        record.message = colored_message
        record.levelname = colored_level
        return super().formatMessage(record)
    

class IgnoreFilter(logging.Filter):
    """IgnoreFilter"""
    
    def filter(self, record):
        ignored_prefixes = (
            'urllib3',
            'paramiko',
            'PIL',              # 图像库相关
            'pyscreenshot',     # 截图相关
            'scrot',
            'imageio',
            'easyprocess',
        )
        return not record.name.startswith(ignored_prefixes)

