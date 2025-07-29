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
import zipfile
import py7zr
import shutil
import os

__all__ = ["quick_compress","quick_extract","get_archive_filenames"]

def _get_extname(name:str|Path) -> str :
    txt = name if isinstance(name, str) else name.name
    return txt.split(".")[-1]

def quick_compress(src:str|Path, dst:str|Path|None = None, 
                   filename:str|None = None, 
                   mode:str = '7z', password:str|None = None, 
                   keep_data:bool = True) -> None :
    if dst is None :
        dst = Path(src).parent
    else :
        dst = Path(dst)
    src = Path(src)
    if filename is None :
        if dst.is_file() :
            filename = dst.with_suffix('.{}'.format(mode))
        else :
            filename = dst/(src.name + '.{}'.format(mode))
    else :
        if dst.is_dir() :
            filename = (dst/filename).with_suffix('.{}'.format(mode))
        else :
            raise ValueError("dst must be a directory!")
    if mode == "7z" :
        with py7zr.SevenZipFile(filename, 'w', dereference=True, 
                                header_encryption = True if password else False, 
                                password = password) as archive:
            if src.is_dir() :
                archive.writeall(src, arcname=src.name)
            else :
                archive.write(src, arcname=src.name)
    elif mode == "zip" :
        print("`zip` mode does not support encryption compression packaging!\n\n")
        with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_BZIP2,
                             compresslevel = 9) as archive:
            if src.is_dir() :
                for xfi in src.glob('**/*.*'):
                    archive.write(xfi, arcname=xfi.relative_to(src))
            else :
                archive.write(src, arcname=xfi.relative_to(src))
    else :
        raise ValueError("mode must be in ['7z','zip']")
    if not keep_data :
        try :
            os.remove(src)
        except :
            shutil.rmtree(src)

def quick_extract(src:str|Path, dst:str|Path|None = None,
                  password:str|None = None, 
                  keep_data:bool = True) -> None :
    mode = _get_extname(src)
    if dst is None :
        dst = Path(src).parent
    if mode == '7z' :
        with py7zr.SevenZipFile(src, 'r',
                                password = password) as archive:
            archive.extractall(path=dst)
    else:
        with zipfile.ZipFile(src, 'r') as archive:
            archive.extractall(path=dst, pwd=password)
    if not keep_data :
        try :
            os.remove(src)
        except :
            shutil.rmtree(src)

def get_archive_filenames(src:str|Path, 
                          password:str|None = None) -> list[str] :
        """
        获取压缩包内的文件列表。
        src:源文件路径。
        """
        mode = _get_extname(src)
        if mode == '7z' :
            with py7zr.SevenZipFile(src, 'r',
                                    password = password) as archive:
                return archive.getnames()
        else:
            with zipfile.ZipFile(src, 'r') as archive:
                if password :
                    archive.setpassword(password)
                return archive.namelist()