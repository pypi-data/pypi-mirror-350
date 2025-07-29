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

import matplotlib.pyplot as plt
import matplotlib.colors as mcolor
import matplotlib.patches as mpatches
import matplotlib.cm as mcm
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import polars as pl
import numpy as np
import inspect
import math
import cmaps
import re

import cartopy.crs as ccrs
import frykit.plot as fplt
import frykit.shp as fshp
from typing import Self
from pathlib import Path
from thefuzz import process
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import Normal, Stroke

__all__ = ["ColormapSZ", "bullet", "chinaMap", "optimize_fonts", "heatmapSZ"]

def _list_cmaps() -> list :
    attributes = inspect.getmembers(cmaps, lambda _: not (inspect.isroutine(_)))
    colors = [_[0] for _ in attributes if
              not (_[0].startswith('__') and _[0].endswith('__'))]
    return colors

def _list_MPLColors() -> list :
    res = list(mcolor.BASE_COLORS.keys())
    res.extend(list(mcolor.TABLEAU_COLORS.keys()))
    res.extend(list(mcolor.CSS4_COLORS.keys()))
    res.extend(list(mcolor.XKCD_COLORS.keys()))
    return res

def _get_MPLColors(name:str) -> str :
    if name in mcolor.TABLEAU_COLORS.keys():
        return mcolor.TABLEAU_COLORS[name]
    elif name in mcolor.CSS4_COLORS.keys():
        return mcolor.CSS4_COLORS[name]
    elif name in mcolor.XKCD_COLORS.keys():
        return mcolor.XKCD_COLORS[name]
    else:
        return mcolor.BASE_COLORS[name]

def _list_MPLColormaps() -> list :
    res = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 
           'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 
            'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 
            'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 
            'hsv', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 
            'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c',
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar']
    return res

def _checkList(txt:str, aList:list) -> bool :
    for i in aList :
        if txt in i :
            return True
    return False

def get_Fonts(subName:str|None = None, n:int = 5) -> list :
    """
    获取字体列表，或查询某一个字体
    """
    fontsList = [i.name for i in mpl.font_manager.fontManager.ttflist]
    fontsList = list(set(fontsList))
    if subName is not None :
        selList = process.extract(subName, fontsList, limit = n)
        res = [i[0] for i in selList]
    else :
        res = fontsList
    return res

def optimize_fonts(Fonts:str|list|None = None) -> None :
    """
    优化绘图字体的显示
    """
    nomarl = ["Source Han Sans SC","Segoe UI","Leelawadee UI"]
    if Fonts is not None :
        if isinstance(Fonts, str) :
            nomarl.append(Fonts)
            nomarl = list(set(nomarl))
        elif isinstance(Fonts, list) :
            nomarl.extend(Fonts)
            nomarl = list(set(nomarl))
        else :
            raise ValueError("Fonts must be str or list!")
    mpl.rcParams["font.family"] = nomarl


class ColormapSZ(object) :
    """
    ::颜色映射::
    
    - 可以使用多种内容生成colormap。核心依赖于 `matplotlib.colors.LinearSegmentedColormap` 。
    - 
    """
    def __init__(self, name:str|list|LinearSegmentedColormap = "blue", 
                 reverse:bool = False) -> None:
        if isinstance(name, list) :
            self.__cmap = LinearSegmentedColormap.from_list("createdColormap", name)
        elif isinstance(name, LinearSegmentedColormap) :
            self.__cmap = name
            if reverse :
                self.__cmap = self.__cmap.reversed()
        else:
            xname = name[:-2] if name.endswith("_r") else name
            if re.match("^#(([A-Fa-f0-9]{3})|([A-Fa-f0-9]{6}))$", xname) :
                self.__cmap = sns.light_palette(xname, reverse=reverse,as_cmap=True)
            elif xname in _list_cmaps() :
                self.__cmap = getattr(cmaps, name).to_seg(256)
                if reverse :
                    self.__cmap = self.__cmap.reversed()
            elif xname in _list_MPLColormaps() :
                self.__cmap = mpl.colormaps[name]
                if reverse :
                    self.__cmap = self.__cmap.reversed()
            elif xname.lower() in _list_MPLColors() :
                self.__cmap = sns.light_palette(
                    _get_MPLColors(name.lower()),reverse=reverse,as_cmap=True)
            else:
                raise ValueError("color name not found !")
    @property
    def name(self) -> str :
        return self.__cmap.name
    @property
    def N(self) -> int :
        return self.__cmap.N
    def reversed(self) -> Self :
        newcmap = self.__cmap.reversed()
        return(ColormapSZ(name = newcmap))
    def resampled(self, n:int) -> LinearSegmentedColormap :
        return self.__cmap.resampled(n)
    def get(self, n:int) -> str :
        return mpl.colors.rgb2hex(self.__cmap(n))
    def getListColors(self, length:int) -> list :
        tcmap = self.resampled(length)
        return [mpl.colors.rgb2hex(tcmap(i+1)) for i in range(length)]
    def colormap(self) -> LinearSegmentedColormap :
        return self.__cmap
    def show(self) -> None :
        import matplotlib.pyplot as plt
        a = np.outer(np.ones(10), np.arange(0, 1, 0.001))
        plt.figure(figsize=(2.5, 0.5))
        plt.subplots_adjust(top=0.95, bottom=0.05, left=0.01, right=0.99)
        plt.subplot(111)
        plt.axis('off')
        plt.imshow(a, aspect='auto', cmap=self.__cmap, origin='lower')
        plt.show()


class bullet(object):
    """
    子弹图
    """
    def __init__(self, data, fitted = False, limits = None, palette = None) -> None:
        '''
        fitted data: 为已经整理好的
        '''
        self.data = data
        self.__fitdata = data if fitted else None
        self.__limits = limits if fitted else None
        self.__pldata = None
        self.__config = {
            'Font':'Simhei',
            'palette': palette if palette else "green",
            'target_color': '#f7f7f7',
            'bar_color': '#252525',
            'label_color': 'black',
            'keep_label': None, #分类数据顺序
            'pass_zero': True,
            'orientations': 'horizontal', #方向：{'vertical', 'horizontal'}
            'figsize': (12,8),
            'labels': None,
            'formatter': None,
            'axis_label' : None,
            'title' : None,
        }
    def datafitting(self, values = None, index = None, columns = None, aggfunc = 'sum'):
        """
        数据整理
        """
        if self.__fitdata is None:
            self.__fitdata = self.data.pivot_table(values=values,index=index,columns=columns,aggfunc=aggfunc)
        if self.__config['keep_label'] :
            self.__fitdata = self.__fitdata[self.__config['keep_label']]
        if self.__config['pass_zero']:
            for i in self.__fitdata.columns.tolist():
                self.__fitdata.loc[self.__fitdata[i]==0,i] = np.nan
        res = self.__fitdata.describe().T
        res = res[['mean','50%']]
        self.__pldata = list(map(lambda x:list([x[0],*x[1]]),res.iterrows()))
        res = res.describe().loc[["min","25%","75%","max"]]
        if self.__limits is None:
            self.__limits = list(map(lambda x: min(x[1]) if x[0]!="max" else np.ceil(max(x[1])*1.1),res.iterrows()))
        if self.__config["labels"] is None:
            self.__config["labels"] = [' ']*len(self.__limits)
    def config(self,**args):
        self.__config.update(args)
    def heatmap(self):
        '''
        直接使用fitted data数据绘制热力图。
        '''
        plt.figure(figsize=self.__config["figsize"])
        sns.heatmap(self.__fitdata.T,cmap=self.__config["palette"])
    def plot(self, save = None):
            """
            子弹图绘制。
            """
            # Determine the max value for adjusting the bar height
            # Dividing by 10 seems to work pretty well
            h = self.__limits[-1] / 10
            plt.rcParams['font.sans-serif'] = [self.__config['Font']]
            # Use the green palette as a sensible default
            if isinstance(self.__config["palette"], str):
                tPalette = sns.light_palette(self.__config["palette"], len(self.__limits), reverse=False)
            else:
                tPalette = self.__config["palette"]
            
            # Must be able to handle one or many data sets via multiple subplots
            if len(self.__pldata) == 1:
                RoCo_Nums = {
                    "sharex" if self.__config['orientations']=='horizontal' else "sharey" : True
                }
                fig, ax = plt.subplots(figsize=self.__config["figsize"], **RoCo_Nums)
            else:
                RoCo_Nums = {
                    "nrows" if self.__config['orientations']=='horizontal' else "ncols" : len(self.__pldata),
                    "sharex" if self.__config['orientations']=='horizontal' else "sharey" : True
                }
                fig, axarr = plt.subplots(figsize=self.__config["figsize"], **RoCo_Nums)

            # Add each bullet graph bar to a subplot
            for idx, item in enumerate(self.__pldata):
                
                # Get the axis from the array of axes returned when the plot is created
                if len(self.__pldata) > 1:
                    ax = axarr[idx]

                # Formatting to get rid of extra marking clutter
                ax.set_aspect('equal')
                if self.__config['orientations']=='horizontal':
                    ax.set_yticklabels([item[0]])
                    ax.set_yticks([1])
                else:
                    ax.set_xticklabels([item[0]])
                    ax.set_xticks([1])
                ax.spines['bottom'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)

                prev_limit = 0
                for idx2, lim in enumerate(self.__limits):
                    # Draw the bar
                    if self.__config['orientations']=='horizontal':
                        ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
                                color=tPalette[idx2])
                    else:
                        ax.bar([1],lim - prev_limit, bottom=prev_limit, width=h,
                               color=tPalette[idx2])
                    prev_limit = lim
                rects = ax.patches
                # The last item in the list is the value we're measuring
                # Draw the value we're measuring
                if self.__config['orientations']=='horizontal':
                    ax.barh([1], item[1], height=(h / 3), color=self.__config["bar_color"])
                else:
                    ax.bar([1], item[1], width=(h / 3), color=self.__config["bar_color"])

                # Need the ymin and max in order to make sure the target marker
                # fits
                if self.__config['orientations']=='horizontal':
                    ymin, ymax = ax.get_ylim()
                    ax.vlines(
                        item[2], ymin * .9, ymax * .9, linewidth=1.5, color=self.__config["target_color"])
                else:
                    xmin, xmax = ax.get_xlim()
                    ax.hlines(
                        item[2], xmin*0.9, xmax*0.9, linewidth=1.5, color=self.__config["target_color"])

            # Now make some labels
            if self.__config["labels"] is not None:
                for rect, label in zip(rects, self.__config["labels"]):
                    if self.__config['orientations']=='horizontal':
                        height = rect.get_height()
                        ax.text(
                            rect.get_x() + rect.get_width() / 2,
                            -height * .4,
                            label,
                            ha='center',
                            va='bottom',
                            color=self.__config["label_color"])
                    else:
                        width = rect.get_width()
                        ax.text(
                            -width * .4,
                            rect.get_y() + rect.get_height() / 2,
                            label,
                            ha='left',
                            va='center',
                            color=self.__config["label_color"])
            if self.__config["formatter"]:
                if self.__config['orientations']=='horizontal':
                    ax.xaxis.set_major_formatter(self.__config["formatter"])
                else:
                    ax.yaxis.set_major_formatter(self.__config["formatter"])
            if self.__config["axis_label"]:
                if self.__config['orientations']=='horizontal':
                    ax.set_xlabel(self.__config["axis_label"])
                else:
                    ax.set_ylabel(self.__config["axis_label"])
            if self.__config["title"]:
                fig.suptitle(self.__config["title"], fontsize=14)
            WHspace = {"hspace" if self.__config['orientations']=='horizontal' else "wspace":0}
            fig.subplots_adjust(**WHspace)


class chinaMap(object) :
    """
    中国地图的热力图绘制
    fonts : 字体设定。可以使用`get_Fonts`方法进行字体名称查询。
            常用的有：微软雅黑（Microsoft YaHei）、黑体（SimHei）、宋体（SimSun）、得意黑（Smiley Sans）
    """
    MAP_PROJECTION = ["NormalChina", "Mercator", "PlateCarree"]
    def __init__(self, data:pl.DataFrame|pd.DataFrame, 
                 place:str|None = None, value:str|None = None, 
                 nbin:list|int|bool = True, vmin:float|str = 'auto', vmax:float|str = 'auto', 
                 cmap:str|tuple = "BlGrYeOrReVi200", 
                 figsize:tuple[int|float] = (10, 6), nine_line:bool = True, 
                 map_projection:str = "NormalChina") -> None :
        self.__oridata = pl.from_dataframe(data) if isinstance(data, pd.DataFrame) else data
        if isinstance(nine_line,str):
            if nine_line != "mini" :
                raise ValueError("nine_line参数错误")
        if place is None :
            self.__usedata = pl.DataFrame()
        else :
            checkData = self.__oridata.with_columns(
                pl.col(place).map_elements(lambda x : str(type(x)), return_dtype=pl.String).alias("check")
            )
            if not _checkList("Polygon", checkData["check"].unique().to_list()) :
                checkData = checkData.with_columns(
                    pl.col(place).map_elements(lambda x : fshp.get_cn_province(
                                                                process.extractOne(x,
                                                                    fshp.get_cn_province_names())[0]
                                                          ), 
                                               return_dtype=pl.Object).alias("geoPlace")
                )
                xplace = "geoPlace"
            else :
                xplace = place
            if value is None :
                self.__usedata = checkData.group_by(xplace).agg(
                    pl.col(xplace).count().alias("count"))
            else :
                self.__usedata = checkData.select(
                    pl.col([xplace,value]))
        self.__selName = self.__usedata.columns
        if map_projection not in chinaMap.MAP_PROJECTION :
            raise ValueError("map_projection参数错误")
        if map_projection == "NormalChina" :
            self.__map_crs = fplt.CN_AZIMUTHAL_EQUIDISTANT
        elif map_projection == "Mercator" :
            self.__map_crs = fplt.WEB_MERCATOR
        else:
            self.__map_crs = fplt.PLATE_CARREE
        self.__data_crs = ccrs.PlateCarree()
        self.__fig = None
        self.__main_ax = None
        self.__mini_ax = None
        self.__cmap = None
        self.__norm = None
        self.__plot_config = {
            "font" : None,
            "figsize" : figsize,
            "nine_line" : nine_line,
            "cmap_name" : cmap, 
            "nbin" : nbin,
            "bins" : None,
            "labels" : None,
            "vmin" : math.floor(self.__oridata[value].min()) if vmin == 'auto' else vmin,
            "vmax" : math.ceil(self.__oridata[value].max()) if vmax == 'auto' else vmax,
            "main_extent":(78, 134, 14, 55), # 用于控制地图的截取(左右下上)(经纬度)
            "mini_extent":(105, 120, 2, 25), # 用于控制地图的截取(左右下上)(经纬度)
        }
    @classmethod
    def show_map_projection(cls, txt:bool = False) -> str|None :
        info = [
            "标准中国地图投影",
            "网格墨卡托投影",
            "等经纬投影"
        ]
        txtDict = dict(zip(chinaMap.MAP_PROJECTION,info))
        res = ""
        for key,data in txtDict.items() :
            res += "{}:\t{}\n".format(key,data)
        if txt :
            return res
        else:
            print(res)
    def set_configs(self, **kwargs) -> None :
        """
        设置绘图参数
        """
        for key,value in kwargs.items() :
            if key in self.__plot_config.keys() :
                self.__plot_config[key] = value
            else :
                raise ValueError("{}参数错误".format(key))
    def set_keydata(self, place:str, value:str|None = None, 
                    replace_data:pd.DataFrame|pl.DataFrame|None = None) -> None :
        """
        设置绘图的关键数据。也可以在这时候替换数据。
        """
        if replace_data is not None :
            if isinstance(replace_data, pd.DataFrame) :
                self.__oridata = pl.from_dataframe(replace_data)
            elif isinstance(replace_data, pl.DataFrame) :
                self.__oridata = replace_data
            else :
                raise ValueError("replace_data参数错误")
            self.__usedata = pl.DataFrame()
        if place is None or place == "" or place not in self.__oridata.columns:
            raise ValueError("place参数错误！必须给出有效数据！")
        if not self._checkData() :
            if value is None :
                self.__usedata = self.__oridata.group_by(place).agg(
                    pl.col(place).count().alias("count"))
            else :
                self.__usedata = self.__oridata.select(
                    pl.col([place,value]))
    def _checkData(self) -> bool :
        """
        检查数据是否准备完毕。
        """
        if self.__usedata.is_empty() :
            return False
        else :
            return True
    def setting_colors(self, colormap:str|list|None = None) -> None :
        """
        还可以在设定颜色时，再次修改colormap。
        根据绘图的预设情况，完成颜色的酌定和Normal化设定。
        """
        if colormap is None :
            self.__cmap = ColormapSZ(name = self.__plot_config["cmap_name"])
        else :
            self.__cmap = ColormapSZ(name = colormap)
            self.__plot_config["cmap_name"] = colormap
        if isinstance(self.__plot_config["nbin"], list) :
            xn = len(self.__plot_config["nbin"]) -1
            self.__plot_config["bins"] = self.__plot_config["nbin"]
        else :
            xn = 5 if isinstance(self.__plot_config["nbin"],bool) else self.__plot_config["nbin"]
            widthTMP = self.__plot_config['vmax']-self.__plot_config['vmin']
            gap = math.ceil(widthTMP/xn)
            self.__plot_config["bins"] = [x for x in range(self.__plot_config['vmin'],self.__plot_config['vmax']+gap,gap)]
        bins = self.__plot_config["bins"]
        if self.__plot_config["labels"] is None :
            self.__plot_config["labels"] = [f'{bins[i]} - {bins[i + 1]}' for i in range(xn)]
        if isinstance(self.__plot_config["nbin"], bool) :
            if self.__plot_config["nbin"] :
                self.__norm = mcolor.BoundaryNorm(bins, xn)
            else:
                self.__norm = mcolor.Normalize(self.__plot_config['vmin'],
                                               self.__plot_config['vmax'], 
                                               clip=True)
        else :
            self.__norm = mcolor.BoundaryNorm(bins, xn)
    def preDrawing(self) -> None :
        """
        正是计划图前的准备过程。生成必要的画布。
        """
        if self.__plot_config["font"] is not None :
            plt.rcParams['font.family'] = self.__plot_config["font"]
        self.__fig = plt.figure(figsize=self.__plot_config["figsize"])
        self.__main_ax = self.__fig.add_subplot(projection=self.__map_crs)
        self.__main_ax.set_extent(self.__plot_config["main_extent"], self.__data_crs)
        if self.__plot_config["nine_line"] :
            fplt.add_nine_line(self.__main_ax, lw=0.5)
        self.__main_ax.axis('off')
        if self.__plot_config["nine_line"]:
            self.__mini_ax = fplt.add_mini_axes(self.__main_ax)
            self.__mini_ax.set_extent(self.__plot_config["mini_extent"], self.__data_crs)
            fplt.add_nine_line(self.__mini_ax, lw=0.5)
    def plot_province(self, **kwags) -> None :
        """
        **kwags : https://matplotlib.org/stable/api/collections_api.html
        """
        if self.__main_ax is None :
            raise ValueError("请先调用predrawing方法，完成绘图准备。")
        # 字体描边，便于文字识别
        path_effects = [Stroke(linewidth=1.5, foreground='w'), Normal()]
        # 绘图
        defautKwags = {"ec":'k', "lw":0.4}
        defautKwags.update(kwags)
        axsList = [self.__main_ax, self.__mini_ax] if self.__mini_ax is not None else [self.__main_ax]
        if self.__plot_config["nbin"] is False :
            cm_n = self.__cmap.colormap()
        else:
            cm_n = self.__cmap.resampled(len(self.__plot_config["labels"]))
        for ax in axsList:
            fplt.add_geoms(
                ax, self.__usedata[self.__selName[0]].to_list(), 
                array=self.__usedata[self.__selName[1]].to_list(), 
                cmap=cm_n, norm=self.__norm, 
                **defautKwags
            )
            for text in fplt.label_cn_province(ax).texts:
                text.set_path_effects(path_effects)
                if text.get_text() in ['香港', '澳门']:
                    text.set_visible(False)
    def add_compass(self, x:float = 0.5, y:float = 0.85, 
                    angle:float|None = None,
                    size:float = 20, style:str = 'circle') -> None :
        """
        添加指南针
        """
        if style not in ['arrow', 'star', 'circle']:
            raise ValueError("style参数错误")
        fplt.add_compass(self.__main_ax, x, y, size=size, 
                         angle=angle, style=style)
    def add_scalebar(self, x:float = 0.22, y:float = 0.1,
                     length:float = 1000, units:str = "km",
                     segments:list|int = 5) -> None :
        """
        添加作标尺
        """
        scale_bar = fplt.add_scale_bar(self.__main_ax, x, y, length=length, units=units)
        if isinstance(segments, list):
            if len(segments) % 2 == 0 :
                scale_bar.set_xticks(segments)
            else:
                shSegs = [v for i,v in enumerate(segments) if i % 2 == 0]
                miSegs = [v for i,v in enumerate(segments) if i % 2 == 1]
                scale_bar.set_xticks(shSegs)
                scale_bar.set_xticks(miSegs, minor=True)
        else:
            bins = length / (segments - 1)
            segList = [x for x in range(0,int(length + bins), int(bins))]
            if segments % 2 == 0 :
                scale_bar.set_xticks(segList)
            else :
                shSegs = [v for i,v in enumerate(segList) if i % 2 == 0]
                miSegs = [v for i,v in enumerate(segList) if i % 2 == 1]
                scale_bar.set_xticks(shSegs)
                scale_bar.set_xticks(miSegs, minor=True)
    def add_legend(self, loc:tuple[float]|str = (0.05,0.05),
                   title:str = "图例", title_fontsize:str = "small",
                   style:str = "spiltbar", 
                   handleheight:float = 1.5,
                   frameon:bool = False) -> None :
        """
        添加图例
        """
        if style not in ["colorbar_v","colorbar_h","spiltbar"]:
            raise ValueError("style参数错误")
        if title_fontsize not in ['xx-small', 'x-small', 'small', 
                              'medium', 'large', 'x-large', 'xx-large'] :
            raise ValueError("title_fontsize参数错误")
        if isinstance(loc,str) and loc not in ['best','upper right','upper left','lower left',
                                               'lower right','right','center left','center right',
                                               'lower center','upper center','center'] :
            raise ValueError("loc参数错误")
        if style == "colorbar_v" :
            if isinstance(loc, tuple) :
                xloc = "lower left"
            else :
                xloc = loc
            cbax = inset_axes(self.__main_ax, 
                              width="3%", height="25%", loc=xloc,
                              axes_kwargs = {"frame_on" : frameon})
            if self.__plot_config["nbin"] is False :
                cmn = self.__cmap.colormap()
            else :
                cmn = self.__cmap.resampled(len(self.__plot_config["labels"]))
            cbfig = plt.colorbar(mcm.ScalarMappable(norm=self.__norm,cmap=cmn), cax=cbax)
            cbfig.set_label(title, fontsize = title_fontsize, rotation=270)
            xtick = np.array(self.__plot_config["bins"][:-1])
            xtick += int((xtick[1]-xtick[0])/2)
            cbfig.set_ticks(xtick, labels=self.__plot_config["labels"])
        elif style == "colorbar_h" :
            if isinstance(loc, tuple) :
                xloc = "lower left"
            else :
                xloc = loc
            cbax = inset_axes(self.__main_ax, 
                              width="25%", height="5%", loc=xloc,
                              axes_kwargs = {"frame_on" : frameon})
            if self.__plot_config["nbin"] is False :
                cmn = self.__cmap.colormap()
            else :
                cmn = self.__cmap.resampled(len(self.__plot_config["labels"]))
            cbfig = plt.colorbar(mcm.ScalarMappable(norm=self.__norm,cmap=cmn), 
                                 cax=cbax, ticks=self.__plot_config["bins"],
                                 orientation="horizontal")
            cbfig.set_label(title, fontsize = title_fontsize, loc="center")
        else :
            patches = []
            for color, label in zip(self.__cmap.getListColors(len(self.__plot_config["labels"])), 
                                    self.__plot_config["labels"]):
                patch = mpatches.Patch(fc=color, ec='k', lw=0.5, label=label)
                patches.append(patch)
            self.__main_ax.legend(
                handles=patches,
                loc=loc,
                frameon=frameon,
                handleheight=handleheight,
                fontsize=title_fontsize,
                title=title,
            )
    def __enter__(self) -> Self :
        return self
    def __exit__(self, exc_type, exc_value, exc_tb) -> None :
        self.close()
    def save(self, saveto:str|Path|None = None,
             transparent:bool = True) -> None :
        """
        保存图片
        """
        if saveto is None :
            sPlace = Path("./picture.png")
        else :
            sPlace = Path(saveto)
        fplt.savefig(sPlace, transparent=transparent)
    def show(self) -> None :
        """
        显示绘图结果
        """
        plt.show()
    def close(self) -> None :
        """
        关闭绘图窗口
        """
        plt.close(self.__fig)

def _set_axis_font(ax:mpl.axes.Axes, 
                    font:str, fontsize:float) -> None :
    for i in ax.get_ticklabels():
        i.set_fontsize(fontsize)
        i.set_fontname(font)

def _is_darkcolor(color:str|tuple|list|None = None, 
                  cmap:str|ColormapSZ|None = None, N:int|None = 10) -> bool|list[bool]|None :
    """
    判断颜色是否为深色
    """
    if color is None and cmap is None :
        return None
    else :
        if color is not None :
            if isinstance(color, list) :
                cList = [mcolor.to_rgb(i) for i in color]
            else :
                cList = [mcolor.to_rgb(color)]
            xList = [sum(np.array(i)*np.array([0.299,0.587,0.114]))*256 for i in cList]
            xList = [(True if i<128 else False) for i in xList]
            if len(xList) == 1 :
                xList = xList[0]
        if cmap is not None :
            if isinstance(cmap, str) :
                colormap = sns.palettes.get_colormap(cmap).resampled(N)
            else:
                colormap = cmap.resampled(N)
            cList = [mcolor.to_rgb(colormap(i)) for i in range(N)]
            xList = [sum(np.array(i)*np.array([0.299,0.587,0.114]))*256 for i in cList]
            xList = [(True if i<128 else False) for i in xList]
        return xList


class heatmapSZ(object) :
    """
    传统热力图。加上常用的图形组合。
    主要用于绘制热力图与分布图的组合方案，也可单纯作为热力图绘制使用。
    """
    def __init__(self, data:pd.DataFrame,
                 vmin:float|None = None, vmax:float|None = None, 
                 xlabel:str|None = None, ylabel:str|None = None,
                 cmap_name:tuple|str|ColormapSZ|None = None,
                 robust:bool = False, figsize:tuple = (16,9),
                 annot:any = None, fmt:str ='.2f', annot_kws:dict|None = None, 
                 linewidths:float = 0, linecolor:str|tuple = 'white',
                 add_plot_data:pl.DataFrame|pd.DataFrame|None = None,
                 add_plot_kws:dict|None = None,
                 cbar:bool = False, cbar_kws:dict|None = None, 
                 space:float = 0.025) -> None:
        """
        data: 数据表
        vmin, vmax: 热力图数据范围，可选设定，默认自动确定范围
        cmap_name: 颜色映射表名称，也可以为任意颜色。使用非ColormapSZ的颜色时，将启用seaborn的颜色系统。
        robust: 如果 True 和 vmin 或 vmax 不存在，则使用稳健分位数而不是极值计算颜色图范围。
        annot: 热力图上的数值，默认为None。
        fmt: 热力图上的数值格式，默认为'.2g'。
        annot_kws: 热力图上的数值设定，默认为None。
        linewidths: 热力图上的线宽，默认为0。
        linecolor: 热力图上的线颜色，默认为'white'。
        add_plot_data: 绘制额外数据，默认为None。
        add_plot_kws: 额外数据绘制设定，默认为None。
        space: 子图间距，默认0.025。
        """
        if cmap_name is not None :
            if isinstance(cmap_name, ColormapSZ) :
                cmap_name = cmap_name.colormap()
            else :
                try:
                    cmap_name = sns.light_palette(cmap_name, as_cmap=True)
                except :
                    raise ValueError("颜色映射`cmap_name`设定错误！")
        else :
            cmap_name = "YlGnBu"
        self.__fig = plt.figure(figsize=figsize)
        if add_plot_data is not None :
            self.__fig.subplots_adjust(wspace=space)
        mpl.rcParams["font.family"] = ["Source Han Sans SC","Segoe UI","Leelawadee UI"]
        self.__data = data
        self.__Labels = [i if i is not None else "" for i in (xlabel, ylabel)]
        self.__annot_kws = {"size": 23, "font":"Smiley Sans"}
        self.__annot_kws.update(annot_kws if annot_kws else {})
        annot_kws = self.__annot_kws
        self.__heatmap_config = {
            "vmin" : vmin, "vmax" : vmax,
            "cmap" : cmap_name,
            "robust" : robust,
            "annot" : annot, "fmt" : fmt, 
            "annot_kws" : annot_kws,
            "linewidths" : linewidths, "linecolor" : linecolor
        }
        self.__leftspan = 6
        self.__rightspan = 1
        if add_plot_data is None :
            self.__heatmap_config["cbar"] = cbar
            self.__heatmap_config["cbar_kws"] = cbar_kws
        else :
            self.__heatmap_config["cbar"] = False
            self.__heatmap_config["cbar_kws"] = None
        self.__xlabel_kws = {"font":'Source Han Sans SC', "fontsize":16}
        self.__ylabel_kws = {"font":'Source Han Sans SC', "fontsize":12}
        self.__title_kws = {"loc":(0.57,1.1),"fontstyle":{"font":'Source Han Sans SC', "fontsize":22}}
        self.__add_data = add_plot_data 
        self.__add_plot_type = "barplot"
        self.__add_plot_kws = {
            "plot_kws" : {"x":self.__data[self.__data.columns[0]].to_list(),
                          "hue":self.__data.index.to_list(),
                          "palette":"Blues_r",
                          "legend":False, "width":1,},
            "title" : "",
            "xlabelstyle" : {"pad":15, "font":'Source Han Sans SC', "fontsize":18},
            "label_type" : "center",
        }
        if add_plot_kws is not None :
            if "plot_kws" in add_plot_kws.keys() :
                self.__add_plot_kws["plot_kws"].update(add_plot_kws["plot_kws"])
                self.__add_plot_kws["plot_kws"]["x"] = self.__add_data[add_plot_kws["plot_kws"]["x"]].to_list()
            if "title" in add_plot_kws.keys() :
                self.__add_plot_kws["title"] = add_plot_kws["title"]
            if "xlabelstyle" in add_plot_kws.keys() :
                self.__add_plot_kws["xlabelstyle"].update(add_plot_kws["xlabelstyle"])
            if "label_type" in add_plot_kws.keys() :
                self.__add_plot_kws["label_type"] = add_plot_kws["label_type"]
    def set_heatmap_config(self, **kws) -> None :
        self.__heatmap_config.update(kws)
    def set_annot_config(self, **kws) -> None :
        """https://matplotlib.org/stable/api/text_api.html"""
        self.__annot_kws.update(kws)
        self.__heatmap_config["annot_kws"] = self.__annot_kws
    def set_xlabel_config(self, **kws) -> None :
        """https://matplotlib.org/stable/api/text_api.html"""
        self.__xlabel_kws.update(kws)
    def set_ylabel_config(self, **kws) -> None :
        """https://matplotlib.org/stable/api/text_api.html"""
        self.__ylabel_kws.update(kws)
    def set_title_config(self, **kws) -> None :
        """https://matplotlib.org/stable/api/text_api.html"""
        res = {}
        res.update(kws)
        if "loc" in kws :
            if kws["loc"].lower() in ["top","bottom","top left","bottom left"] :
                if kws["loc"].lower() == "top" :
                    res["loc"] = (0.57,1.1)
                if kws["loc"].lower() == "bottom" :
                    res["loc"] = (0.57,0)
                if kws["loc"].lower() == "top left" :
                    res["loc"] = (0,1.1)
                if kws["loc"].lower() == "bottom left" :
                    res["loc"] = (0,0)
            elif isinstance(kws["loc"],tuple) :
                res["loc"] = kws["loc"]
            else :
                raise ValueError("loc参数错误")
        self.__title_kws.update(res)
    def set_leftspan(self, span:int) -> None :
        self.__leftspan = span
    def set_rightspan(self, span:int) -> None :
        self.__rightspan = span
    def plot(self) -> None :
        if self.__add_data is not None :
            colsLen = self.__leftspan + self.__rightspan
            ax1 = plt.subplot2grid((1, colsLen), (0, 0), colspan=self.__leftspan)
            sns.heatmap(self.__data, ax=ax1, **self.__heatmap_config)
            ax1.set(xlabel=self.__Labels[0], ylabel=self.__Labels[1])
            ax1.xaxis.tick_top()
            ax1.xaxis.get_label().set(**self.__title_kws["fontstyle"])
            ax1.xaxis.set_label_coords(*self.__title_kws["loc"])
            ax1.yaxis.get_label().set(**self.__title_kws["fontstyle"])
            _set_axis_font(ax1.xaxis, **self.__xlabel_kws)
            _set_axis_font(ax1.yaxis, **self.__ylabel_kws)
            ax2 = plt.subplot2grid((1, colsLen), (0,self.__leftspan))
            if self.__add_plot_kws["label_type"]=="edge":
                colors = ["#000000"] * len(self.__add_plot_kws["plot_kws"]["hue"])
            else:
                colors = [("#000000" if i else "#000000") for i in _is_darkcolor(
                                                            cmap=self.__add_plot_kws["plot_kws"]["palette"],
                                                            N=len(self.__add_plot_kws["plot_kws"]["hue"]))]
            tax = getattr(sns,self.__add_plot_type)(ax=ax2, **self.__add_plot_kws["plot_kws"])
            for i,data in enumerate(tax.containers):
                ax2.bar_label(data,label_type=self.__add_plot_kws["label_type"],
                              fmt = "{{:{}}}".format(self.__heatmap_config["fmt"]), 
                              color=colors[i], **self.__annot_kws)
            ax2.set_title(self.__add_plot_kws["title"],
                          **self.__add_plot_kws["xlabelstyle"])
            ax2.set_axis_off()
        else :
            sns.heatmap(self.__data, ax=self.__fig.gca(), **self.__heatmap_config)
    def save(self, saveto:str|Path|None = None,
             transparent:bool = True) :
        """
        保存图片
        """
        if saveto is None :
            sPlace = Path("./picture.png")
        else :
            sPlace = Path(saveto)
        fplt.savefig(sPlace, transparent=transparent)
    def show(self) :
        """
        显示绘图结果
        """
        plt.show()
    def close(self) :
        """
        关闭绘图窗口
        """
        plt.close(self.__fig)

class worldHeatMap(object):
    """
    世界地图下的国家数据热力图
    使用 Cartopy 作为底层。
    输入参数：
    data:pl.DataFrame|pd.DataFrame, 输入数据，至少包含两个字段，第一个字段为国家名，第二个字段为数据值
    
    """
    def __init__(self, data:pl.DataFrame|pd.DataFrame):
        self.__data = data
        pass


if __name__ == "__main__" :
    import frykit.shp as fshp
    # 构建假数据
    provinces = fshp.get_cn_province_names()
    data = np.linspace(0, 100, len(provinces))
    data = pl.DataFrame({"province":provinces,"data":data})
    # 画图
    cmtest = chinaMap(data=data, place="province",value="data", vmin=-1)
    cmtest.set_configs(font = "Microsoft YaHei")
    cmtest.setting_colors(colormap="Blues")
    cmtest.preDrawing()
    cmtest.plot_province()
    cmtest.add_compass()
    cmtest.add_scalebar()
    cmtest.add_legend(style="colorbar_h")
    cmtest.save("D:/picture.png")
    cmtest.close()