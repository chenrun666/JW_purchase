"""


"""
import requests


def get_flight():
    target_url = "https://www.vanilla-air.com/hk/booking/#/flight-select/?tripType=OW&origin=NRT&destination=CTS&outboundDate=2019-03-31&adults=1&children=0&infants=0&promoCode=&mode=searchResultInter"

    response = requests.get(target_url)

    print(response.text)


def get_traceID():
    url = "https://www.vanilla-air.com/api/booking/track/log.json?__ts=1551242320737&version=1.0"

    data = {
        "fromState": "^",
        "toState": "/flight-select/?tripType&origin&destination&outboundDate&returnDate&adults&children&infants&promoCode&mode&targetMonth&returnTargetMonth&2origin&2destination&3origin&3destination&4origin&4destination",
        "paymentMethod": "",
        "condition": {
            "adultCount": 1,
            "childCount": 0,
            "infantCount": 0,
            "couponCode": "",
            "currency": "",
            "tripType": ""
        },
        "flights": [

        ],
        "passengers": [

        ],
        "contact": {
            "name": "",
            "country": "",
            "zipCode": "",
            "phoneNumber": "",
            "email": "",
            "mailMagFlg": False,
            "preferredLanguage": "",
            "givenName": "",
            "surName": "",
            "password": "",
            "chkbxRegistMember": "",
            "dateOfBirth": "",
            "namePrefix": "",
            "prefecture": ""
        },
        "mode": {
            "pointCalculate": False,
            "priceOnly": False
        },
        "payment": {
            "paymentType": ""
        },
        "flightSummary": [

        ]
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Referer": "https://www.vanilla-air.com/hk/booking/",
        "__locale": "hk",
        "Accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "channel": "pc"
    }
    response = requests.post(url, data=data, headers=headers)

    print(response)


if __name__ == '__main__':
    # get_flight()
    get_traceID()
