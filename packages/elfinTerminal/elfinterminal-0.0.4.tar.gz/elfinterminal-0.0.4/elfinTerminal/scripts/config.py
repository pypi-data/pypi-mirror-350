#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/22 21:52:19

import argparse


def pip_set_args(subparser):
    pip_config = subparser.add_parser("pip", help="pip configuration")


def vim_set_args(subparser):
    vim_config = subparser.add_parser("vim", help="vim configuration")


def pypi_set_args(subparser):
    pypi_config = subparser.add_parser("pypi", help="pypi configuration")
    pypi_config.add_argument("--config", default="token", help="pypi配置项")

def set_args():
    terminal_parser = argparse.ArgumentParser(
        description='系统控制小工具🔧',
        epilog='Enjoy your life with elfinTerminal!😊',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    terminal_parser.add_argument("--mode", help="Sub-command mode")
    subparsers = terminal_parser.add_subparsers(dest="mode", title="Sub-commands")

    pip_set_args(subparsers)
    vim_set_args(subparsers)
    pypi_set_args(subparsers)

    args = terminal_parser.parse_args()
    return args
