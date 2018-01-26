# *-* coding:utf-8 *-*

import datetime
import hashlib
import random
import requests
import string

from common.utils import epoch

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

class WeixinXml(object):
    def __init__(self, x):
        if type(x) is str or type(x) is unicode:
            self._root = ET.fromstring(x)
        else:
            self._root = ET.parse(x)

    def get(self, name):
        try:
            return self._root.find(name).text
        except:
            return None

def dict_to_xml(data, tag='xml'):
    elem = Element(tag)
    for key, val in data.items():
        child = Element(key)
        child.text = str(val).encode("utf-8")
        elem.append(child)
    return elem

class MinaPayment(object):
    def __init__(self, appid, app_secret, mch_id, api_secret):
        '''
        appid: wxd4eae843e18ff7da
        app_secret: 510861ca183551e3a7fcbdc87573c00f
        mch_id: 1495032292
        api_key: aWNhdGUgQXV0aG9yXR5Q0wwYDVQQDEwR
        '''
        self.appid = appid
        self.app_secret = app_secret
        self.mch_id = mch_id
        self.api_secret = api_secret

    def get_nonce_str(self, length=32):
        return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(length)])

    def get_param_str(self, data):
        slist = sorted(data)
        param_list = map(lambda k: "{0}={1}".format(k, str(data[k]).encode("utf-8")), slist)
        param_str = "&".join(param_list)
        return param_str

    def get_sign(self, data):
        __param_str = self.get_param_str(data)
        __param_str = '{0}&key={1}'.format(__param_str, self.api_secret)
        __param_str = hashlib.md5(__param_str).hexdigest()
        ret = __param_str.upper()
        return ret

    def get_prepay_id(self, out_trade_no, total_fee, body, openid, notify_url):
        '''
        获取微信支付的prepay_id
        '''
        data = {
            "appid": self.appid,
            "mch_id": self.mch_id, # 商户号
            "body": body, # 商品描述
            "nonce_str": self.get_nonce_str(), # 随机数
            "notify_url": notify_url,
            "out_trade_no": out_trade_no, # 商户订单号
            "trade_type": "JSAPI", # 交易类型
            "total_fee": total_fee, # 订单总金额, 分为单位
            "spbill_create_ip": "127.0.0.1",
            "openid": openid
        }
        data["sign"] = self.get_sign(data) # 签名
        data_xml = dict_to_xml(data)
        payload = tostring(data_xml)

        headers = {
            "Content-Type": 'application/xml'
        }

        ret = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=payload, headers=headers)
        xml_res = WeixinXml(ret.text)

        return_code = xml_res.get('return_code')
        if return_code is not None and return_code.lower() == 'success':
            prepay_id = xml_res.get('prepay_id')
            return prepay_id
        return None

    def get_js_api_parameter(self, prepay_id):
        data = {
            "appId": self.appid,
            "timeStamp": epoch(datetime.datetime.now()),
            "nonceStr": self.get_nonce_str(),
            "package": "prepay_id={0}".format(prepay_id),
            "signType": "MD5",
        }
        sign = self.get_sign(data)
        data['paySign'] = sign

        return data
