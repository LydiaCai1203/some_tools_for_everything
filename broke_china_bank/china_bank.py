import re
import time
import json

import js2py
import execjs
import requests
import jsbeautifier
from lxml import etree



HEADERS = {
    'User-Agent': '[{"key":"User-Agent","value":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36","description":"","type":"text","enabled":true}]',
    'Referer': 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html',
    'Host': 'www.pbc.gov.cn',
}

URL = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html'

def start_requests():
    session = requests.session()
    resp = session.get(URL, headers=HEADERS)
    cookies = session.cookies.get_dict()

    html_521 = resp.text
    html_521=''.join(re.findall('<script(.*?)</script>', html_521))
    print(html_521)
    html_521 = html_521.replace('eval', 'return')
    obj_521 = execjs.compile(html_521)
    decoded_js = obj_521.call('r')    # p,a,c,k,e,r
    print(decoded_js)

start_requests()
