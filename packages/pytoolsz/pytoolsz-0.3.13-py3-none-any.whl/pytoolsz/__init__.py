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

from pytoolsz.frame import (
    getreader,
    just_load,
    szDataFrame,
    zipreader
)
import szdatasets as datasetsz
import pytoolsz.pretools as pretools
import pytoolsz.compress as compress
import pytoolsz.handlepath as handlepath
import pytoolsz.ppTrans as ppTrans
import pytoolsz.utils as utils
import pytoolsz.graph as graph
import pytoolsz.tsTools as tsTools
import pytoolsz.forecast as forecast
from pytoolsz.saveExcel import (
    saveExcel,
    transColname2Letter
)

__version__ = "0.3.13"

def version(println:bool = True, 
            output:bool = False) -> str|None:
    version_txt = [
        "0.3.13 (2025-05-23)",
        "Copyright (c) 2024 Sidney Zhang <zly@lyzhang.me>",
        "PyToolsz is licensed under Mulan PSL v2."
    ]
    if println :
        print("\n".join(version_txt))
    if output :
        return "\n".join(version_txt)

__all__ = [
    "pretools",
    "handlepath",
    "compress",
    "forecast",
    "datasetsz",
    "getreader",
    "just_load",
    "ppTrans",
    "tsTools",
    "szDataFrame",
    "zipreader",
    "saveExcel",
    "transColname2Letter",
    "graph",
    "utils",
    "version"
]

if __name__ == "__main__":
    from pytoolsz.utils import print_special
    version()
    print_special(datasetsz.iris.NOTE, mode="markdown")
    print(datasetsz.iris.data())