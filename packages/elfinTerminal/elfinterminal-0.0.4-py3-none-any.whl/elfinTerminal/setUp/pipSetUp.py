#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/21 22:44:20

import os
import sys
import warnings
import configparser
from pathlib import Path
from loguru import logger
from prettytable import PrettyTable
warnings.filterwarnings('ignore')
FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


from elfinTerminal.source.config import PIP_SOURCES
from elfinTerminal.tools.pathSearch import get_pip_conf_path


def set_pip_source():
    """设置pip源"""

    source_table = PrettyTable(['序号', '名称', '源地址'])
    for i, source_obj in PIP_SOURCES.items():
        source_table.add_row([i, source_obj['name'], source_obj['index-url']])
    source_table.align['名称'] = 'l'
    source_table.align['源地址'] = 'l'
    print(source_table)
    selected_index = input("请输入源序号: ")
    selected_dict = PIP_SOURCES.get(int(selected_index), None)
    if selected_dict is None:
        raise ValueError(f"未知的源序号: {selected_index}")
    
    conf_path = get_pip_conf_path()
    print(f"pip配置文件路径: {conf_path}")
    config_parser = configparser.ConfigParser()
    config_parser.read(conf_path)
    config_parser["global"] = {
        "timeout": "6000",
        "index-url": selected_dict['index-url'],
        "trusted-host": selected_dict['trusted-host'],
    }
    
    with open(conf_path, 'w') as f:
        config_parser.write(f)
    
    print(f"已设置pip源为:{selected_dict['name']} --> ({selected_dict['index-url']})")
