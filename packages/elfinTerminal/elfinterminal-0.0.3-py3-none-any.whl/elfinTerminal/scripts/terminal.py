#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/22 21:51:33

from elfinTerminal.scripts.config import set_args
from elfinTerminal.setUp.pipSetUp import set_pip_source
from elfinTerminal.setUp.pypiSetUp import set_pypi_token


def elfin_terminal():
    args = set_args()
    if args.mode == "pip":
        set_pip_source()
    elif args.mode == "pypi":
        if args.config == "token":
            set_pypi_token()
    else:
        print("Invalid sub-command mode")


if __name__ == '__main__':
    elfin_terminal()