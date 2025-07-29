#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/24 11:15:09
# @desc: This file is used to set up vim environment.

import re
import os
from pprint import pp
from elfinTerminal.tools.pathSearch import get_vim_conf_path
from elfinTerminal.source.config import VIMRC_CONTENT


def set_vim_config():
    vim_conf_path = get_vim_conf_path()
    if vim_conf_path.exists():
        change = input(f"The vim configuration file {vim_conf_path} already exists, do you want to overwrite it? (y/n) ")
        if change.lower() != 'y':
            return None
    
    vimrc_dict = dict()
    with open(vim_conf_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line and line.startswith('"'):  # 忽略空行和注释
                continue
            if match := re.match(r'^\s*set\s+(\w+)=?(\S*)', line):
                key, value = match.groups()
                vimrc_dict[key] = value

    vimrc_dict.update(VIMRC_CONTENT)
    # 获取系统换行符号
    sys_sep = os.linesep
    with open(vim_conf_path, 'w') as f:
        for k, v in vimrc_dict.items():
            write_line = f'set {k}={v}{sys_sep}' if v else f'set {k}{sys_sep}'
            f.write(write_line)
    print(f"The vim configuration file {vim_conf_path} has been set up successfully. settings:")
    pp(vimrc_dict)



if __name__ == '__main__':
    set_vim_config()
