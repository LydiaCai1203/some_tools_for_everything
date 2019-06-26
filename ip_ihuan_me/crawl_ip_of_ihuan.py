"""
一点无关的注释：
1. python -m model_name 以调用模块的方式执行脚本文件，__name__就等于模块名
这样似乎就可以解决相对引用的问题了 celery就可以不用分文件写了
"""
import re
import time
import random

from gevent import monkey; monkey.patch_socket()
import gevent
import requests
from requests.utils import get_encoding_from_headers, get_encodings_from_content
from lxml import etree

from config import PROXY_JOBS
from utils import get_header, get_charset


BASE_URLS = [
        'https://ip.ihuan.me/?page={}'.format(page) for page in [
            'b97827cc', '4ce63706', '5crfe930', 'f3k1d581', 'ce1d45977', 
            '881aaf7b5', 'eas7a436', '981o917f5', '2d28bd81a', 'a42g5985d']]
PUBKEY_URL = 'https://ip.ihuan.me/cdn-cgi/scripts/baidu.challenge.js'
SESSION_URL = 'https://captcha.su.baidu.com/session_cb/'
BASE_CAPTCHA_SRC = 'https://captcha.su.baidu.com/image/'


def get_cookie(base_url, session, headers):
    try:
        resp = session.get(base_url, headers=headers)
    except Exception as e:
        print(e)
        return None
    cookies = session.cookies.get_dict()
    return cookies


def fetch(url):
    headers = get_header()
    session = requests.session()
    
    # ===========
    cookies = get_cookie(url, session, headers)
    try:
        resp = session.get(url, headers=headers, cookies=cookies)
    except Exception as e:
        print(e)
        return None
    cookies = session.cookies.get_dict()
    resp = session.get(PUBKEY_URL, headers=headers, cookies=cookies)
    searchObj = re.search( r'f=".*?";', resp.text, re.M|re.I)
    if not searchObj:
        print("找不到对应的pubkey的值")
        return None
    pubkey = searchObj.group()[3:-2]

    # ============
    cookies = session.cookies.get_dict()
    try:
        resp = session.get(SESSION_URL, headers=headers, cookies=cookies, params={'pub': pubkey})
    except Exception as e:
        print(e)
        return None
    searchObj = re.search( r'sessionstr":".*?"', resp.text, re.M|re.I)
    if not searchObj:
        print("找不到对应的sessionstr的值")
        return None
    sessionstr = searchObj.group()[13:-1]

    # ==============
    cookies = session.cookies.get_dict()
    resp = session.get(BASE_CAPTCHA_SRC, headers=headers, cookies=cookies, params={'pub': pubkey, 'session': sessionstr})
    if not resp.content:
        return None
    img_name = './captcha/' + ''.join(random.sample('1234567890qwertyuiopasdfghjklzxcvbnm', 5)) + '.png'
    with open(img_name, 'wb') as f:
        f.write(resp.content)  
        print(img_name, "图片已经保存成功")


def asynchorous():
    jobs = [gevent.spawn(fetch, BASE_URL) for BASE_URL in BASE_URLS]
    gevent.joinall(jobs, timeout=12)
    values = [job.value for job in jobs]


if __name__ == '__main__':
    asynchorous()
