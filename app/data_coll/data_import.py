# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/01/06 14:46
# file_name : data_import.py

import pymysql

connect = pymysql.connect(
    **{'host': '172.16.1.106', 'user': 't11developer', 'password': 'JYwl@2019', 'database': 'jy_catering'})
cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

cursor.execute("select user_id,sku_name from catering_task where shop_id = 12001 limit 10")

local = pymysql.connect(
    **{'host': '192.168.186.135', 'user': 'root', 'password': 'Biefeng123!', 'database': 'recosys'})

for e in cursor.fetchall():
    cursor.execute("insert into event")
