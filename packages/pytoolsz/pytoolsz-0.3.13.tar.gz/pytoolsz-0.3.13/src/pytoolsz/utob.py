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
from pytoolsz.frame import szDataFrame,zipreader,optExpr
from pytoolsz.pretools import (
    quick_date,
    get_interval_dates, 
    near_date,
    last_date)
from collections.abc import Mapping,Iterable,Sequence
from polars._typing import (IntoExpr, PolarsDataType)
from pendulum import interval, DateTime

import re
import polars as pl
import pandas as pd
import polars.selectors as cs

__all__ = ["youtube_datetime","read_YouTube_zipdata","read_multiChannel"]

TARGETNAMES = ["频道","内容","流量来源","地理位置","观看者年龄","观看者性别","日期","收入来源",
              "订阅状态","订阅来源","内容类型","播放列表","设备类型","广告类型","交易类型",
              "YouTube 产品","播放位置","操作系统","字幕","视频信息语言","是否使用翻译",
              "片尾画面元素类型","片尾画面元素","卡片类型","卡片","分享服务","频道所有权",
              "版权声明状态","播放器类型","新观看者和回访观看者","资产","观看者年龄_观看者性别"]

DATANAMES = ["表格数据","图表数据","总计"]

COMPARENAME = "（比较对象）"

SUPPLEMENTAL = pl.from_dict(
    {
        "name_short": ["(未知)"],
        "name_official": ["(未知)"],
        "regex": ["(未知)"],
        "ISO2": ["ZZ"],
        "ISO3": [ "ZZZ"],
    }
)

def youtube_currentTime(unit:str = "month", bis_:str = "last",
                        single:bool = False,
                        to_string:bool|str = False
                        ) -> tuple[str]|tuple[DateTime]|str|DateTime:
    """
    常用YouTube统计周期的数据处理。还是针对YouTube导出数据的形式来确认。
    """
    if unit not in ["day","week","month","year"] :
        raise ValueError("unit = {} is not supported!".format(unit))
    if bis_ not in ["last","now"] :
        raise ValueError("The variable bis_ only supports the values 'last' and 'now'.")
    if bis_ == "last" :
        midres = last_date(last_=unit)
        midres = (midres[0],midres[1].add(days=1))
    else:
        midres = near_date(near_=unit, nth=0)
        if unit == "month" :
            midres = (midres[0],near_date(near_="day",nth=0)[1])
        elif unit == "year" :
            midres = (midres[0],last_date(last_="month")[1].add(days=1))
        else:
            midres = (midres[0],midres[1].add(days=1))
    if isinstance(to_string, str):
        sfm = to_string
    else:
        if unit == "year" :
            sfm = "%Y"
        elif unit == "month" :
            sfm = "%Y%m"
        elif unit == "week" :
            sfm = "%Y-%W"
        else :
            sfm = "%Y-%m-%d"
    if '%' in sfm :
        toSFun = (getattr(midres[0], "strftime"),
                  getattr(midres[1], "strftime"))
    else :
        toSFun = (getattr(midres[0], "format"),
                  getattr(midres[1], "format"))
    if single :
        return toSFun[0](sfm) if to_string else midres[0]
    else :
        return [f(sfm) for f in toSFun] if to_string else midres

def youtube_datetime(keydate:str, seq:str|None = None, daily:bool = False,
                     dateformat:str|None = None, in_USA:bool = False,
                     singleday_mode:str = "near") -> tuple[str]|list[tuple[str]]:
    """
    针对常见的YouTube时间数据需求进行处理。
    """
    tz = "America/Indianapolis" if in_USA else None
    if singleday_mode not in ["near", "near_week","near_month","near_year",
                              "last_month","last_season","last_year"]:
        raise ValueError("singleday_mode = {} is not supported!".format(singleday_mode))
    if seq is None :
        listDatas = quick_date(keydate,sformat=dateformat,tz=tz)
        is_month = True if re.match(r"^\d{4}[/-]?\d{2}$", keydate) else False
    else:
        listDatas = keydate.split(seq)
        listDatas = [quick_date(x,sformat=dateformat,tz=tz) for x in listDatas]
        is_month = [
            (True if re.match(r"^\d{4}[/-]?\d{2}$", x) else False)
            for x in keydate.split(seq)
        ]
    if daily :
        res = []
        if isinstance(is_month, bool) :
            tmp = get_interval_dates(listDatas.start_of("month"), 
                                     listDatas.end_of("month").add(days=1),
                                     gap = "1 days", limit_gap = True)
            res = [(x[0].format("YYYY-MM-DD"),x[1].format("YYYY-MM-DD"))
                   for x in tmp]
        else :
            dn = 0
            for i in range(len(is_month)) :
                if is_month[i] :
                    tmp = get_interval_dates(listDatas[i].start_of("month"), 
                                     listDatas[i].end_of("month").add(days=1),
                                     gap = "1 days", limit_gap = True)
                    res.extend([(x[0].format("YYYY-MM-DD"),x[1].format("YYYY-MM-DD")) 
                                for x in tmp])
                else :
                    if dn % 2 == 0 :
                        if i == len(is_month)-1 :
                            if "near" in singleday_mode :
                                type_m = "day" if singleday_mode == "near" else singleday_mode.split("_")[1]
                                ssd = near_date(keydate=listDatas[i],near_=type_m)
                            else :
                                type_m = singleday_mode.split("_")[1]
                                ssd = last_date(keydate=listDatas[i], last_=type_m)
                            tmp = get_interval_dates(ssd[0],ssd[1].add(days=1),
                                        gap = "1 days", limit_gap = True)
                        else:
                            tmp = get_interval_dates(listDatas[i].start_of("day"), 
                                        listDatas[i+1].end_of("day").add(days=1),
                                        gap = "1 days", limit_gap = True)
                        res.extend([(x[0].format("YYYY-MM-DD"),x[1].format("YYYY-MM-DD")) 
                                for x in tmp])
                        dn += 1
                    else :
                        if i == len(is_month) - 1 and dn > 2 :
                            if "near" in singleday_mode :
                                type_m = "day" if singleday_mode == "near" else singleday_mode.split("_")[1]
                                sgday = near_date(keydate=listDatas[i],near_=type_m)
                            else :
                                type_m = singleday_mode.split("_")[1]
                                sgday = last_date(keydate=listDatas[i], last_=type_m)
                            tmp = get_interval_dates(sgday[0],sgday[1].add(days=1), 
                                                     gap = "1 days", limit_gap = True)
                            res.extend([(x[0].format("YYYY-MM-DD"),x[1].format("YYYY-MM-DD")) 
                                for x in tmp])
                        else :
                            dn += 1
    else :
        if isinstance(is_month, bool) :
            if is_month :
                res = (listDatas.start_of("month"),
                       listDatas.end_of("month").add(days=1))
            else :
                if "near" in singleday_mode :
                    type_m = "day" if singleday_mode == "near" else singleday_mode.split("_")[1]
                    res = near_date(keydate=listDatas,near_=type_m)
                else :
                    type_m = singleday_mode.split("_")[1]
                    res = last_date(keydate=listDatas, last_=type_m)
                res = (res[0], res[1].add(days=1))
            res = (res[0].format("YYYY-MM-DD"),res[1].format("YYYY-MM-DD"))
        else :
            res = []
            dn = 0
            for i in range(len(is_month)) :
                if is_month[i] :
                    res.append((listDatas[i].start_of("month"),
                                listDatas[i].end_of("month").add(days=1)))
                else :
                    if dn % 2 == 0 :
                        if i == len(is_month)-1 :
                            if "near" in singleday_mode :
                                type_m = "day" if singleday_mode == "near" else singleday_mode.split("_")[1]
                                ssd = near_date(keydate=listDatas[i],near_=type_m)
                            else :
                                type_m = singleday_mode.split("_")[1]
                                ssd = last_date(keydate=listDatas[i], last_=type_m)
                            res.append((ssd[0], ssd[1].add(days=1)))
                        else:
                            res.append((listDatas[i],
                                        listDatas[i+1].add(days=1)))
                        dn += 1
                    else :
                        if i == len(is_month) - 1 and dn > 2:
                            if "near" in singleday_mode :
                                type_m = "day" if singleday_mode == "near" else singleday_mode.split("_")[1]
                                ssd = near_date(keydate=listDatas[i],near_=type_m)
                            else :
                                type_m = singleday_mode.split("_")[1]
                                ssd = last_date(keydate=listDatas[i], last_=type_m)
                            res.append((ssd[0], ssd[1].add(days=1)))
                        dn += 1
            res = [(x[0].format("YYYY-MM-DD"),x[1].format("YYYY-MM-DD")) for x in res]
    if isinstance(res, list) and len(res) == 1:
        res = res[0]
    return res

def read_YouTube_zipdata(tarName:str, between_date:list[str], channelName:str,
                           dataName:str, rootpath:Path|None = None, 
                           lastnum:bool|int = False,
                           compare:bool = False, 
                           transType:pl.Expr|list[pl.Expr]|None = None) -> szDataFrame:
    """
    读取下载的YouTube数据。
    通常YouTube数据下载后会被压缩到zip文件中，并包含多个数据csv文件。
    """
    if tarName not in TARGETNAMES :
        raise ValueError("This tarName is not supported!")
    if dataName not in DATANAMES :
        raise ValueError("This dataName must be in {}".format(DATANAMES))
    if isinstance(lastnum, bool) :
        plus_str = " (1)" if lastnum else ""
    else :
        plus_str = " ({})".format(lastnum)
    filelike = "{} {}_{} {}{}.zip".format(tarName,*between_date,channelName,plus_str)
    csvlike = "{}{}.csv".format(dataName,COMPARENAME if compare else "")
    homepath = Path(rootpath) if rootpath else Path(".").absolute()
    data = zipreader(homepath/filelike, csvlike)
    if transType is not None :
        optrans = optExpr(transType, data)
        if optrans is not None:
            data = zipreader(homepath/filelike, csvlike, transtype = optrans)
    return data

def read_multiChannel(tarName:str, between_date:list[str], channelNames:list[str],
                      dataName:str, lastnum:bool|int = False,
                      rootpath:Path|None = None,
                      compare:bool = False, 
                      group_by:str|Mapping[str,IntoExpr|Iterable[IntoExpr]|Mapping[str,IntoExpr]]|None = None,
                      convert:str = "polars",
                      schema_overrides: Mapping[str, PolarsDataType] | Sequence[PolarsDataType] | None = None,
                      transType:pl.Expr|list[pl.Expr]|None = None
                    ) -> pl.DataFrame|pd.DataFrame:

    data = []
    for chs in channelNames :
        data.append(read_YouTube_zipdata(tarName, between_date, chs,  
                                         dataName, rootpath, lastnum, compare, 
                                         transType=transType))
    data = [x.get() for x in data]
    if schema_overrides is not None :
        tmpData = []
        for xd in data :
            subdata = xd
            for ke,vd in schema_overrides.items() :
                if ke in xd.columns :
                    subdata = subdata.with_columns([pl.col(ke).cast(vd)])
            tmpData.append(subdata)
        data = tmpData
    if group_by is not None :
        if isinstance(group_by, str) :
            data = pl.concat(data).group_by(group_by).agg(cs.numeric().sum())
        else :
            data = pl.concat(data)
            for key,value in group_by.items() :
                if isinstance(value, Mapping):
                    data = data.group_by(key).agg(**value)
                elif isinstance(value, Iterable):
                    data = data.group_by(key).agg(*value)
                else :
                    data = data.group_by(key).agg(value)
    else :
        data = pl.concat(data)
    return data if convert == "polars" else data.to_pandas()


if __name__ == "__main__":
    print("Hi buddy!")

