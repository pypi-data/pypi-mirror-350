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
from pytoolsz.frame import szDataFrame,zipreader

CITATION   = """
Fisher,R. A.. (1988). Iris. 
UCI Machine Learning Repository. 
https://doi.org/10.24432/C56C76.
"""
TITLE       = """Iris"""
SOURCE      = """
https://archive.ics.uci.edu/dataset/53/iris
"""

DESCRSHORT  = """
A small classic dataset from Fisher, 1936. 
One of the earliest known datasets used for 
evaluating classification methods. 
"""

DESCRLONG   = """
This is one of the earliest datasets used in the literature on classification methods 
and widely used in statistics and machine learning.  The data set contains 3 classes 
of 50 instances each, where each class refers to a type of iris plant.  
One class is linearly separable from the other 2; the latter are not linearly 
separable from each other.

Predicted attribute: class of iris plant.

This is an exceedingly simple domain.

This data differs from the data presented in Fishers article (identified 
by Steve Chadwick,  spchadwick@espeedaz.net ).  The 35th sample should be: 
4.9,3.1,1.5,0.2,"Iris-setosa" where the error is in the fourth feature. The 38th 
sample: 4.9,3.6,1.4,0.1,"Iris-setosa" where the errors are in the second and 
third features.  
"""

#suggested notes
NOTE        = """
Variables Table::

|Variable Name|Role|Type|Description|Units|Missing Values|
|------------|-----|-----|-----------|-----|--------------|
|sepal length|Feature|Continuous| |cm|no|
|sepal width|Feature|Continuous| |cm|no|
|petal length|Feature|Continuous| |cm|no|
|petal width|Feature|Continuous| |cm|no|
|class|Target|Categorical|class of iris plant: Iris Setosa, Iris Versicolour, or Iris Virginica|  |no|
"""


def data() -> szDataFrame :
    keypath = Path(__file__).parent / "iris.zip"
    return zipreader(keypath,"iris.data")