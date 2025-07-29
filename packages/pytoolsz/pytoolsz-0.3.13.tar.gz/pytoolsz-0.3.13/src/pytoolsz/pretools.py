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

from pytoolsz.frame import just_load
from pathlib import Path
from numbers import Number
from decimal import Decimal,ROUND_HALF_UP
from collections.abc import Iterable
from thefuzz import process

import pendulum as pdl
import pycountry as pct
import pandas as pd
import numpy as np
import country_converter as coco
import gettext
import shutil
import re


__all__ = ["covert_macadress","convert_suffix","around_right","round",
           "local_name","convert_country_code","get_keydate",
           "quick_date","near_date","last_date","get_interval_dates",
           "getExcelSheets","lastDay","firstDay"]

def covert_macadress(macadress:str, upper:bool = True) -> str:
    """
    自适应的MAC地址转换方法。
    """
    sl = len(macadress)
    if sl == 12 :
        pattern = r"(\w{2})(\w{2})(\w{2})(\w{2})(\w{2})(\w{2})"
        res = re.sub(pattern, r"\1:\2:\3:\4:\5:\6", macadress)
    elif sl == 17 :
        res = macadress.split(":")
        res = "".join(res)
    else:
        raise ValueError("macadress must be 12 or 17 characters")
    return res.upper() if upper else res.lower()

def convert_suffix(file:str, to:str = "csv") -> None :
    """
    转换文件类型到对应文件类型
    """
    file_path = Path(file)
    data = just_load(file_path)
    if file_path.suffix == '.{}'.format(to) :
        raise ValueError("file is already in {} format".format(to))
    elif file_path.suffix == '.csv' and to == 'txt' :
        shutil.copy(file_path, file_path.with_suffix('.txt'))
    elif to in ["xls","xlsx"] :
        data.write_excel(file_path.with_suffix('.{}'.format(to)))
    else:
        func = getattr(data, "write_{}".format(to), data.write_csv)
        func(file_path.with_suffix('.'+to))
    print("converted successfully!")

def around_right(nums:Number|None, keep_n:int = 2, 
                 null_na_handle:bool|float = True,
                 precise:bool = True) :
    """
    用于更准确的四舍五入操作。
    对于None、Null或者NAN/NA等情况，可通过null_na_handle参数进行处理。
    默认不处理。
    通过null_na_handle参数也可以指定把这些转化为指定数值。
    通过precise参数，可以启用精准四舍五入计算。
    """
    if (nums is None) or (nums is np.nan):
        if isinstance(null_na_handle, bool) :
            tNum = np.float64(0.0) if null_na_handle else nums
            if (tNum is None) or (tNum is np.nan):
                return tNum
        else :
            tNum = np.float64(null_na_handle)
    elif nums is np.inf :
        return np.inf
    else :
        tNum = nums
    if precise :
        def decimal_round(tn:str, keep:int):
            return Decimal(tn).quantize(Decimal('0.'+'0'*keep), rounding=ROUND_HALF_UP)
        middleNum = decimal_round(str(tNum), keep_n+4)
        return np.float64(decimal_round(str(middleNum), keep_n))
    else :
        middleNum = np.around(tNum, decimals=(keep_n+4))
        return np.around(middleNum, decimals=keep_n)

def round(numbs:Iterable, n:int = 2,
          null_na_handle:bool|float = False) -> list[float] :
    res = [around_right(x, keep_n=n, 
                        null_na_handle=null_na_handle,
                        precise=True) for x in numbs]
    return res

def local_name(code:str, local:str = "zh", not_found:str|None = None ) -> str:
    """
    转换国家代码为指定语言的国家名称。
    """
    if code.upper() in ["XK","XKS"] :
        return "科索沃" if local=="zh" else "Kosovo"
    arg = {"alpha_2":code} if len(code) == 2 else {"alpha_3":code}
    contry = pct.countries.get(**arg)
    if contry is None :
        return (code if not_found is None else not_found)
    name = contry.name
    translator = gettext.translation('iso3166-1', pct.LOCALES_DIR, languages=[local])
    translator.install()
    res = translator.gettext(name)
    res = ("中国"+res) if res in ["香港","澳门"] else res
    res = (res + " ,China") if res in ["Macao","Hong Kong","Hongkong","Macau"] else res
    return res

def convert_country_code(code:str|Iterable, to:str = "name_zh",
                         additional_data:pd.DataFrame|None = None,
                         not_found:str|None = None,
                         use_regex:bool = False) -> str|list[str] :
    """
    转换各类国家代码，到指定类型。
    """
    SRCS_trans = {
         "alpha_2":"ISO2", "alpha_3":"ISO3", "numeric":"ISOnumeric",
         "ISO":"ISOnumeric", "name":"name_short"}
    if re.match(r"^name_.", to) :
        langu = to.split("_")[1]
        SRCS_trans = {**SRCS_trans, **{to:"ISO3"}}
    else:
        langu = None
    SRCS = ['APEC', 'BASIC', 'BRIC', 'CC41', 'CIS', 'Cecilia2050', 'Continent_7',
            'DACcode', 'EEA', 'EU', 'EU12', 'EU15', 'EU25', 'EU27', 'EU27_2007',
            'EU28', 'EURO', 'EXIO1', 'EXIO1_3L', 'EXIO2', 'EXIO2_3L', 'EXIO3',
            'EXIO3_3L', 'Eora', 'FAOcode', 'G20', 'G7', 'GBDcode', 'GWcode', 'IEA',
            'IMAGE', 'IOC', 'ISO2', 'ISO3', 'ISOnumeric', 'MESSAGE', 'OECD',
            'REMIND', 'Schengen', 'UN', 'UNcode', 'UNmember', 'UNregion', 'WIOD',
            'ccTLD', 'continent', 'name_official', 'name_short', 'obsolete', 'regex']
    if to not in (list(SRCS_trans.keys())+SRCS) :
        raise ValueError("This value `{}` for `to` is not supported !".format(to))
    converter = coco.CountryConverter(additional_data=additional_data)
    tto = SRCS_trans[to] if to in SRCS_trans.keys() else to
    kargs = { "names" : code, "to" : tto, "not_found" : not_found }
    if use_regex :
        kargs = {**kargs, **{"src":'regex'}}
    res = converter.convert(**kargs)
    if langu is not None :
        if isinstance(res, str) :
            res = local_name(res, local=langu,not_found=not_found)
        else :
            res = [local_name(x, local=langu,not_found=not_found) for x in res]
    return res

def quick_date(date:str|None = None, sformat:str|None = None, 
               tz:str|None = None) -> pdl.DateTime :
    """
    快速处理日期文字，或全默认则生成今日日期。
    """
    if date is None :
        res = pdl.now()
        res = res.in_timezone(tz = tz)
        return res
    if re.match(r"^\d{0,4}\.?\d{1,2}\.\d{1,2}$", date) :
        if date.count('.') == 2 :
            dformat = "YYYY.M.D"
        else :
            dformat = "M.D"
        return pdl.from_format(date, dformat, tz=tz)
    if re.match(r"^\d{4}/?\d{2}$", date) :
        if '/' in date :
            dformat = "YYYY/MM"
        else:
            dformat = "YYYYMM"
        return pdl.from_format(date, dformat, tz=tz)
    if sformat :
        return pdl.from_format(date, sformat, tz=tz)
    else:
        return pdl.parse(date, tz = tz)

def get_interval_dates(start:str|pdl.DateTime, 
                       end:str|pdl.DateTime, tz:str|None = None,
                       gap:str|None = None, limit_gap:bool = False
                      ) -> list[pdl.DateTime]|list[tuple[pdl.DateTime]] :
    """
    生成日期区间列表。
    """
    tupRange = gap.split(" ") if gap else ["1","days"]
    tupRange = [tupRange[-1], int(tupRange[0])]
    sD = quick_date(start,tz=tz) if isinstance(start, str) else start
    eD = quick_date(end,tz=tz) if isinstance(end, str) else end
    listDates = [i for i in pdl.interval(sD,eD).range(*tupRange)]
    if gap is None :
        return listDates
    else :
        if limit_gap :
            return [(listDates[i],listDates[i+1]) 
                    for i in range(len(listDates)-1)]
        else :
            return [(listDates[i],
                     listDates[i].add(**{tupRange[0]:(tupRange[1]-1)})) 
                     for i in range(len(listDates))]

def get_keydate(year:int|None = None, 
                month:int|None = None, 
                day:int|None = None,
                hour:int|None = None,
                minute:int|None = None,
                second:int|None = None
                ) -> pdl.DateTime :
    """获取指定日期；默认值为当前时间"""
    xDate = pdl.now()
    tY = xDate.year if year is None else year
    tM = xDate.month if month is None else month
    tD = xDate.day if day is None else day
    tH = xDate.hour if hour is None else hour
    tmi = xDate.minute if minute is None else minute
    ts = xDate.second if second is None else second
    res = pdl.DateTime(year=tY, month=tM, day=tD,
                       hour=tH, minute=tmi, second=ts)
    return res

def last_date(keydate:str|pdl.DateTime|None = None,
              last_:str = "month",
              tz:str|None = None) -> tuple[pdl.DateTime] :
    """
    计算上一个时间区间的函数。
    last_ 只支持 "day","week","month","season","year"。
        day：昨天
        week：上周
        month：上个月
        season：上个季度
        year：上一年
    """
    if last_ not in ["day","week","month","season","year"] :
        raise ValueError("`last_` must be in ['day', 'week','month', 'season', 'year']")
    pinDate = keydate if isinstance(keydate, pdl.DateTime) else quick_date(date=keydate,tz=tz)
    if last_ == 'season' :
        last_pin = pinDate.subtract(months=3)
        for snx in [[1,2,3],[4,5,6],[7,8,9],[10,11,12]] :
            if last_pin.month in snx :
                res = (last_pin.on(last_pin.year, min(snx), 1).start_of("month"),
                       last_pin.on(last_pin.year, max(snx), 1).end_of("month"))
                return res
    else :
        last_pin = pinDate.subtract(**{(last_+"s"):1})
        return (last_pin.start_of(last_),last_pin.end_of(last_))

def near_date(keydate:str|pdl.DateTime|None = None,
              near_:str = "day", nth:int = 1,
              tz:str|None = None) -> tuple[pdl.DateTime] :
    """
    计算之前的一段时间区间，可以是之前1天也可以是之前n天到前1天。
    near_ 用于计算之前的周期单位。
    nth 用于计算之前周期的跨度。nth>0,表示到昨日的最nth个周期；nth=0,表示当前的周期。
    例如：1. "near_=day,nth=1"，代表昨天时间区间（默认计算昨天）。
         2. "near_=day,nth=0"，代表今天时间区间。
    """
    if near_ not in ["day","week","month","year"] :
        raise ValueError("`near_` must be in ['day', 'week','month', 'year']")
    pinDate = keydate if isinstance(keydate, pdl.DateTime) else quick_date(date=keydate,tz=tz)
    if nth > 0 :
        res = (pinDate.subtract(**{near_+"s":nth}).start_of("day"),
            pinDate.subtract(days=1).end_of("day"))
    else:
        res = (pinDate.start_of(near_),pinDate.end_of(near_))
    return res

def lastDay(keydate:str|pdl.DateTime|None = None, 
            of_:str|None = None,
            point:str = "last", 
            tz:str|pdl.Timezone|pdl.FixedTimezone|None = None) -> pdl.DateTime :
    """
    get the last day of the week/month/year.
    point == last : get the last day of the last week/month/year.
    point == near : get the last day of the next week/month/year.
    point == now : get the last day of this week/month/year.
    """
    if of_ in ["week", "month", "year"] :
        xof = of_
    elif of_ is None :
        xof = "month"
    else:
        raise ValueError("of_ just support week, month or year!")
    if point not in ["last", "near", "now"] :
        raise ValueError("point just support last, near or now!")
    if keydate is None :
        anchor = quick_date()
    else :
        anchor = keydate if isinstance(keydate, pdl.DateTime) else pdl.parse(keydate)
    if point == "last" :
        anchor = anchor.subtract(**{xof+"s":1})
    if point == "near" :
        anchor = anchor.add(**{xof+"s":1})
    anchor = anchor.in_tz(tz if tz else "UTC")
    return anchor.end_of(xof)

def firstDay(keydate:str|pdl.DateTime|None = None, 
            of_:str|None = None,
            point:str = "last", 
            tz:str|pdl.Timezone|pdl.FixedTimezone|None = None) -> pdl.DateTime :
    """
    get the last day of the week/month/year.
    point == last : get the last day of the last week/month/year.
    point == near : get the last day of the next week/month/year.
    point == now : get the last day of this week/month/year.
    """
    if of_ in ["week", "month", "year"] :
        xof = of_
    elif of_ is None :
        xof = "month"
    else:
        raise ValueError("of_ just support week, month or year!")
    if point not in ["last", "near", "now"] :
        raise ValueError("point just support last, near or now!")
    if keydate is None :
        anchor = quick_date()
    else :
        anchor = keydate if isinstance(keydate, pdl.DateTime) else pdl.parse(keydate)
    if point == "last" :
        anchor = anchor.subtract(**{xof+"s":1})
    if point == "near" :
        anchor = anchor.add(**{xof+"s":1})
    anchor = anchor.in_tz(tz if tz else "UTC")
    return anchor.first_of(xof)

def getExcelSheets(path:Path) -> list :
    if path.suffix in [".xls",".xlsx"] :
        res = pd.ExcelFile(path).sheet_names
        return res
    else:
        raise ValueError("only support excel file(.xls/.xlsx)...")

def impedanceList(oriList:list, tarList:list,
                  preset:dict|None = None) -> list :
    res = []
    for xi in oriList :
        if xi in tarList :
            res.append(xi)
        else :
            if preset :
                if xi in preset.keys() :
                    res.append(preset[xi])
                elif xi in preset.values() :
                    res.append({v:k for k,v in preset.items()}[xi])
                else :
                    res.append(process.extract(xi, tarList, limit=1)[0][0])
            else :
                res.append(process.extract(xi, tarList, limit=1)[0][0])
    return res

