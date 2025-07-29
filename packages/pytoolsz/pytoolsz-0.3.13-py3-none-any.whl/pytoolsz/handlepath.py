#  ____       _____           _
# |  _ \ _   |_   _|__   ___ | |___ ____
# | |_) | | | || |/ _ \ / _ \| / __|_  /
# |  __/| |_| || | (_) | (_) | \__ \/ /
# |_|    \__, ||_|\___/ \___/|_|___/___|
#        |___/

# Copyright (c) 2024 Sidney Zhang <zly@lyzhang.me>
# PyToolsz is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from pathlib import Path
from typing import Optional, List, Union

import pdfplumber
import sys

__all__ = [
    "checkFolders", "lastFile", "read_pdf_text", "find_latest_updated_directory"
]


def checkFolders(folders:str|Path|list[str|Path], 
                 mkdir:bool = True, output:bool = False) -> bool|list[bool]|None :
    """
    检查多个文件夹路径是否存在
    mkdir - 是否创建不存在的文件夹（默认创建）
    output - 是否输出检查结果（默认不输出）
    """
    if isinstance(folders, (str, Path)) :
        givefolders = [folders]
    else :
        givefolders = folders
    givefolders = [Path(x) for x in givefolders]
    res = [x.exists() for x in givefolders]
    if mkdir :
        for i in range(len(givefolders)) :
            if not res[i] :
                if givefolders[i] != Path("No Path") :
                    givefolders[i].mkdir(parents=True, exist_ok=True)
    if output :
        if len(res) == 1 :
            return res[0]
        else :
            return res

def lastFile(folder:str|Path, filename:str,
             last_:str = "mtime", mode:str = "desc") -> Path :
    """
    获取指定文件夹下的最后一个文件
    filename - 文件名或查找匹配的字符
    last_ - 排序方式，可选值为 : 
            "mtime"（修改时间）
            "createtime"（创建时间）
            "atime"（访问时间）
            "size"（文件大小）
    mode - 排序方式，可选值为 :
            "desc"（降序）
            "asc"（升序）
    """
    if mode not in ["desc", "asc"] :
        raise ValueError("mode must be one of {}".format(["desc", "asc"]))
    kfolder = Path(folder)
    findedfile = sorted(kfolder.glob(filename))
    if sys.version_info >= (3, 12) :
        fixlast = "birthtime" if last_ == "createtime" else last_
    else :
        fixlast = "ctime" if last_ == "createtime" else last_
    attname = "st_{}".format(fixlast)
    if len(findedfile) == 0 :
        return Path("No Path")
    checkList = [getattr(x.stat(), attname) for x in findedfile]
    if mode == "desc" :
        cKdata = checkList.index(max(checkList))
    else: 
        cKdata = checkList.index(min(checkList))
    return findedfile[cKdata]

def read_pdf_text(pdfPath:str|Path) -> list[str] :
    """
    以文本形式读取PDF内容
    """
    data = []
    with pdfplumber.open(Path(pdfPath)) as pdf :
        for page in pdf.pages:
                    txt = page.extract_text()
                    txt = txt.split('\n')
                    data.extend(txt)
    return data

def find_latest_updated_directory(
    target_dir: str,
    exclude_dirs: Optional[Union[List[str], str]] = None
) -> Optional[Path]:
    """
    在指定的目录下查找最新更新的子文件夹。

    Args:
        target_dir (str): 目标目录的路径。
        exclude_dirs (Optional[Union[List[str], str]]): 
            要排除的文件夹名称列表或单个文件夹名称。
            可以是字符串（单个目录名）或字符串列表（多个目录名）。
            默认为None，表示不排除任何目录。

    Returns:
        Optional[Path]: 最新更新的文件夹的Path对象，如果不存在子文件夹则返回None。

    Raises:
        FileNotFoundError: 当目标目录不存在时引发。
        NotADirectoryError: 当目标路径不是目录时引发。
    """
    target_path = Path(target_dir)
    # 检查目标路径是否存在且为目录
    if not target_path.exists():
        raise FileNotFoundError(f"目录不存在: {target_dir}")
    if not target_path.is_dir():
        raise NotADirectoryError(f"不是目录: {target_dir}")
    
    # 处理exclude_dirs参数
    if exclude_dirs is None:
        exclude_dirs = []
    elif isinstance(exclude_dirs, str):
        exclude_dirs = [exclude_dirs]
    
    # 获取所有直接子目录（排除符号链接和要排除的目录）
    subdirs = [
        d for d in target_path.iterdir() 
        if (d.is_dir() and 
            not d.is_symlink() and 
            d.name not in exclude_dirs)
    ]
    
    if not subdirs:
        return None
    
    # 找到最后修改的子目录
    latest_subdir = max(subdirs, key=lambda x: x.stat().st_mtime)
    return latest_subdir