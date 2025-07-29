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
    
    if os.name == 'posix':  # Unix/Linux/Mac
        new_path = Path.home() / '.config' / 'pip' / 'pip.conf'
        if new_path.exists():
            return new_path
        else:
            return Path.home() / '.pip' / 'pip.conf'
    else:
        # return Path(os.environ.get('APPDATA')) / 'pip' / 'pip.ini'
        raise NotImplementedError('暂不支持该系统')


def get_pypi_conf_path():
    """获取PyPI配置文件路径"""
    
    if os.name == 'posix':  # Unix/Linux/Mac
        new_path = Path.home() / '.pypirc'
    else:
        # new_path = Path.home() / '.pypirc'
        raise NotImplementedError('暂不支持该系统')
    return new_path