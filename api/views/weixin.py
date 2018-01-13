# *-* coding:utf-8 *-*

import hashlib
import random
import requests
import string
import urllib
from urllib import quote
from xml.etree.ElementTree import tostring

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

import datetime
from django.conf import settings

from xml.etree.ElementTree import Element

def epoch(t):
    """Date/Time converted to seconds since epoch"""
    if not hasattr(t, 'tzinfo'):
        return
    return int(time.mktime(_append_tz(t).timetuple()))


def dict_to_xml(data, tag='xml'):
    elem = Element(tag)
    for key, val in data.items():
        child = Element(key)
        child.text = str(val).encode("utf-8")
        elem.append(child)
    return elem


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

# openid: ooE4V0QzwSVR4AekmJI4b8nqLFi0


class WXPayment(object):
    
    def __init__(self, out_trade_no):
        self.__out_trade_no = out_trade_no

    def __get_nonce_str(self, length=32):
        return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(length)])
    
    @staticmethod
    def generate_test_out_trade_no():
        test_out_trade_no = hashlib.md5(str(datetime.datetime.now()) + 'test_order').hexdigest()
        return test_out_trade_no 

    def __generate_sign(self, data):
        slist = sorted(data)
        param_list = map(lambda k: "{0}={1}".format(k, str(data[k]).encode("utf-8")), slist)
        param_str = "&".join(param_list)
        param_str = '{0}&key={1}'.format(param_str, settings.WXPAY_API_KEY)
        param_str = hashlib.md5(param_str).hexdigest()
        ret = param_str.upper()
        return ret

    
    def settlement(self, total_fee, body, openid, notify_url):
        prepay_id = self.__get_prepay_id(total_fee, body, openid, notify_url)
        ret = {
            'timestamp': '',
            'nonce_str': self.__get_nonce_str(),
            'package': 'prepay_id=%s'%prepay_id,
            'sign_type': 'MD5',
        }


    def __get_prepay_id(self, total_fee, body, openid, notify_url):
        data = {
            "appid": settings.WECHAT_APP_ID,
            "mch_id": settings.WXPAY_MCH_ID, 
            "body": body,                           
            "nonce_str": self.__get_nonce_str(), 
            "out_trade_no": self.__out_trade_no,
            "total_fee": total_fee, 
            "spbill_create_ip": "127.0.0.1",
            "notify_url": notify_url,
            "trade_type": "JSAPI", 
            "openid": openid
        }
        data["sign"] = self.__generate_sign(data) # 签名
        data_xml = dict_to_xml(data)
        payload = tostring(data_xml)
        
        ret = requests.post(
            'https://api.mch.weixin.qq.com/pay/unifiedorder', 
            data=payload, 
            headers={
                "Content-Type": 'application/xml'
            }
        )
        xml_res = WeixinXml(ret.text)
        return_code = xml_res.get('return_code')
        
        if return_code is not None and return_code.lower() == 'success':
            prepay_id = xml_res.get('prepay_id')
            return prepay_id
        return None

#class JSAPIPayment(WeixinPayment):
#    def __init__(self):
#        super(JSAPIPayment, self).__init__()
#        self.__code = None
#        self.__openid = None
#        self.__paramters = None
#        self.__prepay_id = None
#
#    """
#    生成请求code的url
#    """
#    def get_oauth_code_url(self, redirect_url, state):
#        data = {
#            "appid": self.appid,
#            "redirect_uri": redirect_url,
#            "response_type": "code",
#            "scope": "snsapi_base",
#            "state": "{0}{1}".format(state, "#wechat_redirect")
#        }
#        query_param = self.get_param_str(data)
#
#        return "https://open.weixin.qq.com/connect/oauth2/authorize?" + query_param
#
#    """
#    生成请求openid的url
#    """
#    def get_oauth_openid_url(self):
#        data = {
#            "appid":self.appid,
#            "secret":self.appsecret,
#            "code":self.__code,
#            "grant_type":"authorization_code",
#        }
#        query_param = self.get_param_str(data)
#        return "https://api.weixin.qq.com/sns/oauth2/access_token?" + query_param
#
#    def get_openid(self):
#        log.info("=========请求openid========")
#        url = self.get_oauth_openid_url()
#        ret = requests.get(url)
#        log.info(ret.json())
#        return ret.json().get('openid')
#
#    def set_code(self, code):
#        self.__code = code
#
#    def set_prepay_id(self, prepay_id):
#        self.__prepay_id = prepay_id
#
#    def get_js_api_parameter(self):
#        data = {
#            "appId": self.appid,
#            "timeStamp": epoch(datetime.datetime.now()),
#            "nonceStr": self.get_nonce_str(),
#            "package": "prepay_id={0}".format(self.__prepay_id),
#            "signType": "MD5",
#        }
#        sign = self.get_sign(data)
#        data['paySign'] = sign
#
#        return data
