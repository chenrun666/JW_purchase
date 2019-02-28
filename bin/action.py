import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select

from conf.settings import *
from bin.log import logger
from bin.MyException import *


class Action(object):

    def __init__(self, url):
        """
        初始化浏览器
        """
        # 当前运行状态，如果页面动作出现错误之后将终止运行
        self.run_status = True
        self.index_url = url
        try:
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome()
            # self.driver = webdriver.Firefox()
            # self.driver = webdriver.PhantomJS()
            self.wait = WebDriverWait(self.driver, 20, 0.5)
            self.driver.get(self.index_url)

            time.sleep(3)
            # self.driver.set_window_size(500, 700)
            logger.info("初始化webdriver对象")
        except TimeoutException:
            logger.error("初始化超时")
            self.run_status = False
            raise StopException("初始化浏览器超时")
        except Exception as e:
            logger.error("初始化webdriver对象失败" + str(e))
            self.run_status = False

    # 对input框输入内容
    def fill_input(self, content, xpath, single_input=False, el=None):
        """
        获取到xpath表达式，定位元素，输入内容
        :param args:
        :param kwargs:
        :return:
        """
        try:
            if not el:
                input_content = self.wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        xpath
                    ))
                )
                if input_content.is_enabled():
                    # 一个一个字母输入
                    input_content.clear()
                    if single_input:
                        for item in content:
                            input_content.send_keys(item)
                            time.sleep(0.7)
                    else:
                        input_content.send_keys(content)
                else:
                    logger.debug(f"fill_input:{xpath}该元素不可操作")
                    self.run_status = False
            else:
                if not single_input:
                    el.find_element_by_xpath(xpath).send_keys(content)
                else:
                    for item in content:
                        el.find_element_by_xpath(xpath).send_keys(item)
                        time.sleep(0.3)
        except TimeoutException:
            logger.error("填写信息超时")
            self.run_status = False
            raise StopException("填写信息超时")
        except Exception as e:
            logger.error(f"定位{xpath}时，填写{content}时出错，错误信息：{str(e)}")
            self.run_status = False

    def click_btn(self, xpath, el=None):
        try:
            if not el:
                btn = self.wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        xpath
                    ))
                )
                if btn.is_enabled():
                    btn.click()
                    time.sleep(1)
                else:
                    logger.debug(f"click_btn:{xpath}该元素不可操作")
                    self.run_status = False
            else:
                el.find_element_by_xpath(xpath).click()
        except TimeoutException:
            logger.error(f"点击{xpath}超时")
            self.run_status = False
            raise StopException("点击超时")
        except Exception as e:
            logger.error(f"定位{xpath}时，点击click时出错，错误信息：{str(e)}")
            self.run_status = False

    def select_date(self, div_num, day):
        """
        选择日期
        :param div_num:
        :param day:
        :return:
        """
        try:
            a = self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f'//*[@id="datepicker"]/div/div[{div_num}]'  # 2 是相对于当前的第几个月
                ))
            )
            # 如果day小于10，就要去掉前面的0
            day = str(int(day))
            a.find_element_by_link_text(f"{day}").click()

            logger.info("选择出发日期")
            time.sleep(1)

        except Exception as e:
            logger.error(f"选择出发日期时发生错误，错误信息：{str(e)}")
            self.run_status = False

    def get_text(self, xpath, el=None):
        try:
            if not el:
                h1 = self.wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        xpath
                    ))
                )
                return h1.text
            else:
                t = el.find_element_by_xpath(xpath)
                return t.text
        except Exception as e:
            logger.error(f"获取页面文本值出错，错误信息为{str(e)}")
            self.run_status = False

    def scroll_screen(self, el=None):
        if not el:
            scroll_screen_js = 'window.scroll(0, document.body.scrollHeight)'
            self.driver.execute_script(scroll_screen_js)
        else:
            if isinstance(el, webdriver.remote.webelement.WebElement):
                self.driver.execute_script("arguments[0].scrollIntoView();", el)
                pass
            else:
                # 拖动至可见元素
                element_obj = self.wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        el
                    ))
                )
                self.driver.execute_script("arguments[0].scrollIntoView();", element_obj)

    def get_ele_list(self, xpath):
        try:
            ele_list = self.wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    xpath
                ))
            )
            return ele_list
        except Exception as e:
            logger.error(f"获取元素列表失败，错误提示：" + str(e))
            self.run_status = False
