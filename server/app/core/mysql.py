import json
from django.db import connection
import numpy as np
import pandas as pd
import datetime


# 帮助方法,合并对象
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


# 帮助类：重写json类
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # 遇到日期特殊处理
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        # 遇到nparray特殊处理
        elif isinstance(
                obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray, )):
            return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)


# 帮助类：mysql请求池
class MysqlPool:
    def run(self, sql, values=None):
        """
        定义Mysql帮助类
        @param {String} sql SQL语句
        @param {List} values 值数组
        @return {Object} 返回执行结果
        """
        result = None
        if sql.find("SELECT") != -1:
            df = pd.read_sql(sql, connection)
            # 获取列名
            column_list = list(df.columns)
            df1 = list(np.array(df))
            lst = []
            for row in df1:
                # 循环每一行数据，组装成一个字典，然后得到字典的列表
                lst.append(dict(zip(column_list, row.tolist())))
            # 导入json,将列表转为json字符串
            # son.dumps序列化时候对中文默认使用的ascii编码，想要输出真正的中文需要指定ensure_ascii=False
            str1 = json.dumps(lst, cls=MyEncoder, ensure_ascii=False)
            # 再转回dict
            result = json.loads(str1)
        else:
            result = False
            cur = connection.cursor()
            cur.execute(sql)
            result = True
        return result

    def escapeId(self, str_1):
        """ 作用：将`去掉 """
        str_1 = str(str_1)
        return "`" + str_1.replace(r"/`/", "") + "`"

    def escape(self, str_1):
        """ 作用：将前后的'去掉 """
        str_1 = str(str_1)
        return "'" + str_1.replace(r"/'/", r"\'") + "'"

    def toWhere(self, queryDict={}, like=True):
        """
            转sql wehre语句
            @param {String} sql SQL语句
            @param {List} values 值数组
            @return {String} 返回执行结果
            """
        where = ""
        if like:
            for k in queryDict:
                val = queryDict[k]
                if(k.endswith("_min")):
                    where += " and `" + k.replace("_min", "") + "` >= " + self.escape(str(val))
                elif(k.endswith("_max")):
                    where += " and `" + k.replace("_max", "") + "` <= " + self.escape(str(val))
                elif isinstance(val, str):
                    where += (" and `" + k + "` LIKE '%" +
                              self.escape(val).strip("'") + "%'")
                elif isinstance(val, int):
                    where += " and `" + k + "`=" + str(val)
                else:
                    where += " and `" + k + "`=" + str(val)

        else:
            for k in queryDict:
                val = queryDict[k]
                if(k.endswith("_min")):
                    where += " and `" + k.replace("_min", "") + "` >= " + self.escape(str(val))
                elif(k.endswith("_max")):
                    where += " and `" + k.replace("_max", "") + "` <= " + self.escape(str(val))
                elif isinstance(val, str):
                    where += (" and `" + k + "` = '" +
                              self.escape(val).strip("'") + "'")
                elif isinstance(val, int):
                    where += " and `" + k + "`=" + str(val)
                else:
                    where += " and `" + k + "`=" + str(val)
        return where.replace(" and ", "", 1)

    def toOrWhere(self, queryDict={}, like=True):
        """
         转sql wehre语句
        @param {String} sql SQL语句
        @param {List} values 值数组
        @return {String} 返回执行结果
        """
        where = ""
        if like:
            for k in queryDict:
                val = queryDict[k]
                # type(val) == "<type 'str'>"
                if isinstance(val, str):
                    where += (" or `" + k + "` LIKE '%" +
                              self.escape(val).strip("'") + "%'")
                elif isinstance(val, int):
                    where += " or `" + k + "`=" + str(val)
                else:
                    where += " or `" + k + "`=" + str(val)

        else:
            for k in queryDict:
                where += " or " + self.escapeId(k) + "=" + self.escape(
                    queryDict[k])
        return where.replace(" or ", "", 1)

    def toSet(self, body):
        """
         转sql set语句
        @param {Dictionary} body 查询条件
        @return {String} sql语句
        """
        setData = ""
        for k in body:
            v = body[k]
            setData += ", `" + k + "`=" + self.escape(v)
        return setData.replace(", ", "", 1)

    def toAddSql(self, body, config):
        """
        转添加sql语句
        @param {Dictionary} body 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        if "table" in config:
            table = config["table"]
        key = ""
        val = ""
        for k in body:
            key += "," + self.escapeId(k)
            val += "," + self.escape(body[k])
        sql = "INSERT INTO `{0}` ({1}) VALUES ({2});"
        return (sql.replace("{0}", table).replace("{1}", key.replace(
            ",", "", 1)).replace("{2}", val.replace(",", "", 1)))

    def toDelSql(self, query={}, config={}):
        """
        转删除sql语句
        @param {Dictionary} body 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        if "table" in config:
            table = config["table"]
        where = self.toWhere(query, False)
        sql = "DELETE FROM `{0}` WHERE {1};"
        return sql.replace("{0}", table).replace("{1}", where)

    def toSetSql(self, query, body, config):
        """
        转修改sql语句
        @param {Dictionary} body 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        if "table" in config:
            table = config["table"]
        where = self.toWhere(query, False)
        setData = self.toSet(body)
        sql = "UPDATE `{0}` SET {1} WHERE {2};"
        return sql.replace("{0}",
                           table).replace("{1}",
                                          setData).replace("{2}", where)

    def toGetSql(self, query={}, config={}):
        """
        转查询sql语句
        @param {Dictionary} query 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        like = True
        where = groupby = orderby = size = page = ""
        sql = "SELECT {1} FROM `{0}`"
        if "table" in config:
            table = config["table"]
        if "orderby" in config:
            orderby = config["orderby"]
        if "field" in config:
            field = config["field"]
        else:
            field = "*"
        if "page" in config:
            page = int(config["page"])
        if "size" in config:
            size = int(config["size"])
        if "like" in config:
            like = config["like"]
        if "groupby" in config:
            groupby = config["groupby"]
        where = self.toWhere(query, like)
        if where:
            sql += " WHERE " + where
        if groupby:
            sql += " GROUP BY " + groupby.replace(r"/;/", "")
        if orderby:
            sql += " ORDER BY " + orderby.replace(r"/;/", "")

        sql = sql.replace("{0}", table).replace("{1}", field)
        if size and page:
            start = size * (page - 1)
            sql += " limit " + str(start) + "," + str(size)
        return sql

    def toCountSql(self, query={}, config={}):
        """
        查询符合结果总数
        @param {Dictionary} query 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        groupby = ""
        if "table" in config:
            table = config["table"]
        if "groupby" in config:
            groupby = config["groupby"]
        sql = "SELECT count(*) count FROM `" + table + "`"
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        # 用户组
        if groupby:
            sql = sql.replace("count(", groupby + ",count(")
            if "groupby" in query:
                query.pop("groupby")
            sql += " GROUP BY " + groupby
        return sql

    def toSumSql(self, query={}, config={}):
        """
        查询结果总数合计
        @param {Dictionary} query 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        groupby = ""
        where = ""
        if "table" in config:
            table = config["table"]
        if "field" in config:
            field = config["field"]
        if "groupby" in config:
            groupby = config["groupby"]
        sql = "SELECT sum(" + self.escapeId(
            field) + ") sum FROM `" + table + "`"
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        if groupby:
            sql = sql.replace("sum(", groupby + ",sum(")
            if "groupby" in query:
                query.pop("groupby")
            sql += " GROUP BY" + self.escapeId(groupby)

        return sql

    def toAvgSql(self, query={}, config={}):
        """
        查询结果平均数
        @param {Dictionary} query 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        groupby = ""
        if "table" in config:
            table = config["table"]
        if "field" in config:
            field = config["field"]
        if "groupby" in config:
            groupby = config["groupby"]
        sql = "SELECT avg(" + self.escapeId(
            field) + ") avg FROM `" + table + "`"
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        if groupby:
            sql = sql.replace("avg(", groupby + ",avg(")
            if "groupby" in query:
                query.pop("groupby")
            sql += " GROUP BY" + self.escapeId(groupby)
        return sql

    # 计算日期
    def toDateComput(self, query={}, config={}):
        """
        计算日期
        @param {Dictionary} query 查询条件
        @param {Dictionary} config 配置
        @return {String} sql语句
        """
        date_key = "create_time"
        method = "count"
        field = "*"
        size = 0
        format_t = r"%Y-%m-%d"
        if "date_key" in config:
            date_key = config["date_key"]
        if "method" in config:
            method = config["method"]
        if "field" in config:
            field = config["field"]
        if "size" in config:
            size = config["size"]
        if "format" in config:
            format_t = config["format"]
        if "table" in config:
            table = config["table"]
        sql = ("SELECT DATE_FORMAT(`" + date_key + "`, '" + format_t +
               "') `date`, " + method + "(" + field + ") " + method +
               " FROM `" + table + "`")
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        sql += " GROUP BY `date` ORDER BY `date` desc"
        if size:
            sql += " limit 0," + str(size)
        return sql


mysqlPool = MysqlPool()


# 服务器父类
class Service:
    error = {"code": 0, "message": "", "sql": ""}

    def __init__(self, config):
        """
        构造函数
        @param {Dictionary} config 配置参数
        """
        config_temp = {
            "table": "",
            "page": 1,
            "size": 30,
        }
        self.config = obj_update(config_temp, config)

    def run(self, sql, values=None):
        """
        执行sql服务
        @param {String} query SQL语句
        @param {Dictionary} values 对应值
        @return {Array} 返回执行结果
        """
        ret = None
        try:
            self.error = None
            ret = mysqlPool.run(sql, values=None)
        except Exception as e:
            self.error = {"code": 0, "message": str(e), "sql": sql}
            return False
        else:
            if sql.find("SELECT") != -1:
                if ret is None:
                    ret = []
            return ret

    def Add(self, body={}, config={}):
        """
        增
        @param {Dictionary} query 查询条件
        @return {String} 返回成功信息
        """
        sql = mysqlPool.toAddSql(body, obj_update(self.config, config))
        ret = self.run(sql)
        return ret

    def Del(self, query={}, config={}):
        """
        删
        @param {Dictionary} query 查询条件
        @return {String} 返回成功信息
        """
        sql = mysqlPool.toDelSql(query, obj_update(self.config, config))
        ret = self.run(sql)
        return ret

    def Set(self, query={}, body={}, config={}):
        """
        修
        @param {Dictionary} query 查询条件
        @return {String} 返回成功信息
        """
        sql = mysqlPool.toSetSql(query, body, obj_update(self.config, config))
        ret = self.run(sql)
        return ret

    def Get_list(self, query={}, config={}):
        """
        查一条
        @param {Dictionary} query 查询条件
        @return {Array} 返回列表
        """
        sql = mysqlPool.toGetSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Get_obj(self, query={}, config={}):
        """
        查多条
        @param {Dictionary} query 查询条件
        @return {Array} 返回列表
        """
        sql = mysqlPool.toGetSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]
        return None

    def Count(self, query={}, config={}):
        """
        统计查询结果数
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = mysqlPool.toCountSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]["count"] or 0
        return 0

    def Sum(self, query={}, config={}):
        """
        合计字段值
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = mysqlPool.toSumSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]["sum"] or 0
        return 0

    def Avg(self, query={}, config={}):
        """
        求平均数
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = mysqlPool.toAvgSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]["avg"] or 0
        return 0

    def Count_group(self, query={}, config={}):
        """
        分组求总数
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = mysqlPool.toCountSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Sum_group(self, query={}, config={}):
        """
        分组求合
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = mysqlPool.toSumSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Bar_group(self, query={}, config={}):
        """
        分组求合
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sum_list = ''
        where = ''
        for o in config['field'].split(','):
            sum_list += ",sum(" + o + ")"
        if "like" in config:
            like = config["like"]
            where = " WHERE " + self.toWhere(query, like)
        sql = "SELECT " + config['groupby'] + sum_list + " FROM " + self.config["table"] + where + " GROUP BY " + config['groupby']
        return self.run(sql)

    def Avg_group(self, query={}, config={}):
        """
        分组求平均数
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = mysqlPool.toAvgSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Prev(self, key, value):
        """
        获取上一条
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = ("SELECT * FROM `" + self.config["table"] + "` WHERE `" +
               str(key) + "`<" + str(value) + " ORDER BY `" + str(key) +
               "` DESC limit 0,10;")
        return self.run(sql)

    def Next(self, key, value):
        """
        获取下一条
        @param {Dictionary} query 查询条件
        @return {Array} 返回条数
        """
        sql = ("SELECT * FROM `" + self.config["table"] + "` WHERE `" +
               str(key) + "`>" + str(value) + " limit 0,10;")
        return self.run(sql)

    def date_comput(self, query={}, config={}):
        sql = mysqlPool.toDateComput(query, obj_update(query, {"table": self.config["table"]}), config)
        return self.run(sql)

    # 导入
    def Import_db(self, data, config):
        pass

    # 导出
    def Export_db(self, query={}, config={}):
        # 数据库语言
        sql = mysqlPool.toGetSql(query, obj_update(self.config, config))
        df = pd.read_sql(sql, connection)
        # 获取列名
        column_list = list(np.array(df.columns))
        df1 = list(np.array(df))
        lst = []
        lst.append(column_list)
        for row in df1:
            lst.append(row)
        # json.dumps转换时间格式
        str1 = json.dumps(lst, cls=MyEncoder, ensure_ascii=False)
        # 再转回lst
        lst = json.loads(str1)
        return lst

    # 是否已有
    def Has(self, query={}, config={}):
        sql = mysqlPool.toOrWhere(query)
        df = pd.read_sql(sql, connection)
        return df == True