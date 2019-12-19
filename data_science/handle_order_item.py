# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/19 9:27
# file_name : handle_order_item.py

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime


def data_from_database():
    print("开始加载...")
    engine = create_engine("mysql+pymysql://t11developer:JYwl@2019@172.16.1.154/jy_order")
    start = datetime.now()
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_table("order_item", conn)
        print(data, [1, 2, 3])
    end = datetime.now()
    print("加载时间：" + str((end - start).seconds) + "S")
    return data


def data_from_csv():
    print("开始加载...")
    start = datetime.now()
    df = pd.read_csv("d:\\doc\\data\\order_item.csv", delimiter=" ", low_memory=False,
                     usecols=['sku_id', 'product_name', 'order_id'])
    end = datetime.now()
    print("加载时间：" + str((end - start).seconds) + "S")
    return df


if __name__ == '__main__':
    df = data_from_csv()
    print(df)
