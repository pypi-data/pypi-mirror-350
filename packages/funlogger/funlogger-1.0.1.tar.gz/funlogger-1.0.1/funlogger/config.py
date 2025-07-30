#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2025 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import os
from getpass import getuser
from platform import machine


class _Setting:

    SYS_ARCH = machine()
    USERNAME = getuser()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # 日志文件生成的路径
    LOG_FILE_PATH = os.path.join("/tmp", "logs")
    LOG_FILE_NAME = "test.log"
    # 本机IP
    HOST_IP = str(os.popen("hostname -I |awk '{print $1}'").read()).strip("\n").strip()
    TAG = None

    LOG_LEVEL = "DEBUG"
    CLASS_NAME_STARTSWITH: list = []
    CLASS_NAME_ENDSWITH: list = []
    CLASS_NAME_CONTAIN: list = []

config = _Setting()