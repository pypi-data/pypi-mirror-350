#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/21 22:36:27

import os
import sys
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


def get_pip_conf_path():
    """获取pip配置文件路径"""

    new_path = (Path.home() / '.config' / 'pip' / 'pip.conf').expanduser()
    if new_path.exists():
        return new_path
    else:
        new_path = (Path.home() / '.pip' / 'pip.conf').expanduser()
        return new_path


def get_pypi_conf_path():
    """获取PyPI配置文件路径"""
    
    new_path = (Path.home() / '.pypirc').expanduser()
    return new_path


def get_vim_conf_path():
    """获取Vim配置文件路径"""

    new_path = (Path.home() / ".vimrc").expanduser()
    return new_path

