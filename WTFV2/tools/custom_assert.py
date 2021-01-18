from WTFV2.tools.common import Common
from WTFV2.tools.util import DBUtil, LogUtil


class CustomAssert:

    logger = LogUtil.get_logger('util')

    @classmethod
    def write_result_to_db(cls, version, table, info, result_msg, error_msg, error_img_path):
        """
        将测试结果写入数据库中
        :param version: 当前测试版本
        :param table: 数据表
        :param info: 测试信息的字典形式
        :param result_msg: 结果信息
        :param error_msg: 错误信息
        :param error_img_path: 错误截图路径
        :return: None
        """
        case_version = version
        case_id = info["case_id"]
        module_name = info["module_name"]
        test_type = info["test_type"]
        api_url = info["api_url"]
        request_method = info["request_method"]
        case_desc = info["case_desc"]
        test_data = info["test_data"]
        expect = info["expect"]

        sql = f'insert into {table}(case_version,case_id,module_name,test_type,api_url,' \
              f'request_method,case_desc,test_data,expect,result_msg,error_msg,error_img_path) ' \
              f'values("{case_version}", "{case_id}", "{module_name}", "{test_type}",' \
              f'"{api_url}", "{request_method}", "{case_desc}", "{test_data}", "{expect}", ' \
              f'"{result_msg}","{error_msg}","{error_img_path}")'
        if not DBUtil.update('db_conn_info_result', sql):
            cls.logger.error('sql执行错误')


    @classmethod
    def assert_error(cls, version, table, info):
        """
        断言错误处理
        :param version: 版本名称
        :param table: 数据库表
        :param info: 测试信息
        :return: None
        """
        result_msg = 'test error'
        error_img_path = Common.get_screenshot(version)
        cls.write_result_to_db(version, table, info, result_msg, info['error_msg'] ,error_img_path)

    @classmethod
    def assert_equal(cls, version, actual, info, table):
        """
        断言相等处理
        :param version: 当前版本
        :param actual: 实际结果
        :param info: 测试信息
        :param table: 数据库表
        :return: None
        """
        if info['expect'] == actual:
            result_msg = 'test pass'
            error_msg = '无'
            error_img_path = '无'
        else:
            result_msg = 'test fail'
            error_msg = "无"
            error_img_path = Common.get_screenshot(version)

        cls.write_result_to_db(version, table, info, result_msg, error_msg, error_img_path)


    def assert_contain(self):
        pass
