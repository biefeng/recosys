# *- coding=utf-8 -*
# /bin/bash
import getopt
import sys
from csv import DictWriter

import pymysql
from xlwt import Workbook, XFStyle, Font, Borders, Pattern, Style, Alignment

DEV = {'host': '10.128.62.33', 'user': 'root', 'password': 'root', 'database': 'jy_catering'}
PROD = {'host': '172.16.1.106', 'user': 't11developer', 'password': 'JYwl@2019', 'database': 'jy_catering'}

BASE_WIN_OUTPUT_PATH = 'd:/'
profiles = {'dev': DEV, 'prod': PROD}


class Export:
    def export_to_csv(self, **kwargs):
        limit = 10000
        count = self.get_data_scale(**kwargs)['count']
        print("***************************************共计：d%条", count)
        times = (count + limit - 1) // limit

        add_header = False
        dict_writer = None
        with open('result.csv', 'w', newline='') as csvfile:
            for i in range(times):
                kwargs["startIndex"] = i * limit + 1
                # kwargs['endIndex'] =(i + 1) * limit
                kwargs['endIndex'] = limit
                print("第%d条至第%d条", kwargs["startIndex"], (i + 1) * limit)

                records = self.get_data(**kwargs)
                column_names = []
                for data in records:
                    if not add_header:
                        for column_name in data.keys():
                            column_names.append(column_name)
                        add_header = True
                        dict_writer = DictWriter(csvfile, fieldnames=column_names, delimiter=" ")
                        dict_writer.writeheader()
                    dict_writer.writerow(data)

    def export_to_inserts(self, **kwargs):
        prop = {'host': '192.168.186.135', 'user': 'root', 'password': 'Biefeng123!', 'database': 'recosys'}
        insert_connection = pymysql.connect(host=prop['host'], user=prop['user'], password=prop['password'],
                                            database=prop['database'])
        insert_cursor = insert_connection.cursor(cursor=pymysql.cursors.DictCursor)

        limit = 10000
        count = self.get_data_scale(**kwargs)['count']
        print("***************************************共计：d%条", count)
        times = (count + limit - 1) // limit

        init = False
        insert_sql = ""

        with open('result.sql', 'w', encoding="utf-8") as sqlfile:
            for i in range(times):
                kwargs["startIndex"] = i * limit + 1
                # kwargs['endIndex'] =(i + 1) * limit
                kwargs['endIndex'] = limit
                print("第%d条至第%d条", kwargs["startIndex"], (i + 1) * limit)

                records = self.get_data(**kwargs)
                column_names = []
                for data in records:
                    if not init:
                        insert_sql = "insert into " + kwargs['tableName'] + "("
                        for column_name in data.keys():
                            insert_sql = insert_sql + column_name + ","
                        init = True
                        insert_sql = insert_sql[:len(insert_sql) - 1] + ") values ("
                        print(insert_sql)
                    temp = insert_sql
                    for (key, value) in data.items():

                        if value is None:
                            temp = temp + "NULL" + ","
                        else:
                            temp = temp + "'" + str(value) + "'" + ","
                    temp = temp[:len(temp) - 1] + ");\r\n"
                    # print(temp)
                    insert_cursor.execute(temp)
                    insert_connection.commit()
                    try:
                        sqlfile.write(temp)
                    except Exception as e:
                        print(e)

    def export_to_excel(self, **kwargs):
        work_book = Workbook(encoding="ascii")
        center_alignment = Alignment()
        center_alignment.horz = Alignment.HORZ_RIGHT
        center_alignment.vert = Alignment.VERT_CENTER

        border = Borders()
        border.top = Borders.THIN
        border.left = Borders.THIN
        border.bottom = Borders.THIN
        border.right = Borders.THIN

        head_style = XFStyle()

        head_pattern = Pattern()
        head_pattern.pattern = Pattern.SOLID_PATTERN
        head_pattern.pattern_fore_colour = Style.colour_map['gray25']

        head_style.pattern = head_pattern

        head_font = Font()
        head_font.bold = True
        head_style.font = head_font

        head_style.alignment = center_alignment
        head_style.borders = border

        data_style = XFStyle()
        data_style.alignment = center_alignment
        data_style.borders = border
        work_sheet = work_book.add_sheet("Sheet")
        limit = 10000
        count = self.get_data_scale(**kwargs)['count']
        times = (count + limit - 1) // limit
        add_header = False
        for i in range(1):
            kwargs["startIndex"] = i * limit + 1
            kwargs['endIndex'] = (i + 1) * limit + 1

            records = self.get_data(**kwargs)

            column_names = []
            y = 0
            for data in records:
                if not add_header:
                    x = 0
                    for column_name in data.keys():
                        work_sheet.write(y, x, column_name, head_style)
                        column_names.append(column_name)
                        x += 1
                    add_header = True
                    y += 1
                x = 0
                for column_name in column_names:
                    work_sheet.write(y, x, data[column_name], data_style)
                    x += 1
                y += 1
                x = 0

        work_book.save(BASE_WIN_OUTPUT_PATH + "result.xls")

    @staticmethod
    def get_cursor(**kwargs):
        # connection = pymysql.connect(host="10.128.62.33", usser="root", password="root", database="jy_catering")
        connection = pymysql.connect(host=kwargs['host'], user=kwargs['user'], password=kwargs['password'],
                                     database=kwargs['database'])
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor

    def get_data(self, **kwargs):
        cursor = self.get_cursor(**kwargs)
        # sql = "select * from " + kwargs['table'] + ' limit ' + str(kwargs['startIndex']) + "," + str(kwargs['endIndex'])
        sql = 'select * from (' + kwargs['sql'] + ')tmp limit ' + str(
            kwargs['startIndex']) + "," + str(kwargs['endIndex'])
        cursor.execute(sql)
        return cursor.fetchall()

    def get_data_scale(self, **kwargs):
        cursor = self.get_cursor(**kwargs)
        sql = "select count(1) count from (" + kwargs['sql'] + ") tmp"
        cursor.execute(sql)
        return cursor.fetchone()

    def export(self):
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, "hd:s:p:")
        props = {"profiles": "dev"}
        for opt, arg in opts:
            if opt == '-h':
                print("python export_to_excel.py -d <database> -s <sql> -p <profile> ")
                sys.exit(1)
            elif opt == '-d':
                profiles[props['profiles']]['database'] = props['database']
            elif opt == '-s':
                props['sql'] = arg
            elif opt == '-p':
                props['profiles'] = arg
            elif opt == '-o':
                props['output_path'] = arg
        profiles[props['profiles']]['sql'] = props['sql']

        self.export_to_csv(**profiles[props['profiles']])


if "__main__" == __name__:
    e = Export()
    prop = PROD
    prop['sql'] = "select * from catering_task order by order_time"
    prop['tableName'] = "catering_task"
    e.export_to_inserts(**prop)
