TEST = True
# TEST = False


CLIENTTYPE = "JW_WEB_CLIENT"
MACHINECODE = "JWceshi"

# 回填数据格式
BACKFILLINFO = {
    "accountPassword": "",
    "accountType": "",
    "accountUsername": "",
    "cardName": "",  # VCC-VCC
    "cardNumber": "",  # 5533970000008000
    "checkStatus": True,
    "clientType": "JW_WEB_CLIENT",
    "createTaskStatus": True,

    "linkEmail": "",
    "linkEmailPassword": "",
    "linkPhone": "",

    "machineCode": "JWceshi",
    "nameList": [],
    "payTaskId": None,  # 34212
    "pnr": "",
    "price": None,  # 支付的机票含税总价（不包含行李价格）
    "baggagePrice": None,
    "sourceCur": "EUR",
    "status": None,
    "targetCur": "EUR"
}

# BookingFail(301,"保留失败"),
# PriceVerifyFail(340, "失败,执行下一条规则"),// 某些客户端特有
# BookingSuccess(350,"保留成功"),
# PayFail(401,"支付失败"),// 普通失败，如登录失败，某些页面刷新错误
# PayFailForNoFlight(402,"无航班,支付失败"),// 无航班特有状态
# PayFailForHighPrice(403,"高价,支付失败"),// 支付价高于目标价
# PayFailForErrorAccount(404,"登录账号有误,支付失败"),// 需注意，明确登录账号或者密码有误回此状态
# PayFailAfterSubmitCard(440,"提交支付后,获取票号失败"),// 提交最后一步时，页面刷新错误
# PaySuccess(450,"支付成功"),
#
# // 下面为客户端返回440之后适配的流程状态
# SearchPNRException(441, "查询票号状态异常"),// 此状态会自动重发查询票号任务
# SearchPNRFail(442, "查询票号状态,确认失败"),
# SearchPNRToPerson(444, "票号状态需人工确认"),// 查询之后客户端也确定不了票号的状态
