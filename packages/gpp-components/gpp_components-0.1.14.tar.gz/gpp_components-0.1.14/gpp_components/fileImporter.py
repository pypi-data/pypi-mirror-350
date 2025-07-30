from .handleData import Response
import pandas as pd
import oracledb as odb
import sqlalchemy as sqla


class FileImporter:
    def __init__(self, jsonStr) -> None:
        self.jsonStr = jsonStr

    """
    {
      "file_name": "Dragon_Deviation",
      "file_path": "\\\\xmncc4engdb07.dhcp.apac.dell.com\\APCC",
      "file_type": "Excel",
      "file_extend":"xlsx",
      "row_split": "",
      "data_value": [],
      "host_name": "XMNCC4ENGDB010.dhcp.apac.dell.com:1521",
      "service_name":"mostpdb.apac.dell.com",
      "dsn":"",
      "user_name": "MOST",
      "password": "MOST_2020",
      "db_type": "Oracle",
      "table_name": "test_import",
      "sheet_name": "Sheet1",
      "model": "append",
      "header": 0,
      "skiprows": 0,
      "mapping_data": [{"source": "Original Part", "column_name": "ORDERNUM"},{"source": "lob_group", "column_name": "QTY"}],
      "before_script": "",
      "after_script": "",
      "extends_data":{
        "lob_group":"Client"
      }
    }
    """

    def importData(self):
        table_data = self.loadFile(self.jsonStr)
        # if not table_data.empty:
            # DB 操作
        res = self.executeDB(self.jsonStr, table_data)
        if res:
            return Response(success=False, msg=str(res), data=[])

        return Response(success=True, data=[])

    def executeDB(self, obj, table_data):
        """
        obj:{
            "db_type": "SQL",
            "host_name": "xmncc4engdb04.dhcp.apac.dell.com:1433/PCWebsite",
            "user_name": "sa",
            "password": "k9efQV0uNJ)Zz3CZ",
            "before_script": "ddd",
            "after_script": "",
        }
        table_data:[{"ORDERNUM":"11111","QTY":"333"}]
        """
        db_type = obj["db_type"]
        table_name = obj["table_name"]
        model = obj["model"]
        before_script = obj["before_script"]
        after_script = obj["after_script"]
        try:
            conn = self.connDB(obj)
            if db_type == "Oracle":
                # connect DB
                cur = conn.cursor()
                if before_script and before_script != "None":
                    cur.execute(before_script)
                if model == "Overall":
                    cur.execute(f"delete from {table_name}")

                if not table_data.empty:
                    rows = [tuple(x) for x in pd.DataFrame(table_data).values]
                    columns = [x for x in pd.DataFrame(table_data).keys()]
                    # 动态造insert 语句
                    sql_str = self.rebuildSQL(table_name, columns, db_type)
                    # rows:[(value1,value2)]
                    cur.executemany(sql_str, rows)
                if after_script and after_script != "None":
                    cur.execute(after_script)
                cur.close()
            elif db_type == "SQL":
                if before_script and before_script != "None":
                    conn.execute(sqla.text(before_script))
                if model == "Overall":
                    model = "replace"
                if not table_data.empty:
                    table_data = pd.DataFrame(table_data)
                    # table_data:DataFrame类型
                    # if_exists：replace 替换原有数据/append 新增数据/fail 默认；创建一个表，目标表存在就失败
                    # index:True 默认，新增一列索引
                    table_data.to_sql(table_name, conn, if_exists=model, index=False)
                if after_script and after_script != "None":
                    conn.execute(sqla.text(after_script))
            conn.commit()
            conn.close()
        except Exception as e:
            return str(e)

    # 连接DB
    def connDB(self, obj):
        """
        {
            "db_type": "Oracle",
            "host_name": "XMNCC4ENGDB010.dhcp.apac.dell.com:1521",
            "service_name":"mostpdb.apac.dell.com",
            "user_name": "MOST",
            "password": "MOST_2020",
            "dsn":""
        }
        """
        db_type = obj["db_type"]
        host_name = obj["host_name"]
        service_name = obj["service_name"]
        dsn = obj["dsn"]
        user_name = obj["user_name"]
        password = obj["password"]

        # 判断db
        if db_type == "Oracle":
            if dsn:
                conn = odb.connect(user=user_name, password=password, dsn=dsn)
            else:
                conn_str = f"{user_name}/{password}@{host_name}/{service_name}"
                conn = odb.connect(conn_str)
        elif db_type == "SQL":
            conn = sqla.create_engine(
                f"mssql+pymssql://{user_name}:{password}@{host_name}/{service_name}?charset=utf8"
            ).connect()

        return conn

    def rebuildSQL(self, table_name, columns, db_type):
        """
        table_name:
        columns:['ORDERNUM', 'QTY']
        output:
          insert into test_import(ORDERNUM,QTY)values(:1,:2)
        """
        # columns str
        col_str = ""
        # values str
        value_str = ""
        for j, key in enumerate(columns):
            if any(char.isspace() for char in key):
                if db_type == "Oracle":
                    col_str = col_str + '"' + key + '"'
                elif db_type == "SQL":
                    col_str = col_str + "[" + key + "]"
            else:
                col_str += key
            value_str += ":" + str((j + 1))
            # 最后一个不拼接','
            if j != len(columns) - 1:
                col_str += ","
                value_str += ","
        return f"insert into {table_name}({col_str}) values({value_str})"

    def loadFile(self, obj):
        """
        {
          file_name:xx,
          file_path:xx,
          file_extend:xx,
          file_type:xx,
          row_split:xx,
          quote:xx,
          data_value:xx,
          table_name:
          sheet_name:
          model:
          header:
          skiprows:
          mapping_data:[
            {
              source:
              column_name
            }
          ]
          ],
          "extends_data":{
            "lob_group":"Client"
          }
        }

        """

        file_type = obj["file_type"]
        if file_type == "Value":
            if "data_value" in obj:
                table_data = obj["data_value"]
            else:
                table_data = []
        else:
            try:
                file_name = obj["file_name"]
                file_extend = obj["file_extend"]
                file_name = f"{file_name}.{file_extend}"
                file_path = obj["file_path"]
                file_fullPath = f"{file_path}\\{file_name}"
                sheet_name = obj["sheet_name"]
                mapping_data = obj["mapping_data"]
                if "header" in obj:
                    header = obj["header"]
                else:
                    header = None
                if "skiprows" in obj:
                    skiprows = obj["skiprows"]
                else:
                    skiprows = None
                if file_type == "Excel":
                    sheet_name_data = pd.read_excel(
                        file_fullPath,
                        sheet_name=sheet_name,
                        skiprows=skiprows,
                        header=header,
                    )
                elif file_type == "CSV":
                    sheet_name_data = pd.read_csv(
                        file_fullPath,
                        header=header,
                        skiprows=skiprows,
                    )
                elif file_type == "TXT":
                    if "row_split" in obj:
                        row_split = obj["row_split"]
                    else:
                        row_split = ","
                    sheet_name_data = pd.read_csv(
                        file_fullPath,
                        skiprows=skiprows,
                        header=header,
                        sep=row_split,
                    )
                # 将所有 NaN 值替换为空字符串
                sheet_name_data = sheet_name_data.fillna("")
                if "extends_data" in obj:
                    extends_data = obj["extends_data"]
                else:
                    extends_data = dict()
                table_data = self.mergeData(sheet_name_data, mapping_data, extends_data)
            except pd.errors.EmptyDataError:
                table_data = pd.DataFrame()

            
        return table_data

    
    def mergeData(self, sheet_name_data, mapping_data, extends_data):
        """
        sheet_name_data:DataFrame Data
        mapping_data:[{"source":xx,"column_name":xx2}]
        """
        data1 = []
        # 如果新加值不存在file的，往dataframe新增
        if len(extends_data) > 0:
            for key in extends_data:
                sheet_name_data[key] = extends_data[key]

        columns_to_keep = []
        rename_columns = dict()

        for i in mapping_data:
            columns_to_keep.append(i["column_name"])
            rename_columns[i["source"]] = i["column_name"]
        # rename
        # 数字变成字符串
        sheet_name_data.rename(columns=lambda x: str(x), inplace=True)
        sheet_name_data.rename(columns=rename_columns, inplace=True)

        # 移除列list
        columns_to_remove = set(sheet_name_data.columns) - set(columns_to_keep)
        sheet_name_data = sheet_name_data.drop(columns=columns_to_remove)
        # 数据转成字符串
        data1 = sheet_name_data.astype(str)
        return data1
