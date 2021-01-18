from WTFV2.tools.util import DBUtil, LogUtil, TimeUtil


class Report:

    logger = LogUtil.get_logger('report')
    db_info = 'db_conn_info_result'
    @classmethod
    def generate_html_test_report(cls, table, version, app_name):

        sql = f'select * from {table} where case_version="{version}"'
        result = DBUtil.query_all(cls.db_info, sql)
        if len(result) == 0:
            cls.logger.info('该版本没有测试结果')
            return

        with open('../report/template.html', encoding='utf8') as file:
            contents = file.read()

        base_sql = f'select count(*) from {table} where case_version="{version}" and result_msg='
        count_success_sql = base_sql + "\"test pass\""
        count_fail_sql = base_sql + "\"test fail\""
        count_error_sql = base_sql + "\"test error\""

        count_sccess = DBUtil.query_one(cls.db_info, count_success_sql)[0]
        count_fail = DBUtil.query_one(cls.db_info, count_fail_sql)[0]
        count_error = DBUtil.query_one(cls.db_info, count_error_sql)[0]

        last_time_sql = f'select case_time from {table} ORDER BY case_time DESC limit 0,1;'
        last_time = DBUtil.query_one(cls.db_info, last_time_sql)[0]
        test_date = str(last_time).split(' ')[0]
        test_time = str(last_time).split(' ')[1]

        # 对固定的内容进行替换
        contents = contents.replace('$test-date', test_date)
        contents = contents.replace('$test-version', version)
        contents = contents.replace('$pass-count', str(count_sccess))
        contents = contents.replace('$fail-count', str(count_fail))
        contents = contents.replace('$error-count', str(count_error))
        contents = contents.replace('$last-time', test_time)
        test_result = ''
        color = ''
        for content in result:
            if content[10] == 'test pass':
                color = 'green'
            elif content[10] == 'test fail':
                color = 'yellow'
            else:
                color = 'red'
            test_result += f'<tr height="40">' \
                           f'<td width="7%">' \
                          f'{str(content[0])}</td>' \
                          f'<td width="9%">{content[3]}</td>' \
                          f'<td width="9%">{content[4]}</td>' \
                          f'<td width="7%">{content[2]}</td>' \
                          f'<td width="20%">{content[7]}</td>' \
                          f'<td width="7%" bgcolor={color}>{content[10]}</td>' \
                          f'<td width="16%">{content[11]}</td>' \
                          f'<td width="15%">{content[12]}</td>' \
                          f'<td width="10%"><a href={content[13]}>查看截图</a></td>' \
                           f'</tr>'
        contents = contents.replace('$test-result', test_result)
        # woniubossV1.0版本测试报告_20210115.html
        report_name = f'../report/{app_name}{version}版本测试报告_{TimeUtil.get_date()}.html'

        with open(report_name, 'w', encoding='utf8') as file:
            file.write(contents)


if __name__ == '__main__':

    Report().generate_html_test_report('woniuboss_test_result', 'V1.0', 'woniuboss')
