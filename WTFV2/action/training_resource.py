from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from WTFV2.action.setup import Setup
from WTFV2.tools.ui_util import UIUtil
from WTFV2.tools.util import FileUtil
import time

class TrainingResource:

    path = '..\\conf\\element_attr.ini'
    section = 'training_resource'

    def __init__(self):
        self.driver = UIUtil.get_driver()
        Setup.admin_login(self.driver)
        time.sleep(2)
        Setup.decrypt(self.driver)
        Setup.click_resouce_manager_link(self.driver)
        training_resource_link = Setup.get_page_element(self.driver, 'main_page', 'training_resource_link')
        UIUtil.click(training_resource_link)

    def click_add_resource_button(self):
        """
        点击添加资源按钮
        :return: None
        """
        add_resource_button = Setup.get_page_element(self.driver, self.section, 'add_resource_button')
        UIUtil.click(add_resource_button)

    def input_phone(self, value):

        phone = Setup.get_page_element(self.driver, self.section, 'phone')
        UIUtil.input(phone, value)

    def input_name(self, value):

        name = Setup.get_page_element(self.driver, self.section, 'name')
        UIUtil.input(name, value)

    def select_last_status(self, value):

        last_status = Setup.get_page_element(self.driver, self.section, 'last_status')
        UIUtil.select_by_txt(last_status, value)

    def click_save_resource_button(self):

        save_resource_button = Setup.get_page_element(self.driver, self.section, 'save_resource_button')
        UIUtil.click(save_resource_button)

    def select_resouce(self, value):

        cus_source = Setup.get_page_element(self.driver, self.section, 'cus_source')
        UIUtil.select_by_txt(cus_source, value)

    def click_track_button(self):

        track_button = Setup.get_page_element(self.driver, self.section, 'track_button')
        UIUtil.click(track_button)

    def click_track_resouce_link(self):

        track_resource_link = Setup.get_page_element(self.driver, self.section, 'track_resource_link')
        UIUtil.click(track_resource_link)

    def input_track_content(self, value):

        remark_link = Setup.get_page_element(self.driver, self.section, 'remark')
        UIUtil.input_textarea(remark_link, value)

    def select_new_status(self, value):

        new_status = Setup.get_page_element(self.driver, self.section, 'newStatus')
        UIUtil.select_by_txt(new_status, value)

    def click_save_track_button(self):

        save_track_button = Setup.get_page_element(self.driver, self.section, 'save_track_button')
        UIUtil.click(save_track_button)

    def do_add_resouce(self, resouce_data):
        self.click_add_resource_button()
        time.sleep(2)
        self.input_phone(resouce_data['cus.tel'])
        self.input_name(resouce_data['cus.name'])
        self.select_last_status(resouce_data['cus.last_status'])
        self.select_resouce(resouce_data['cus.source'])
        time.sleep(2)
        self.click_save_resource_button()

    def get_add_resouce_result(self, resouce_data):
        self.do_add_resouce(resouce_data)
        time.sleep(2)
        add_resouce_success_button_attr = FileUtil.get_ini_value(self.path, self.section, 'add_resouce_success_button')
        if UIUtil.is_elment_present(self.driver, add_resouce_success_button_attr):
            add_resouce_msg = Setup.get_page_element(self.driver, self.section, 'add_resouce_msg')
            content = UIUtil.get_element_text(add_resouce_msg)
            if '新增成功' in content:
                actual = '添加资源成功'
            else:
                actual = '添加资源重复'
            add_resouce_msg_button = Setup.get_page_element(self.driver, self.section, 'add_resouce_msg_button')
            UIUtil.click(add_resouce_msg_button)
        else:
            actual = '添加资源失败'
        self.driver.refresh()

        return actual

    def do_track_resouce(self, track_resouce_data):
        self.click_track_button()
        self.click_track_resouce_link()
        self.input_track_content(track_resouce_data['track_content'])
        self.select_new_status(track_resouce_data['status'])
        self.click_save_track_button()



if __name__ == '__main__':

    tr = TrainingResource()
    # tr.do_track_resouce({'track_content':'第一次打电话','status':'新认领'})
    # tr.do_add_resouce({'cus.tel':'15112121312','cus.name':'小明','cus.last_status':'新入库','cus.source':'自然流量'})
    result = tr.get_add_resouce_result({'cus.tel':'15892161832','cus.name':'小明','cus.last_status':'新入库','cus.source':'自然流量'})
    print(result)