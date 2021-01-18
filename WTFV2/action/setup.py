from WTFV2.tools.ui_util import UIUtil
from WTFV2.tools.util import FileUtil


class Setup:

    path = '..\\conf\\element_attr.ini'
    section = 'main_page'

    @classmethod
    def admin_login(cls, driver):
        """
        使用固定的账号直接登录
        :param driver: 浏览器驱动对象
        :return: None
        """
        driver.find_element_by_name('userName').send_keys('WNCD000')
        driver.find_element_by_name('userPass').send_keys('woniu123')
        checkcode = driver.find_element_by_name('checkcode')
        checkcode.click()
        checkcode.clear()
        checkcode.send_keys('0000')
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/button').click()

    @classmethod
    def decrypt(cls, driver):
        """
        进行账号的二次解密
        :param driver: 浏览器驱动对象
        :return: None
        """
        driver.find_element_by_id('btn-decrypt').click()
        driver.find_element_by_name('secondPass').send_keys('woniu123')
        driver.find_element_by_xpath('/html/body/div[12]/div/div/div[3]/button').click()

    @classmethod
    def get_page_element(cls, driver, section, option):
        main_page_element_attr = FileUtil.get_ini_value(cls.path, section, option)
        return UIUtil.find_element_by_attr(driver, main_page_element_attr)


    @classmethod
    def click_resouce_manager_link(cls, driver):
        """
        点击主页上的资源管理链接
        :param driver: 浏览器驱动对象
        :return: None
        """
        resource_manager_link = cls.get_page_element(driver, cls.section, 'resource_manager_link')
        resource_manager_link.click()

    @classmethod
    def click_personnel_manager_link(cls, driver):
        """
        点击主页上的人事管理链接
        :param driver: 浏览器驱动对象
        :return: None
        """
        personnel_manager_link = cls.get_page_element(driver, cls.section, 'personnel_manager_link')
        personnel_manager_link.click()


if __name__ == '__main__':
    Setup.admin_login()