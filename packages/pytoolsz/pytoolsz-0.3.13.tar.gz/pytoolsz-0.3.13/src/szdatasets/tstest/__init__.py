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
Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos,
The M4 Competition: 100,000 time series and 61 forecasting methods,
International Journal of Forecasting,
Volume 36, Issue 1,
2020,
Pages 54-74,
ISSN 0169-2070,
https://doi.org/10.1016/j.ijforecast.2019.04.014.
"""
TITLE       = """The M4 Competition"""
SOURCE      = """
https://autogluon.s3.amazonaws.com/datasets/timeseries/m4_hourly_subset/train.csv
"""

DESCRSHORT  = """
The M4 dataset was created on December 28, 2017, and contains 100,000 time series. 
It has been scaled to avoid negative values and has removed information that could 
lead to the identification of the original series, ensuring the objectivity of 
the results.
"""

DESCRLONG   = """
The M4 dataset was created on December 28th, 2017, when Professor Makridakis 
chose a seed number to randomly select the sample of 100,000 time series to 
be used in the M4. The selected series were then scaled to prevent negative 
observations and values lower than 10, thus avoiding possible problems when 
calculating various error measures. The scaling was performed by simply adding 
a constant to the series so that their minimum value was equal to 10 (29 occurrences 
across the whole dataset). In addition, any information that could possibly lead 
to the identification of the original series was removed so as to ensure the 
objectivity of the results. This included the starting dates of the series, 
which did not become available to the participants until the M4 had ended.
"""

#suggested notes
NOTE        = """
The M4 dataset consists of 100,000 time series of yearly, quarterly, monthly 
and other (weekly, daily and hourly) data, which are divided into training 
and test sets. The training set was made available to the participants at the 
beginning of the competition, while the test set was kept secret till its end, 
when it was released and used by the organizers for evaluating the submissions. 
The minimum numbers of observations in the training test are 13 for yearly, 
16 for quarterly, 42 for monthly, 80 for weekly, 93 for daily and 700 for 
hourly series. It is worth mentioning that M4 consists of much longer series 
than M3 on average, thus offering more opportunities for complicated methods 
that require large amounts of data for proper training.
"""


def data() -> szDataFrame :
    keypath = Path(__file__).parent / "testtrain.csv"
    return szDataFrame(keypath)