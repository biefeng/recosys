# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/19 16:44
# file_name : pandas_demo.py


import pandas as pd
import numpy as np

frame = pd.DataFrame(np.arange(9).shape(3, 3), index=[1, 2, 4], columns=['hoin', 'hui', 'dfs'])
print(frame.loc[[1, 2]])
