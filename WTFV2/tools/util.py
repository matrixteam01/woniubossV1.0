

import os
import time
import configparser

class LogUtil:

    # 单例模式
    logger = None

    @classmethod
    def get_logger(cls, module_name):

        """
        获取logger对象
        :param module_name: 一般可以放调用该对象的模块的字符串名称
        :return:logger对象
        """
        import logging
        if cls.logger is None:
            cls.logger = logging.getLogger(module_name)
            # 普通有4种信息级别：error,warn,info,debug
            cls.logger.setLevel(level=logging.INFO)

            # 判断logs路径是否存在，如果不存在则创建它
            if not os.path.exists('..\\logs') :
                os.mkdir('..\\logs')

            # 获取时间字符串
            ctime = TimeUtil.get_file_time()
            # 拼接日志文件的名称
            log_name = f'..\\logs\\{module_name}.{ctime}.log'
            # 创建句柄，用于和文件的关联
            handle = logging.FileHandler(log_name, encoding='utf8')
            # 定义日志信息的保存格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # 句柄具有规定的格式
            handle.setFormatter(formatter)
            cls.logger.addHandler(handle)
            cls.logger.info('**********************************************************\n')
        return cls.logger

class TimeUtil:

    @classmethod
    def get_file_time(cls):
        """
        按格式获取当前系统时间，一般用于拼接文件名
        :return: 当前时间的字符串
        """

        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

    @classmethod
    def get_date(cls):

        return cls.get_file_time().split('_')[0]



class FileUtil:

    logger = LogUtil.get_logger('util')

    @classmethod
    def get_version(cls, path):
        """
        获取某个应用的当前测试版本
        :param path: 版本信息所在的excel数据文件路径
        :return: 版本名称
        """
        import xlrd
        workbook = xlrd.open_workbook(path)
        sheet_content = workbook.sheet_by_name('caseinfo')
        return sheet_content.cell(1, 1).value

    @classmethod
    def get_contents_by_line_text(cls, path):
        """
        从文本文件中按行读取所有内容
        :param path: 文本文件的路径
        :return: 元素为字符串的列表
        """

        li = []
        contents = None
        try:
            with open(path, encoding='utf-8') as file:
                contents = file.readlines()
            for content in contents:
                li.append(content.strip())
        except Exception as e:
            cls.logger.error(f'{path}错误，文件读取失败')

        return li

    @classmethod
    def get_json(cls, path):
        """
        从json文件中读取内容并返回
        :param path: json文件路径
        :return: 文件的json内容
        """
        import json5
        contents = None
        try:
            with open(path, encoding='utf-8') as file:
                contents = json5.load(file)
        except Exception as e:
            cls.logger.error(f'{path}错误，文件读取失败')

        return contents

    @classmethod
    def get_ini_by_section(cls, path, section):

        """
        从ini文件中根据节点读取节点中的所有内容
        :param path:ini文件的路径
        :param section:节点的名称
        :return:节点下内容的原始数据类型
        """
        contents = None
        cp = configparser.ConfigParser()
        try:
            cp.read(path, encoding='utf-8')
            contents = cp.items(section)
        except Exception as e:
            cls.logger.error(f'读取{path}的{section}节点内容错误')

        return contents

    @classmethod
    def get_ini_value(cls, path, section, option):
        """
        从ini配置文件中读取某个节点section下某个键option对应的值
        :param path:ini文件的路径
        :param section:节点的名称
        :param option:节点下的某个键
        :return:ini文件中section节点下option对应的值的原始数据类型
        """
        cp = configparser.ConfigParser()
        content = None
        try:
            cp.read(path, encoding='utf-8')
            content = eval(cp.get(section, option))
        except Exception as e:
            cls.logger.error(f'读取{path}下的{section}节点中的{option}错误')

        return content

    # 传递一个列表+元组格式的对象，转化为json格式
    @classmethod
    def trans_tuple_to_dict(cls, contents):
        """
        将列表+元组格式的数据转化为json格式数据
        :param contents:列表+元组格式的数据
        :return:json格式数据
        """
        di = {}
        try:
            for c in contents:
                di[c[0]] = c[1]
        except Exception as e:
            cls.logger.error(f'{conents}内容错误')

        return  di


    @classmethod
    def get_excel(cls, path, section):
        """
        从excel中读取所有的测试信息
        :param path: 测试信息的配置文件路径
        :param section: 功能的节点名
        :return: json格式的测试信息
        """
        import xlrd
        test_info = cls.get_ini_by_section(path, section)
        test_info = cls.trans_tuple_to_dict(test_info)
        workbook = xlrd.open_workbook(test_info['test_data_path'])
        contents = workbook.sheet_by_name(test_info['sheet_name'])
        all = []
        for i in range(int(test_info['start_row']), int(test_info['end_row'])) :
            temp = {}
            temp['case_id'] = contents.cell(i, 0).value
            temp['module_name'] = contents.cell(i, 1).value
            temp['test_type'] = contents.cell(i, 2).value
            temp['api_url'] = contents.cell(i, 3).value
            temp['request_method'] = contents.cell(i, 4).value
            temp['case_desc'] = contents.cell(i, 5).value
            temp['expect'] = contents.cell(i, 7).value
            data = contents.cell(i, 6).value
            tl = str(data).split('\n')
            data_dict = {}
            for t in tl:
                data_dict[t.split('=')[0]] = t.split('=')[1]
            temp['test_data'] = data_dict
            all.append(temp)
        return all

class DBUtil:

    logger = LogUtil.get_logger('util')
    @classmethod
    def get_conn(cls, option):
        """
        根据配置文件的option获取对应数据库的连接
        :param option: base.ini文件中db_info节点下的键
        :return:
        """
        import pymysql
        conn = None
        try:
            db_conn_info = FileUtil.get_ini_value('..\\conf\\base.ini', 'db_info', option)
            conn = pymysql.connect(db_conn_info[0], db_conn_info[1],
                            db_conn_info[2], db_conn_info[3],
                            charset=db_conn_info[4])
        except Exception as e:
            cls.logger.error(u'数据库连接失败')

        return conn

    @classmethod
    def query_one(cls, option, sql):
        """
        查询一条记录，返回一条结果
        :param option: key
        :param sql: 要执行的sql语句
        :return: 记录的一维元组
        """

        result = None
        conn = cls.get_conn(option)

        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                result = cursor.fetchone()
            except Exception as e:
                cls.logger.error(f'{sql}语句错误，执行失败')
            cursor.close()
        else:
            cls.logger.error(u'数据库连接失败')
        conn.close()
        return result




    @classmethod
    def query_all(cls, option, sql):
        """
        查询多条记录，返回多条记录
        :param option: key
        :param sql: 要执行的sql
        :return: 记录的二维元组
        """
        result = None
        conn = cls.get_conn(option)

        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
            except Exception as e:
                cls.logger.error(f'{sql}语句错误，执行失败')
            cursor.close()
        else:
            cls.logger.error('数据库连接失败')
        conn.close()
        return result

    @classmethod
    def update(cls, option, sql):
        """
        执行增删改操作，返回操作是否成功的标识
        :param option:key
        :param sql:要执行的增删改sql
        :return:True或False
        """
        conn = cls.get_conn(option)
        flag = False
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
                flag = True
            except Exception as e:
                cls.logger.error(f'{sql}语句错误，执行失败')
            cursor.close()
        else:
            cls.logger.error('数据库连接失败')
        conn.close()
        return flag






if __name__ == '__main__':

    print(FileUtil.get_excel('..\\data\\case_data_conf.ini', 'add_resource'))



