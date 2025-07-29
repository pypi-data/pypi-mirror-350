#!/usr/bin/env python3
# encoding: utf-8
# @author: firstelfin
# @time: 2025/05/21 22:33:44


# 预定义的pip源
PIP_SOURCES = {
    0: {'name': '阿里云(aliyun)',
        'index-url': 'http://mirrors.aliyun.com/pypi/simple/',
        'trusted-host': 'mirrors.aliyun.com'},
    1: {'name': '中国科技大学(ustc)',
        'index-url': 'https://pypi.mirrors.ustc.edu.cn/simple/',
        'trusted-host': 'pypi.mirrors.ustc.edu.cn'},
    2: {'name': '豆瓣(douban)',
        'index-url': 'https://pypi.doubanio.com/simple/',
        'trusted-host': 'pypi.doubanio.com'},
    3: {'name': '清华大学(tsinghua)',
        'index-url': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'trusted-host': 'pypi.tuna.tsinghua.edu.cn'},
    4: {'name': '腾讯云(tencent)',
        'index-url': 'https://mirrors.cloud.tencent.com/pypi/simple/',
        'trusted-host': 'mirrors.cloud.tencent.com'},
    5: {'name': '浙江大学(zju)',
        'index-url': 'http://mirrors.zju.edu.cn/pypi/web/simple/',
        'trusted-host': 'mirrors.zju.edu.cn'},
    6: {'name': '网易(163)',
        'index-url': 'http://mirrors.163.com/pypi/simple/',
        'trusted-host': 'mirrors.163.com'},
    7: {'name': '华为云(huawei)',
        'index-url': 'https://repo.huaweicloud.com/repository/pypi/simple',
        'trusted-host': 'repo.huaweicloud.com'},
    8: {'name': '北京外国语大学(bfsu)',
        'index-url': 'https://mirrors.bfsu.edu.cn/pypi/web/simple/',
        'trusted-host': 'mirrors.bfsu.edu.cn'},
    9: {'name': '上海交通大学(sjtug)',
        'index-url': 'https://mirrors.sjtug.sjtu.edu.cn/pypi/web/simple',
        'trusted-host': 'mirrors.sjtug.sjtu.edu.cn'},
    10: {'name': '南京大学(nju)',
        'index-url': 'https://mirrors.nju.edu.cn/pypi/web/simple/',
        'trusted-host': 'mirrors.nju.edu.cn'}
}


VIMRC_CONTENT = {
    "number": "",  # "显示行号"
    "relativenumber": "",  #: "显示相对行号(方便跳转)"
    "cursorline": "",  #: "高亮当前行"
    "showcmd": "",  #: "显示当前输入的命令"
    "wildmenu": "",  #: "命令补全提示"
    "tabstop": 4,  #: "Tab显示为4空格"
    "shiftwidth": 4,  #: "自动缩进宽度"
    "expandtab": "",  #: "Tab转空格"
    "autoindent": "",  #: "自动缩进"
    "hlsearch": "",  #: "高亮搜索结果"
    "ignorecase": "",  #: "忽略大小写"
    "smartcase": "",  #: "智能大小写(有大写时区分)"
    "backspace": "indent,eol,start",  #: "允许退格键删除更多"
    "mouse": "a",  #: "启用鼠标支持"
    "syntax": "on",  #: "语法高亮"
    "clipboard": "unnamed",  #: "共享系统剪贴板,需Vim支持"
    "encoding": "utf-8",  #: "编辑器编码为UTF-8"
    "fileencodings": "utf-8,ucs-bom,gb18030,gbk,gb2312,cp936",  #: "文件编码"
}


if __name__ == '__main__':
    import os
    # from pprint import pp
    # res = dict()
    # for i, j, k in zip(PIP_SOURCES[0], PIP_SOURCES[1], PIP_SOURCES[2]):
    #     k_id, k_name = k.split("-")
    #     res[int(k_id)] = {
    #         "name": k_name,
    #         "index-url": i,
    #         "trusted-host": j
    #     }
    # pp(res)
    from pathlib import Path
    print(Path.home())
    a = (Path.home() / ".vimrc").expanduser()
    print(a)
