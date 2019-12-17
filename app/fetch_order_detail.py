# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2019/12/17 17:05
# file_name : fetch_order_detail.py
import csv
import requests
import pymysql

order_url = "http://web.myt11.com/oms/order/findByPage"
detail_url_prefix = "http://web.myt11.com/oms/order/findOrderDetail?"
headers = {
    'sid': '338e7e4ea15a4ec18d02caa5182584de'
}
order_params = {"orderQueryDto": {"orderId": "", "receiver": "", "startTime": "2019-11-17 00:00:00",
                                  "endTime": "2019-12-17 23:59:59", "sendPay": "", "thanPrice": "", "storeId": "",
                                  "userId": "", "orderSource": "", "paymentWayId": "", "lessPrice": "", "state": "100",
                                  "mobile": "", "sku": ""}, "pageHelper": {"page": 1, "rows": 10}}

detail_params = {"orderId": "2120013300000065832",
                 "userMobile": "13466665886"}

flag = True
connection = pymysql.connect(host="192.168.186.135", user="root", password="Biefeng123!",
                             database="recosys")
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
with open("order_detail.csv", 'w', encoding='utf-8', newline="\n") as csv_file:
    response = requests.post(url=order_url, headers=headers, json=order_params)
    order_lsit = response.json()['data']['list']
    for order in order_lsit:
        detail_params['orderId'] = order['orderId']
        detail_url = detail_url_prefix + "orderId=" + str(order['orderId'])
        if "mobile" in order:
            detail_url = detail_url + "&userMobile=" + str(order['mobile'])
        detail_response = requests.get(url=detail_url, headers=headers)
        order_items = detail_response.json()['data']['orderDataDetail']['orderItems']
        for order_item in order_items:
            sql = "insert into order_detail (sku_id,order_id,sku_name) values (" + "'" + str(
                order_item['skuId']) + "'," + "'" + str(
                order['orderId']) + "'," + "'" + str(order_item['productName']) + "');"
            print(sql)
            cursor.execute(sql)
            connection.commit()

    # fields = list(detailList[0].keys())
    # fields.append('orderSource')
    # fields.append("refundTypeStr")
    # fields.append("refundType")
    # fields.append("remark")
    # writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=r" ")
    # writer.writeheader()
    # while flag:
    #     response = requests.post(url=url, headers=headers, json=parameters)
    #     detailList = response.json()['data']['list']
    #     if len(detailList) > 0 and parameters['pageNo'] <= 2000:
    #         for row in detailList:
    #             writer.writerow(row)
    #         parameters['pageNo'] = parameters['pageNo'] + 1
    #         print("-------------fetch date ,pageNO: " + str(parameters["pageNo"]))
    #     else:
    #         flag = False
