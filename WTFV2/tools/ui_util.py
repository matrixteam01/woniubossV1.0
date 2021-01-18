
import os
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from WTFV2.tools.util import LogUtil


class UIUtil:

    logger = LogUtil.get_logger( 'ui_util')
    driver = None
    mouse = PyMouse()
    keyboard = PyKeyboard()


    @classmethod
    def get_driver(cls):
        """
        单例模式，通过反射机制获取webdriver对象并返回
        :return:webdriver单例对象
        """
        from selenium import webdriver
        from WTFV1.tools.util import FileUtil
        browser = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui_info', 'browser')
        login_page = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui_info', 'login_page')
        if cls.driver is None:
            try:
                cls.driver = getattr(webdriver, browser)(service_log_path="D:/workspace/geckodriver_log/geckodriver.log")
            except Exception as e:
                cls.logger.error('浏览器名称不正确，已使用默认浏览器')
                cls.driver = webdriver.Firefox(service_log_path="D:/workspace/geckodriver_log/geckodriver.log")
            cls.driver.implicitly_wait(5)
            cls.driver.maximize_window()
            cls.driver.get(login_page)
        return cls.driver

    @classmethod
    def find_element_by_attr(cls, driver, element_attr):
        """
        找到元素对象并返回
        :param driver: 浏览器驱动对象
        :param element_attr: 元素属性
        :return: 元素对象
        """

        return driver.find_element(getattr(By, element_attr[0]), element_attr[1])

    @classmethod
    def is_elment_present(cls, driver, element_attr):
        """
        判断某个元素是否存在
        :param driver: 浏览器驱动对象
        :param element_attr: 元素的属性的元组形式
        :return: 是否存在的标识
        """
        try:
            driver.find_element(getattr(By, element_attr[0]), element_attr[1])
            return True
        except Exception as e:
            return False

    @classmethod
    def input(cls, element, value):
        '''

        :param element: 页面上的输入框元素
        :param value: 给输入框输入的值
        :return: None
        '''

        element.click()
        element.clear()
        element.send_keys(value)

    @classmethod
    def input_textarea(cls, element, value):
        """
        向文本域输入内容
        :param element: 文本域元素
        :param value: 要输入的值
        :return: None
        """
        element.click()
        element.send_keys(value)

    @classmethod
    def click(cls, element):
        """

        :param element: 要单击的元素
        :return: 无
        """
        element.click()

    @classmethod
    def select_random(cls, element):
        """
        随机选择下拉框中的某一项
        :param element: 下拉框对象
        :return:None
        """
        import random
        select_obj = Select(element)
        option_count = len(select_obj.options)
        select_obj.select_by_index(random.randint(0, option_count))

    @classmethod
    def select_by_txt(cls, element, text):
        """
        通过指定文本选择option
        :param element: 下拉框对象
        :param text: 可见的文本
        :return: None
        """
        select_obj = Select(element)
        select_obj.select_by_visible_text(text)

    @classmethod
    def get_element_text(cls, element):
        """
        获取元素的文本值
        :param element: 某个元素
        :return: 元素的文本值
        """
        return element.text

    @classmethod
    def match_image(cls, target):
        """

        :param target: 模板图片的名称
        :return:大图匹配的十字中心点坐标
        """
        image_path = "..\\image"
        screen_path = os.path.join(image_path,'screen.png')
        # 对大图进行截图，并保存在指定路径
        from PIL import ImageGrab
        ImageGrab.grab().save(screen_path)

        import cv2
        # 读取大图
        screen = cv2.imread(screen_path)
        # 读取小图
        template = cv2.imread(os.path.join(image_path, target))

        # 调用匹配算法
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

        min, max , min_loc, max_loc = cv2.minMaxLoc(result)

        # 计算矩形十字中心点的坐标
        x = max_loc[0] + int(template.shape[1] / 2)
        y = max_loc[1] + int(template.shape[0] / 2)
        return x, y


    # 单击图片元素
    @classmethod
    def click_image(cls, target):
        """
        单击图片
        :param target: 图片名称
        :return:None
        """
        x, y = cls.match_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'没有找到{target}图片')
            return
        cls.mouse.click(x, y)

    # 双击图片元素
    @classmethod
    def double_click_image(cls, target):
        """
        双击图片
        :param target: 图片名称
        :return: None
        """
        x, y = cls.match_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'没有找到{target}图片')
            return
        cls.mouse.click(x, y, n=2)

    # 向一个文本框图片输入
    @classmethod
    def input_image(cls, target, value):
        """
        向输入框文本图片输入内容
        :param target: 图片名称
        :param value:输入的值
        :return:None
        """
        x, y = cls.match_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'没有找到{target}图片')
            return
        cls.keyboard.type_string(value)

    @classmethod
    def select_image(cls, target, count):
        """
        按次数选择下拉框的option
        :param target: 图片名称
        :param count: 向下的次数
        :return: None
        """
        # 点击下拉图片
        cls.click_image(target)
        for i in range(count) :
            # 按count次向下的箭头
            cls.keyboard.press_key(cls.keyboard.down_key)
        # 回车
        cls.keyboard.press_key(cls.keyboard.enter_key)


if __name__ == '__main__':
    pass
    # print(UIUtil.image_match('demo02.png'))
