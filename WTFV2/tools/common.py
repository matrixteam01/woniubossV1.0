from WTFV2.tools.ui_util import UIUtil


class Common:

    @classmethod
    def get_screenshot(cls, version):
        """
        截取当前屏幕并返回截图路径
        :param version: 版本
        :return: 截图路径
        """
        import os
        from WTFV2.tools.util import TimeUtil

        screenshot_path = f'../report/{version}/screenshot/'
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        driver = UIUtil.get_driver()
        image_name = screenshot_path + str(TimeUtil.get_file_time()) + '.png'
        driver.get_screenshot_as_file(image_name)
        return image_name
