"""
target_url = https://www.vanilla-air.com/hk/


https://www.vanilla-air.com/api/booking/track/log.json?__ts=1551233518756&version=1.0

https://www.vanilla-air.com/hk/booking/#/flight-select/?tripType=OW&origin=NRT&destination=HKD&outboundDate=2019-03-22&adults=1&children=0&infants=0&promoCode=&mode=searchResultInter
rev
"""
import time
import datetime

from bin.log import logger
from bin.MyException import StopException
from bin.action import Action
from conf.settings import TEST, BACKFILLINFO


class Buy(Action):
    def __init__(self, task):
        self.fill_back = BACKFILLINFO

        self.origin = task["depAirport"]
        self.destination = task["arrAirport"]
        self.outboundDate = task["depDate"]
        # 初始化成人儿童婴儿个数
        self.adults = 0
        self.children = 0
        self.infants = 0
        self.now_year = int(datetime.datetime.now().year)
        self.passengers = task["passengerVOList"]
        # 根据乘客年龄进行排序
        self.passengers.sort(key=lambda x: int(x["birthday"].split("-")[0]))
        for passenger in self.passengers:
            self.fill_back["nameList"].append(passenger["name"])

            if (self.now_year - int(passenger["birthday"].split("-")[0])) >= 12:
                self.adults += 1
            elif 2 <= (self.now_year - int(passenger["birthday"].split("-")[0])) < 12:
                self.children += 1
            else:
                self.infants += 1

        url = "https://www.vanilla-air.com/hk/booking/#/flight-select/?tripType=OW&origin={}&destination={}&outboundDate={}&adults={}&children={}&infants={}&promoCode=&mode=searchResultInter".format(
            self.origin, self.destination, self.outboundDate, self.adults, self.children, self.infants)

        # 初始化航班信息
        self.flight_num = task["depFlightNumber"]
        # 初始化乘客信息
        self.passengers_info = task["passengerVOList"]
        # 初始化行李信息
        self.luggages_weight = [item["baggageWeight"] for item in self.passengers]
        # 初始化联系人方式
        self.contact = task["contactVO"]
        # 初始化卡信息
        self.payment_card_info = task["payPaymentInfoVo"]["cardVO"]
        # 获取目标价格
        self.target_price = task["targetPrice"]

        # 初始化回填数据

        self.fill_back["cardName"] = task["pnrVO"]["cardName"]
        self.fill_back["cardNumber"] = task["pnrVO"]["cardNumber"]
        self.fill_back["linkEmail"] = task["contactVO"]["linkEmail"]
        self.fill_back["linkEmailPassword"] = task["contactVO"]["linkEmailPassword"]
        self.fill_back["linkPhone"] = task["contactVO"]["linkPhone"]
        self.fill_back["sourceCur"] = task["sourceCurrency"]
        self.fill_back["targetCur"] = task["targetCurrency"]

        Action.__init__(self, url)

    def select_flight(self, flight_num):
        """
        选择对应的航班号
        :param flight_num:
        :return:
        """
        try:
            flight_info_xpath = '/html/body/div[1]/div[2]/div/div/div[1]/div/div[1]/div[3]/div[2]/div/div[4]/div/div[2]/dl'
            dl_list = self.get_ele_list(flight_info_xpath)

            # 匹配航班号
            for index, item in enumerate(dl_list):
                # 获取页面的航班号
                if index == 0:
                    continue
                page_flight_num_xpath = './dt/span[2]'
                page_flight_num, page_flight_date = self.get_text(page_flight_num_xpath, item).split()
                if page_flight_num == flight_num:
                    # 点击选中航班
                    # 点击原味香草simple
                    simple_xpath = './dd[2]'
                    self.click_btn(simple_xpath, item)
                    time.sleep(2)
                    # 关闭提示框
                    tip_xpath = './dd[2]/div/span/span[2]/div/div/div[1]/a'
                    self.click_btn(tip_xpath, item)
                    time.sleep(1)
                    # 获取价格校验航班价格
                    page_flight_price_xpath = './dd[2]/div/span/span[2]'
                    currency, page_flight_price = self.get_text(page_flight_price_xpath, item).split()
                    if float(page_flight_price) > self.target_price:  # 页面价格大于目标价格，中断程序
                        logger.info(f"目标价格小于页面价格, 页面价格为：{page_flight_price}, 任务目标价格为：{self.target_price}")
                        self.fill_back["status"] = 403
                        raise StopException("目标价格小于页面价格")

                    # 回填数据
                    # 。。。。。。

                    # 点击下一步
                    next_step_xpath = '/html/body/div[1]/div[2]/div/div/div[1]/div/div[1]/div[4]/div[3]/div[2]/a'
                    self.click_btn(next_step_xpath)
                    time.sleep(2)

                    # 记录日志
                    logger.debug(f"选择航班结束， 航班号为{page_flight_num}")
                    break
            else:
                self.fill_back["status"] = 402
                logger.debug("没有找到航班")
                raise StopException("没有查询到航班")

        except StopException as e:
            logger.error(f"{e}导致程序中断")
            raise StopException(e)
        except Exception as e:
            logger.error(f"选择航班发生错误，错误提示：{e}")
            raise StopException(e)

    def fill_passenger_info(self):
        """
        填写乘客信息
        :return:
        """
        # 关闭登陆提示框
        close_btn_xpath = '//*[@id="loginform-modal"]/div/div/div[1]/a'
        self.click_btn(close_btn_xpath)
        # 获取所有的乘客输入div标签
        form_passenger_xpath = '//ng-form[@name="passengersCtl.paxInfo"]/div[1]/div'
        form_passengers_obj = self.get_ele_list(form_passenger_xpath)

        for index, passenger in enumerate(self.passengers_info):
            # index : 乘客对应的form输入框
            # 名字
            firstname_xpath = './form//ul/li[1]/input'
            lastname_xpath = './form//ul/li[2]/input'
            self.fill_input(content=passenger["name"].split("/")[1], xpath=firstname_xpath,
                            el=form_passengers_obj[index])
            self.fill_input(content=passenger["name"].split("/")[0], xpath=lastname_xpath,
                            el=form_passengers_obj[index])

            man_xpath = './form/div[1]/div[4]/div[2]/div/div[2]/ul/li[3]/span[1]'
            female_xpath = './form/div[1]/div[4]/div[2]/div/div[2]/ul/li[3]/span[2]'
            if passenger["sex"] == "F":  # 女生
                self.click_btn(el=form_passengers_obj[index], xpath=female_xpath)
            else:
                self.click_btn(el=form_passengers_obj[index], xpath=man_xpath)

            # 输入出生日期
            # 在输入日期之前先点击输入框
            birthday_xpath = './form//ul/li[4]/input'
            self.click_btn(xpath=birthday_xpath, el=form_passengers_obj[index])
            birthday = "".join(passenger["birthday"].split("-"))
            self.fill_input(xpath=birthday_xpath, content=birthday,
                            el=form_passengers_obj[index], single_input=False)

            # 选择国家
            if index == 0:
                country_xpath = './form/div[2]/ul/li[1]/dl/dd/div[1]/label/input'
                self.fill_input(content="日本", xpath=country_xpath, el=form_passengers_obj[index])

        # 填写完毕，点击下一步
        next_xpath = '//dd[@class="usr-action-box--jp-b next"]/button'
        self.click_btn(xpath=next_xpath)

        logger.debug("乘客信息填写完毕")
        time.sleep(3)

    def select_luggages(self):
        if sum(self.luggages_weight) > 0:
            # 有乘客携带行李，选择行李
            add_luggage_xpath = '//div[@class="vnl-service-options-box vnl-service-options-box--jp-b baggage"]'
            self.click_btn(add_luggage_xpath)
            passenger_luggage_list_xpath = '//div[@class="vnl-seat-select-box"]/div/div[2]/div/div[2]/div'
            passenger_luggage_list = self.get_ele_list(passenger_luggage_list_xpath)

            # 对每个乘客进行行李的点击
            for index, passenger in enumerate(self.passengers):
                # 滑动到可见元素
                self.scroll_screen(passenger_luggage_list[index])
                time.sleep(2)

                if passenger["baggageWeight"] == 0:
                    continue
                # 计算获取对应的重量
                quotient, residue = divmod(passenger["baggageWeight"], 5)
                if residue > 0:
                    quotient += 1
                # 行李重量li标签的索引
                if quotient < 4:
                    select_weight_index = 2
                else:
                    select_weight_index = quotient - 2
                # 51KG一下的
                # 点击选择行李重量
                if select_weight_index < 10:
                    weight_xpath = './div[@class="vnl-baggage-select-box--flight_baggage-one-person"]/div[2]/ol/li[{}]'
                    self.click_btn(xpath=weight_xpath.format(select_weight_index), el=passenger_luggage_list[index])
                else:
                    # 501KG以上的行李选择
                    # 先点击更多
                    more_xpath = './div[@class="vnl-baggage-select-box--flight_baggage-one-person"]/div[2]/ol/li[@class="more"]'
                    # 滑动屏幕
                    # self.scroll_screen()
                    self.click_btn(more_xpath, el=passenger_luggage_list[index])
                    time.sleep(1)
                    select_weight_index -= 8
                    weight_xpath = './div[@class="vnl-baggage-select-box--flight_baggage-one-person"]/div[2]/ol/li[@class="more"]/div/ul/li[{}]'
                    self.click_btn(xpath=weight_xpath.format(select_weight_index), el=passenger_luggage_list[index])
                pass

            else:
                # 点击完成
                over_xpath = '//a[@ng-click="selectBaggageCtl.close()"]'
                self.click_btn(over_xpath)
                time.sleep(2)

        # 无行李，选择空过
        # 点击下一步
        next_xpath = '//a[@data-id="act-next"]'
        self.click_btn(next_xpath)

        logger.debug("选择行李完毕")
        time.sleep(2)
        # 选择不用了，谢谢
        no_thanks_js = "document.querySelector('body > div.vnl-modal-popup.vnl-modal-popup_wrap > div > div > div > div.vnl-popup_btn > a.no.action_close').click()"
        self.driver.execute_script(no_thanks_js)

    def fill_contact_info(self):
        """
        填写联系人信息
        :return:
        """
        # 填写邮箱
        email_xpath = '//div[@class="vnl-payment-contact-information"]//div[@class="right"]/dl[1]/dd//input'
        self.fill_input(xpath=email_xpath, content=self.contact["linkEmail"])
        email_sure_xpath = '//div[@class="vnl-payment-contact-information"]//div[@class="right"]/dl[2]/dd//input'
        self.fill_input(xpath=email_sure_xpath, content=self.contact["linkEmail"])

        # 联系人区号
        area_code_xpath = '//div[@class="vnl-payment-contact-information"]//div[@class="left"]/dl[4]/dd//input'
        self.fill_input(xpath=area_code_xpath, content=100000)
        # 联系人电话
        phone_num_xpath = '//div[@class="vnl-payment-contact-information"]//div[@class="left"]/dl[5]/dd//input'
        self.fill_input(xpath=phone_num_xpath, content=self.contact["linkPhone"])

        logger.debug("联系人信息填写完毕")

    def select_payment_method(self):
        """
        选择支付方式
        :return:
        """
        # 选用VCC visa
        vcc_xpath = '//div[@class="cardtype ng-scope"]/label[2]/span'
        self.click_btn(vcc_xpath)
        time.sleep(5)

        logger.debug("支付方式选择完毕")
        # 点击下一步
        next_xpath = '//div[@class="vnl-payment-action"]/a[@data-id="act-next"]'
        self.click_btn(next_xpath)
        time.sleep(5)

    def sure_info(self):
        """
        确认所选信息, 校对选择的行李是否正确，获取行李的总价格回填行李价格和其他费用
        :return:
        """
        if sum(self.luggages_weight) > 0:
            # 有行李
            # 获取行李价格
            detail_info_list_xpath = '//div[@data-id="flight_1"]//div[@class="vnl-fare-detail-summary-detail-box vnl-fare-detail-summary-detail__blk"][2]/div'
            detail_info_list = self.get_ele_list(detail_info_list_xpath)
            for item in detail_info_list:
                if "託運行李" in self.get_text(xpath='./p', el=item):
                    luggage_price_xpath = './/dd[@class="price ng-binding"]'
                    luggage_price = self.get_text(xpath=luggage_price_xpath, el=item).split()[1].replace(",",
                                                                                                         "")  # 'HKD 1,976'
                    self.fill_back["baggagePrice"] = float(luggage_price)

                    break

        else:
            # 回填行李重量和价格
            self.fill_back["baggagePrice"] = 0.0

        # 获取价格，去掉行李的价格
        total_price_xpath = '//div[@class="vnl_itinerary_price-total_price"]/span/span'
        total_price = self.get_text(xpath=total_price_xpath).split()[1].replace(",", "")

        self.fill_back["price"] = float(total_price) - self.fill_back["baggagePrice"]

        # 同意协议
        sure_xpath = '//div[@class="reconfirm_agreement_check"]/p//span[1]'
        self.click_btn(sure_xpath)
        # 点击下一步
        pay_btn_xpath = '//a[@data-id="act-purchase"]'
        self.click_btn(pay_btn_xpath)

        logger.debug("同意协议点击无误")
        time.sleep(10)

    def fill_card_info(self):
        """
        输入卡号信息
        :return:
        """
        card_num_xpath = '//*[@id="cardNumber"]'
        card_name_xpath = '//*[@id="cardholderName"]'
        month_xpath = '//*[@id="expiryMonth"]'
        year_xpath = '//*[@id="expiryYear"]'
        cvv_code_xpath = '//*[@id="securityCode"]'

        card_info_dict = {
            card_num_xpath: self.payment_card_info["cardNumber"],
            card_name_xpath: self.payment_card_info["lastName"] + "/" + self.payment_card_info["firstName"],
            month_xpath: self.payment_card_info["cardExpired"].split("-")[1],
            year_xpath: self.payment_card_info["cardExpired"].split("-")[0],
            cvv_code_xpath: self.payment_card_info["cvv"],
        }

        for k, v in card_info_dict.items():
            self.fill_input(content=v, xpath=k)

        logger.debug("填写卡号信息完成")

    def pay(self):
        """
        点击进行支付
        :return:
        """
        logger.debug("开始支付")
        pay_btn_xpath = '//*[@id="submitButton"]'
        self.click_btn(pay_btn_xpath)

        # 获取票号

    def __call__(self, *args, **kwargs):
        try:
            # 选择乘客
            self.select_flight(self.flight_num)
            # 填写乘客信息
            self.fill_passenger_info()
            # 选择行李
            self.select_luggages()
            # 填写联络信息
            self.fill_contact_info()
            # 选择支付方式
            self.select_payment_method()
            # 确认行李
            self.sure_info()
            # 输入支付卡信息
            self.fill_card_info()
            # 点击支付，获取pnr
            self.pay()

        except StopException as e:
            if not self.fill_back["status"]:
                self.fill_back["status"] = 401
            logger.error(f"程序中断：错误提示 -》{e}")
            return

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    if TEST:
        import json

        with open("../files/fake_task.json", "r", encoding="utf-8") as f:
            task = f.read()
        task = json.loads(task)["data"]
    else:
        task = {}
    buy = Buy(task)
    buy()
