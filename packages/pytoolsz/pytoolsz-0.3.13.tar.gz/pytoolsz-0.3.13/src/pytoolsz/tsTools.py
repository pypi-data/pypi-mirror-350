#  ____       _____           _
# |  _ \ _   |_   _|__   ___ | |___ ____
# | |_) | | | || |/ _ \ / _ \| / __|_  /
# |  __/| |_| || | (_) | (_) | \__ \/ /
# |_|    \__, ||_|\___/ \___/|_|___/___|
#        |___/
#
# Copyright (c) 2024 Sidney Zhang <zly@lyzhang.me>
# PyToolsz is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

# 用来处理时间序列的相关工具
# 1. 时间序列数据框
# 2. 简单的时间数据计算

import pandas as pd
import polars as pl
import numpy as np

import matplotlib.pyplot as plt

from typing import Self
from collections.abc import Iterable
from pytoolsz.frame import szDataFrame
from pytoolsz.utils import isSubset

from pmdarima.model_selection import train_test_split

__all__ = ["tsFrame"]

class tsFrame(object):
    def __init__(self, data:pl.DataFrame|pd.DataFrame|szDataFrame,
                 dt:str|Iterable, variable:str, 
                 covariates:str|Iterable[str]|None = None) -> None:
        self.__data = data if isinstance(data, szDataFrame) else szDataFrame(from_data=data)
        self.__data = self.__data.to_polars()
        if dt in self.__data.columns:
            self.__dt = dt
            self.__data = self.__data.with_column(pl.col(dt).cast(pl.Date)).sort(self.__dt)
        else:
            raise ValueError(f"{dt} is not a column in data")
        if variable in self.__data.columns:
            self.__y = variable
        else:
            raise ValueError(f"{variable} is not a column in data")
        if isinstance(covariates, str) :
            if covariates in self.__data.columns :
                self.__variables = [covariates]
            else :
                raise ValueError(f"{covariates} is not a column in data")
        elif isSubset(self.__data.columns, covariates) :
            self.__variables = covariates
        elif covariates is None :
            self.__variables = None
        else :
            raise ValueError(f"{covariates} is not a subset of data-columns")
    def for_prophet(self, cap:str|Iterable|float|None = None, 
                    floor:str|Iterable|float|None = None) -> pd.DataFrame :
        if cap is None and floor is None :
            res = self.__data.select([self.__dt, self.__y]).to_pandas()
            res.columns = ["ds","y"]
        if cap is not None and floor is None :
            if isinstance(cap, str) :
                res = self.__data.select([self.__dt, self.__y, cap]).to_pandas()
                res.columns = ["ds","y","cap"]
            else :
                res = self.__data.select([self.__dt, self.__y]).to_pandas()
                res["cap"] = cap
        if cap is not None and floor is not None :
            if isinstance(cap, str) and isinstance(floor, str) :
                res = self.__data.select([self.__dt, self.__y, cap, floor]).to_pandas()
                res.columns = ["ds","y","cap","floor"]
            else :
                res = self.__data.select([self.__dt, self.__y]).to_pandas()
                res["cap"] = cap
                res["floor"] = floor
        if cap is None and floor is not None :
            raise ValueError("floor must be None when cap is not None")
        return res
    def for_auto_arima(self) -> np.ndarray|tuple[np.ndarray] :
        if self.__variables :
            Xres = self.__data.select(pl.col(self.__variables)).to_numpy()
            return self.__data[self.__y].to_numpy(), Xres
        else:
            return self.__data[self.__y].to_numpy(), None
    def getFreq(self) -> str :
        res = pd.infer_freq(self.__data[self.__dt].to_pandas())
        return res
    def make_future_dataframe(self, n_periods:int = 10, 
                              include_history:bool = False,
                              frequency:str|None = None,
                              keep_name:str|bool = False) -> pd.DataFrame :
        if frequency is None:
            freq = self.getFreq()
        else :
            freq = frequency
        last_date = self.__data[self.__dt].max()
        dates = pd.date_range(
            start=last_date,
            periods=n_periods + 1,
            freq=freq)
        dates = dates[dates > last_date]
        dates = dates[:n_periods]
        if include_history:
            dates = np.concatenate((np.array(self.__data[self.__dt].to_list()), dates))
        if keep_name :
            xname = self.__dt if isinstance(keep_name, bool) else keep_name
        else :
            xname = "ds"
        return pd.DataFrame({xname: dates})
    def plot(self, to_show:bool = True) -> None :
        self.__data.plot(x=self.__dt, y=self.__y)
        if to_show :
            plt.show()
    def to_polars(self) -> pl.DataFrame :
        return self.__data
    def to_pandas(self) -> pd.DataFrame :
        return self.__data.to_pandas()
    def __repr__(self) -> str :
        if self.__variables :
            return f"tsFrame(\n\tdata{self.__data.shape}, \n\tdt={self.__dt}, \n\ty={self.__y}, \n\tvariables={self.__variables}\n)"
        else :
            return f"tsFrame(\n\tdata{self.__data.shape}, \n\tdt={self.__dt}, \n\ty={self.__y}\n)"
    def train_test_split(self, test_size:float|int|None = None, 
                         train_size:float|int|None = None) -> tuple[Self, Self] :
        trainp,testp = train_test_split(self.__data, test_size, train_size)
        trainp = tsFrame(trainp, self.__dt, self.__y, self.__variables)
        testp = tsFrame(testp, self.__dt, self.__y, self.__variables)
        return trainp, testp
        