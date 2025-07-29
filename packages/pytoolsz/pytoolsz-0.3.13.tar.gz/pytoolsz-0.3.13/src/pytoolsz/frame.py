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

import pandas as pd
import polars as pl
from zipfile import ZipFile
from os import stat_result
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Self
from rich import print

from pmdarima.model_selection import train_test_split

__all__ = ["getreader","read_tsv","checkExpr","dataframeColumns",
           "just_load","szDataFrame","zipreader"]

def read_tsv(filepath:Path, **kwgs) -> pl.DataFrame:
    with open(filepath, 'r', encoding="utf-8") as file:
        first_line = file.readline()
    lenCols = len(first_line.split("\t"))
    akwgs = {
        "separator":"\t",
        "quote_char":None,
        "schema_overrides":[pl.Utf8]*lenCols,
    }
    akwgs.update(kwgs)
    return pl.read_csv(filepath, **akwgs)

def getreader(dirfile:Path|str, used_by:str|None = None):
    if used_by is None :
        fna = Path(dirfile).suffix
        if fna in [".xls",".xlsx"]:
            return pl.read_excel
        elif fna == ".tsv":
            return read_tsv
        else:
            return getattr(pl, "read_{}".format(fna), pl.read_csv)
    else:
        return getattr(pl, "read_{}".format(used_by))

def dataframeColumns(data:str|Path|pl.DataFrame|pd.DataFrame) -> list[str] :
    if isinstance(data, (str, Path)) :
        tcols = getreader(data)(data).columns
    else :
        tcols = data.columns
    return tcols

def checkExpr(ziel:pl.Expr|list[pl.Expr], 
              indata:str|Path|pl.DataFrame|pd.DataFrame,
              by_:str = "all") -> bool :
    tcols = dataframeColumns(indata)
    res = []
    if isinstance(ziel, list) :
        for xExpr in ziel :
            tmp = []
            for i in xExpr.meta.root_names() :
                tmp.append(i in tcols)
            res.append(all(tmp))
        if by_ == "all" :
            res = all(res)
        elif by_ == "any" :
            res = any(res)
        else :
            raise ValueError("by_ only support `any` and `all` !")
    else :
        for i in ziel.meta.root_names() :
            res.append(i in tcols)
        res = all(res)
    return res

def optExpr(ziel:pl.Expr|list[pl.Expr], 
            indata:str|Path|pl.DataFrame|pd.DataFrame
            ) -> pl.Expr|list[pl.Expr]|None :
    if checkExpr(ziel, indata, by_="any") :
        tcols = dataframeColumns(indata)
        res = []
        if isinstance(ziel, list) :
            for xExpr in ziel :
                tmp = []
                for i in xExpr.meta.root_names() :
                    tmp.append(i in tcols)
                if all(tmp) :
                    res.append(xExpr)
        else :
            res = ziel
        return res
    else :
        return None

def just_load(filepath:str|Path, engine:str = "polars", 
              transtype:pl.Expr|list[pl.Expr]|None = None,
              used_by:str|None = None, **kwgs) -> pl.DataFrame|pd.DataFrame:
    """load file to DataFrame"""
    if filepath != Path("No Path") :
        rFunc = getreader(filepath, used_by)
        res = rFunc(Path(filepath), **kwgs)
    else:
        res = pl.DataFrame()
    if engine not in ["polars","pandas"]:
        raise ValueError("engine must be one of {}".format(["polars","pandas"]))
    else:
        if transtype is None :
            return res.to_pandas() if engine == "pandas" else res
        else :
            if checkExpr(transtype, filepath) :
                if isinstance(transtype, list) :
                    res = res.with_columns(*transtype)
                else :
                    res = res.with_columns(transtype)
                return res.to_pandas() if engine == "pandas" else res
            else :
                raise ValueError("Column Not Found Error !")

class szDataFrame(object):
    """
    简单的数据处理。不提供超大数据集的惰性加载。
    提供常见的数据处理方法，包括：
    1. 时间序列处理
    2. 训练/测试数据处理
    3. 数据转换
    """
    __ENGINES = ["polars","pandas"]
    def __init__(self, filepath:str|None, engine:str = "polars", 
                 from_data:pl.DataFrame|pd.DataFrame|None = None, **kwgs) -> None:
        if engine not in szDataFrame.__ENGINES:
            raise ValueError("engine must be one of {}".format(szDataFrame.__ENGINES))
        if from_data is None :
            self.__data = just_load(filepath, engine, **kwgs)
        else:
            if isinstance(from_data, pl.DataFrame):
                self.__data = from_data
            else:
                self.__data = pl.from_pandas(from_data)
        self.__filepath = Path(filepath) if filepath else None
    def __repr__(self) -> str:
        return self.__data.__repr__()
    def __str__(self) -> str:
        return self.__data.__str__()
    def __len__(self) -> int:
        return len(self.__data)
    @property
    def shape(self) -> tuple:
        return self.__data.shape
    @property
    def columns(self) -> list:
        return self.__data.columns
    @property
    def stat(self) -> stat_result|None:
        if self.__filepath is None:
            res = None
        else :
            res = self.__filepath.stat()
        return res
    def get(self, type:str = "polars") -> pl.DataFrame|pd.DataFrame:
        if type not in szDataFrame.__ENGINES:
            raise ValueError("type must be one of {}".format(szDataFrame.__ENGINES))
        return self.__data if type == "polars" else self.__data.to_pandas()
    def convert(self, to:str) -> any:
        funx = getattr(self.__data, "to_{}".format(to), None)
        if to == "polars" :
            return self.__data
        if funx is None:
            raise ValueError("Don't have this convert method!")
        return funx()
    def append(self, other:Self) -> Self:
        data = self.__data.vstack(other.get())
        return szDataFrame(filepath=self.__filepath, from_data=data)
    def train_test_split(self, test_size:float|int|None = None, 
                         train_size:float|int|None = None) -> tuple[Self, Self]:
        train, test = train_test_split(self.__data, test_size, train_size)
        return szDataFrame(filepath=self.__filepath, from_data=train), \
               szDataFrame(filepath=self.__filepath, from_data=test)


def zipreader(zipFilepath:Path|str, subFile:str, 
              transtype:pl.Expr|list[pl.Expr]|None = None, **kwgs) -> szDataFrame:
    with TemporaryDirectory() as tmpdirname:
        with ZipFile(Path(zipFilepath), "r") as teZip:
            teZip.extractall(path = tmpdirname)
            subFiles = teZip.namelist()
        if subFile not in subFiles:
            raise ValueError("'{}' not in zip-file({})!".format(subFile,zipFilepath))
        return szDataFrame(Path(tmpdirname)/subFile, transtype = transtype, **kwgs)

if __name__ == "__main__":
    rootpath = Path(__file__).absolute().parent.parent
    data = zipreader(rootpath/"datasets/iris/iris.zip",
                     "iris.data", has_header = False)
    print(data.convert("pandas"))