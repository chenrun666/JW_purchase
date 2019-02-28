"""
获取任务
"""
import json
import time

import requests

from bin.log import logger
from conf.settings import *


def get_task():
    """
    领任务
    :return: 返回任务的json格式
    """
    taskheaders = {'Content-Type': 'application/json'}
    data = {
        "clientType": CLIENTTYPE,
        "machineCode": MACHINECODE
    }
    while True:
        try:
            taskJson = requests.post("http://47.92.119.88:18002/getBookingPayTask",
                                     data=json.dumps(data), headers=taskheaders)
            if taskJson.json()["data"]:
                return taskJson.json()
            else:
                print(taskJson.json(), type(taskJson.json()))
                print("没有任务，休息10秒")
                time.sleep(10)
        except Exception as e:
            logger.error("请求任务接口发生错误，错误提示：" + str(e))


def back_fill(data):
    taskheaders = {'Content-Type': 'application/json'}
    url = 'http://47.92.119.88:18002/bookingPayTaskResult'
    response = requests.post(url, data=json.dumps(data), headers=taskheaders)
    if json.loads(response.text)["status"] == 'Y':
        logger.info('回填任务成功， 回填内容: ' + str(data))
        with open('../logs/success_data.txt', 'a+')as f:
            f.write(json.dumps(data) + '\n')
        return True
    else:
        logger.info(f'回传任务失败,错误信息：{response.text}')
        with open('../logs/error_data.txt', 'a+')as f:
            f.write(json.dumps(data) + '\n')
        return False


if __name__ == '__main__':
    test_back_fill = {'accountPassword': '', 'accountType': '', 'accountUsername': '', 'cardName': 'VCC-VCC',
                      'cardNumber': '5533978673546737', 'checkStatus': True, 'clientType': 'EW_WEB_CLIENT',
                      'createTaskStatus': True,
                      'linkEmail': 'eurowingstsy@163.com', 'linkEmailPassword': 'Ss136313', 'linkPhone': '17710407835',
                      'machineCode': 'EWceshi', 'nameList': ['DAI/RIRONG', 'ZHOU/BINGYI', 'TAO/PING', 'RUAN/MENGQIN'],
                      'payTaskId': 102290, 'pnr': 'D8TCGS', 'price': 399.96, 'baggagePrice': 0, 'sourceCur': 'EUR',
                      'status': 305, 'targetCur': 'EUR'}
    print(test_back_fill)
