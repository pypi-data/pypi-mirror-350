from math import e
from urllib import response
import oracledb
from numpy import isin
from .response import Response
from copy import deepcopy


class RunOracle:
    def __init__(self, tns_config):
        self.tns_config = tns_config
        self.conn = False
        self.cursor = False
        self.qs = None
        self.connectOracle()
        pass

    def connectOracle(self):
        user = self.tns_config.get("user")
        password = self.tns_config.get("password")
        host = self.tns_config.get("host")
        service_name = self.tns_config.get("service_name")
        dsn = self.tns_config.get("dsn")

        conn_str = f"{user}/{password}@{host}/{service_name}"  # ('system/system@172.24.0.64:1521/helowinXDB')

        try:
            # self.conn = oracledb.connect(conn_str)
            self.conn = oracledb.connect(user=user, password=password, dsn=dsn)
        except Exception as e:
            return Response(False, "tns is not correct, connection fail !")

    def closeConnection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def runSql(self, sqlStr):
        try:
            if self.conn:
                self.cursor = self.conn.cursor()
                self.cursor.execute(sqlStr)
                col = [x[0] for x in self.cursor.description]
                self.qs = deepcopy(self.cursor.fetchall())
            else:
                return Response(False, f"No Connenct Found !")
        except oracledb.DatabaseError as e:
            return Response(False, f"Problem in runSql: {e}")
        finally:
            self.closeConnection()
            if self.qs:
                data = []
                for i in self.qs:
                    data.append(dict(zip(col, i)))
                return data
            else:
                return Response(False, f"No TNS Found, Pls check your targetDB Info !")

    def excuteSql(self, sqlStr):
        print(sqlStr)
        try:
            if self.conn:
                self.cursor = self.conn.cursor()
                self.cursor.execute(sqlStr)
                return Response(data=[])
            else:
                return Response(False, f"No Connenct Found !")
        except oracledb.DatabaseError as e:
            return Response(False, f"Problem in excuteSql: {e}")
        finally:
            self.closeConnection()

    def runProc(self, sp_name, jsonStr):
        try:
            if self.conn:
                # user = self.tns_config.get("user")
                # password = self.tns_config.get("password")
                # host = self.tns_config.get("host")
                # service_name = self.tns_config.get("service_name")

                # conn_str = f"{user}/{password}@{host}/{service_name}"  # ('system/system@172.24.0.64:1521/helowinXDB')
                # conn = oracledb.connect('MOST/MOST_2020@xmncc4engdb010.dhcp.apac.dell.com:1521/MOSTPDB')
                self.cursor = self.conn.cursor()
                v_output = self.cursor.var(oracledb.CLOB)
                self.cursor.callproc(sp_name, [str(jsonStr), v_output])
                result = deepcopy(v_output.getvalue())
                return result
            else:
                return Response(False, f"No Connenct Found !")
        except oracledb.DatabaseError as e:
            return Response(False, f"Problem in runProc: {e}")
        finally:
            self.closeConnection()
            # cursor.close()
            # conn.close()

    def getTNS(self, dbJson):
        host_name = dbJson.get("host_name")
        port = dbJson.get("port")
        container = dbJson.get("container")
        tb_space = dbJson.get("tb_space")

        # sqlStr = f"SELECT user_name, user_pwd, tns_content FROM DB_CONFIG WHERE host_name = '{host_name}' AND port = {port} AND container = '{container}' AND tb_space = '{tb_space}'"

        sqlStr = f"WITH tmp_data AS (SELECT pid, user_name, user_pwd, tns_content FROM DB_CONFIG WHERE host_name = '{host_name}' AND port = {port} AND container = '{container}' AND tb_space = '{tb_space}'),tmp_root AS (SELECT tns_content FROM DB_CONFIG WHERE ID = (SELECT pid FROM tmp_data)) SELECT a.user_name, a.user_pwd, NVL(a.tns_content, b.tns_content) AS tns_content FROM tmp_data a LEFT JOIN tmp_root b ON 1 = 1"

        try:
            rsp = self.runSql(sqlStr)
            if isinstance(rsp, Response):
                return rsp
            else:
                user_name = rsp[0].get("USER_NAME")
                user_pwd = rsp[0].get("USER_PWD")
                dsn = rsp[0].get("TNS_CONTENT")

                result = {
                    "user": user_name,
                    "password": user_pwd,
                    "host": host_name + ":" + str(port),
                    "service_name": container,
                    "dsn": dsn,
                }
                return result
        except Exception as e:
            return Response(False, f"Problem in getTNS, No TNS found !: {e}")
