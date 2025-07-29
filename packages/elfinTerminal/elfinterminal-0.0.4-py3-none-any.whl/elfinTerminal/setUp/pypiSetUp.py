#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/23 22:09:33
# @desc: 设置PYPI相关使用配置

import configparser
from getpass import getpass
from pathlib import Path
from elfinTerminal.tools.pathSearch import get_pypi_conf_path


def set_pypi_token():
    """
    设置PYPI相关使用配置
    :return:
    """
    pypi_conf_path = get_pypi_conf_path()
    change_token = True
    if Path(pypi_conf_path).exists():
        change_token = False
        
        for _ in range(3):
            status = input(f"检测到{pypi_conf_path}文件, 是否需要重新设置PYPI相关配置?([y]/n)")
            if status.lower() == 'y' or status.lower() == 'yes' or status == '':
                change_token = True
                break
            elif status.lower() == 'n' or status.lower() == 'no':
                return None
            else:
                print("输入有误, 请重新输入.")
    
    if not change_token:
        return None
    
    print("正在设置PYPI相关配置...")
    token = getpass("请输入PYPI Token: ")
    config_parser = configparser.ConfigParser()
    config_parser.read(pypi_conf_path)
    config_parser["pypi"] = {
        "username": "__token__",
        "password": token,
    }
    with open(pypi_conf_path, 'w') as f:
        config_parser.write(f)
