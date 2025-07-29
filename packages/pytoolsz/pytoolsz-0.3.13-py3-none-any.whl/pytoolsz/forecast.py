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

# 说明：
# 预测需要做这样几件事：
# 1. 确实数据是否平稳
# 2. 处理数据，进行差分
# 3. 拟合模型
# 4. 预测
# 传统来说，平稳与否是一个时间序列预测是否可行的标志。但现在也有很多手段可以在务虚平稳条件下进行预测。
# 模型目前支持：prophet、ARIMA。
# 这里提供预测所需要的各类方法。
# 对模型的基础理解：
# 1. ARIMA ：传统时序模型的基准模型，需要前序处理，并寻找平稳方案。
# 2. prophet ：传统时序模型的集大成者，减少前序处理程度，并提供了更多添加属性，使时序预测更准确。

from itertools import product
from typing import Union
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from statsmodels.tsa.stattools import adfuller,arma_order_select_ic
from statsmodels.tsa.statespace.sarimax import SARIMAX

from pytoolsz.tsTools import tsFrame
from pytoolsz.frame import szDataFrame

import pmdarima as pm
import importlib

import pandas as pd
import polars as pl
import numpy as np

__all__ = ["is_DataFrame", "auto_orders", "help_kwargs", "quickProphet", "quickARIMA"]

def is_DataFrame(obj) -> bool :
    """判断是否为 DataFrame 类型"""
    return isinstance(obj,
                      (pl.DataFrame, pd.DataFrame, tsFrame, szDataFrame))

def auto_orders(data:pd.Series, diff_max:int = 40, 
                use_log:bool = False) -> tuple:
    """
    自动选择合适时序特征
    目前并不推荐auto_orders方法，因为其计算量过大，且存在所搜范围可能不足的问题。
    除非特殊情况，请选择quickOrders方法来确定arima的模型参数。
    """
    tdt = np.log(data) if use_log else data
    tmax = len(tdt) if diff_max > len(tdt) else diff_max
    for i in range(1,tmax+1):
        temp = tdt.diff(i).dropna()
        if any((temp == np.inf).tolist()):
            temp[temp == np.inf] = 0.0
        adf = adfuller(temp)
        if adf[1] < 0.05:
            d = i
            break
    bpq = []
    for i in ["n","c"]:
        tmp = arma_order_select_ic(tdt, ic=['aic','bic','hqic'])
        bpq.extend([
            tmp["aic_min_order"],
            tmp["bic_min_order"],
            tmp["hqic_min_order"],
        ])
    p = np.argmax(np.bincount(np.array(bpq).T[0]))
    q = np.argmax(np.bincount(np.array(bpq).T[1]))
    x = np.fft.fft(tdt)
    xf = np.linspace(0.0,0.5,len(tdt)//2)
    dx = xf[np.argmax(np.abs(x[1:(len(tdt)//2)]))]
    s = 0 if dx == 0.0 else 1//dx
    if s == 0 :
        bP,bD,bQ = (0,0,0)
    else:
        Pl = list(range(0,p+1))
        bD = 1
        Ql = list(range(0,q+1))
        lPDQl = list(product(Pl,[bD],Ql,[s]))
        PDQtrend = product(lPDQl,['n',"c",'t','ct'])
        aic_min = 100000
        for ix in PDQtrend:
            model = SARIMAX(tdt,order=(p,d,d),
                            seasonal_order=ix[0],
                            trend=ix[1]).fit(disp=False)
            aic = model.aic
            if aic < aic_min:
                aic_min = aic
                bP,bD,bQ,_ = ix[0]
                bT = ix[1]
    return ((p,d,q),(bP,bD,bQ,int(s)),bT)

def quickOrders(data:pl.DataFrame|pd.DataFrame, target:str, 
                m:int = 1, **kwargs) -> tuple:
    """
    快速选择ARIMA模型的参数
    m - 季节性周期：
        1 - no seasonality（默认）
        7 - daily
        12 - monthly
        52 - weekly
    kwargs - arima模型的额外参数，可使用 `help_kwargs("AutoARIMA")` 查看所有参数。
    返回：
    order - ARIMA模型的参数（p,d,q）
    seasonal_order - 季节性参数（P,D,Q,s）
    """
    if not is_DataFrame(data):
        raise ValueError("Input data must be a polars/pandas DataFrame.")
    if target not in data.columns:
        raise ValueError(f"Column {target} not found in DataFrame.")
    if isinstance(data, pl.DataFrame) :
        tardata = data.to_pandas()[target]
    else :
        tardata = data[target]
    alargs = {
        "seasonal":True,
        "m":m,
        "stepwise":True,
        "trace":True,
        "error_action":"ignore",
        "suppress_warnings":True
    }.update(kwargs)
    model = pm.auto_arima(tardata,**alargs)
    return model.order, model.seasonal_order, model.trend

def help_kwargs(funcnama:str, println:bool = True) -> str|None :
    """参数帮助文档"""
    match funcnama :
        case "Prophet" :
            txt = Prophet.__dict__["__doc__"]
        case "AutoARIMA" :
            txt = pm.arima.AutoARIMA.__dict__['__doc__']
        case "SARIMA" :
            txt = SARIMAX.__dict__['__doc__']
        case "PatchTST":
            module = importlib.import_module("gluonts.torch")
            txt = getattr(module, "PatchTSTEstimator").__dict__['__doc__']
        case "DeepAR" :
            module = importlib.import_module("gluonts.torch")
            txt = getattr(module, "DeepAREstimator").__dict__['__doc__']
        case "Chronos" :
            module = importlib.import_module("autogluon.timeseries")
            txt = getattr(module, "TimeSeriesPredictor").fit.__doc__
        case _ :
            raise ValueError("funcnama `{}` is not supported.".format(funcnama))
    if println :
        print(txt)
    else :
        return txt

def quickProphet(data: pl.DataFrame|pd.DataFrame, 
                 dt: str, y: str, 
                 exog: list[str]|None = None,
                 n_periods: int = 10, 
                 future_exog:pl.DataFrame|pd.DataFrame|None = None, **kwargs) -> szDataFrame:
    """
    使用Prophet库进行时间序列预测的快速函数。

    参数:
        data (pl.DataFrame): 输入的时序数据，包含时间列和目标列。
        dt (str): 时间列在输入数据框中的列名。
        y (str): 目标列在输入数据框中的列名。
        exog (list[str]): 额外的外生变量列名列表。
        n_periods (int): 需要预测的未来时间周期数量。
        future_exog (pl.DataFrame): 未来时间点的外生变量数据框。
        **kwargs: Prophet模型的额外参数。可使用 `help_kwargs("Prophet")` 查看所有参数。

    返回:
        pl.DataFrame: 包含原始数据和预测结果的Polars DataFrame。
    """
    # 参数检查
    if not is_DataFrame(data):
        raise ValueError("Input data must be a polars/pandas DataFrame.")
    if dt not in data.columns or y not in data.columns:
        raise ValueError(f"Columns {dt} or {y} not found in DataFrame.")
    if exog is not None :
        if not set(exog).issubset(data.columns) :
            raise ValueError("exog columns not found in DataFrame.")
        if future_exog is None :
            raise ValueError("futuree_exog must be provided when exog is not None.")
    # 创建Prophet所需的DataFrame格式
    if isinstance(data, pl.DataFrame) :
        df = data.select(pl.col(dt), pl.col(y)).rename({dt: "ds", y: "y"})
        df = df.to_pandas()
    else :
        df = data[[dt, y]].rename({dt: "ds", y: "y"})
    # 计算时间间隔
    freq = pd.infer_freq(df["ds"])
    # 初始化Prophet模型
    model = Prophet(**kwargs)
    for col in exog :
        model.add_regressor(col)
    model.fit(df)
    # 生成未来的时间点
    future = model.make_future_dataframe(periods=n_periods, freq=freq)
    if exog is not None :
        for col in exog :
            future[col] = future_exog[col]
    # 预测
    forecast = model.predict(future)
    # 转换为Polars DataFrame并合并
    forecast_pl = pl.from_pandas(forecast)
    result = data.join(forecast_pl.rename({"ds": dt}), on=dt, how="outer")
    return szDataFrame(filepath=None, from_data=result)

def quickARIMA(data: Union[pl.DataFrame, pd.DataFrame], target: str, 
               n_periods: int = 10,
               exog: Union[list[str], None] = None, m: int = 1,
               future_exog: Union[pl.DataFrame, pd.DataFrame, None] = None,
               orders: Union[tuple, str] = "auto", **kwargs) -> pl.DataFrame:
    # 输入校验
    if not is_DataFrame(data):
        raise ValueError("Input data must be a polars/pandas DataFrame.")
    if exog is not None:
        if not set(exog).issubset(data.columns):
            raise ValueError("exog columns not found in DataFrame.")
    # 处理orders参数
    if isinstance(orders, str):
        if orders.lower() == "auto":
            # 假设quickOrders返回(order, seasonal_order, trend)
            orders = quickOrders(data, target, m=m, **kwargs)
        else:
            raise ValueError("orders must be a tuple or 'auto'.")
    elif not (isinstance(orders, tuple) and len(orders) == 3):
        raise ValueError("orders must be a tuple((p,d,q),(P,D,Q,s),trend) or 'auto'.")
    # 统一转换为pandas格式处理
    if isinstance(data, pl.DataFrame):
        data_pd = data.to_pandas()
    else:
        data_pd = data.copy()
    # 提取目标变量和外生变量
    endog = data_pd[target]
    exog_data = data_pd[exog] if exog is not None else None
    # 拆分orders参数
    order, seasonal_order, trend = orders
    # 创建并拟合模型
    model = SARIMAX(
        endog=endog,
        exog=exog_data,
        order=order,
        seasonal_order=seasonal_order,
        trend=trend,
        **kwargs
    )
    model_fit = model.fit(disp=False)
    # 预测阶段的外生变量处理
    future_exog_processed = None
    if exog is not None:
        if future_exog is None:
            raise ValueError("future_exog must be provided when using exog.")
        if not set(exog).issubset(future_exog.columns):
            raise ValueError("future_exog must contain all exog columns.")
        if len(future_exog) != n_periods:
            raise ValueError(f"future_exog must have exactly {n_periods} rows.")
        # 转换为pandas格式
        if isinstance(future_exog, pl.DataFrame):
            future_exog_pd = future_exog.to_pandas()
        else:
            future_exog_pd = future_exog.copy()
        future_exog_processed = future_exog_pd[exog]
    # 执行预测并获取置信区间
    forecast = model_fit.get_forecast(
        steps=n_periods,
        exog=future_exog_processed
    )
    # 提取预测结果的三要素
    forecast_mean = forecast.predicted_mean
    conf_int = forecast.conf_int()  # 获取置信区间DataFrame
    # 构建返回结果
    return pl.DataFrame({
        f"{target}_pred": forecast_mean.values,
        f"{target}_upper": conf_int.iloc[:, 1].values,
        f"{target}_lower": conf_int.iloc[:, 0].values
    })

def quickPreRNN(data:pl.DataFrame|pd.DataFrame, target:str,
                engine:str = "autogluon", module:str = "bolt_base") -> pl.DataFrame :
    """
    使用高阶RNN模型进行时间序列预测的函数。
    主要支持的模型有：
    - PatchTST
    - DeepAR
    - Chronos
    """
    # 定义基本可支持模型。
    models = {
        "gluonts": {
            "PatchTST": "torch.PatchTSTEstimator",
            "DeepAR": "torch.DeepAREstimator",
        },
        "autogluon": "timeseries.TimeSeriesPredictor",
    }
    if engine not in models.keys():
        raise ValueError("Engine `{}` is not supported.".format(engine))
    else :
        spec = importlib.util.find_spec(engine)
        if spec is None :
            raise ValueError(f"Engine `{engine}` is not installed. Use `pip install {engine}` to install.")
        else :
            if engine == "autogluon" :
                pickName = models[engine].split(".")
                fixName = ".".jion([engine, pickName[0]])
            else :
                if module not in models[engine].keys():
                    raise ValueError(f"Module `{module}` is not supported in engine `{engine}`.")
                pickName = models[engine][module].split(".")
                fixName = ".".jion([engine, pickName[0]])
            packModule = importlib.import_module(fixName)
            createModel = getattr(packModule, pickName[1])
    if not is_DataFrame(data):
        raise ValueError("Input data must be a polars/pandas DataFrame.")
    if target not in data.columns:
        raise ValueError(f"Column {target} not found in DataFrame.")
    pass