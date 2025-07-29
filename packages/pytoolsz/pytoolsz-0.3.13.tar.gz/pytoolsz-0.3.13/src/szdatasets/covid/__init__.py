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
from pytoolsz.frame import szDataFrame

CITATION   = """
Mathieu, E., Ritchie, H., Ortiz-Ospina, E. et al. A global database of COVID-19 vaccinations. 
Nat Hum Behav (2021). 
https://doi.org/10.1038/s41562-021-01122-8

All visualizations, data, and code produced by _Our World in Data_ are completely open access 
under the [Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/). 
You have the permission to use, distribute, and reproduce these in any medium, 
provided the source and authors are credited.
"""
TITLE       = """Covid-19"""
SOURCE      = """
https://github.com/owid/covid-19-data/tree/master/public/data
"""

DESCRSHORT  = """
shortened version of our complete dataset with only the latest value for each location and metric
 (within a limit of 2 weeks in the past). This file is available in CSV, XLSX, and JSON formats.
"""

DESCRLONG   = """
The /public path of this repository is hosted at https://covid.ourworldindata.org/. For example, 
you can access the CSV for the complete dataset at https://covid.ourworldindata.org/data/owid-covid-data.csv 
or the CSV with latest data at https://covid.ourworldindata.org/data/latest/owid-covid-latest.csv. 
Note that latest data file only contains data up to 4 weeks prior the file update date.

We have the goal to keep all stable URLs working, even when we have to restructure this repository. 
If you need regular updates, please consider using the covid.ourworldindata.org URLs rather than 
pointing to GitHub.The /public path of this repository is hosted at https://covid.ourworldindata.org/. 
For example, you can access the CSV for the complete dataset at 
https://covid.ourworldindata.org/data/owid-covid-data.csv or the CSV with latest data at 
https://covid.ourworldindata.org/data/latest/owid-covid-latest.csv. Note that latest data file only 
contains data up to 4 weeks prior the file update date.

We have the goal to keep all stable URLs working, even when we have to restructure this repository. 
If you need regular updates, please consider using the covid.ourworldindata.org URLs rather than 
pointing to GitHub.
"""

#suggested notes
NOTE        = """
data informations :

https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-codebook.csv

Update **20240826**
"""


def data() -> szDataFrame :
    keypath = Path(__file__).parent / "covid.csv"
    return szDataFrame(keypath)