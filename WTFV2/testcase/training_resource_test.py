import traceback

from WTFV2.tools.custom_assert import CustomAssert
from WTFV2.tools.util import FileUtil, LogUtil

from WTFV2.action.training_resource import TrainingResource


class TrainingResourceTest:

    logger = LogUtil.get_logger('training_resource_test')

    def __init__(self):
        self.tr = TrainingResource()
        self.path = '..\\data\\wb_case_ui.xlsx'
        self.table = 'woniuboss_test_result'
        self.version = FileUtil.get_version(self.path)


    def test_add_training_resource(self):
        test_info = FileUtil.get_excel('..\\data\\case_data_conf.ini', 'add_resource')
        for info in test_info:
            test_data = info['test_data']
            try:
                actual = self.tr.get_add_resouce_result(test_data)
                CustomAssert.assert_equal(self.version, actual, info, self.table)
            except Exception as e:
                error_msg = traceback.format_exc()
                info['error_msg'] = error_msg
                CustomAssert.assert_error(self.version, self.table, info)



if __name__ == '__main__':
    trt = TrainingResourceTest()
    trt.test_add_training_resource()