"""
__creator__ = 'caiqj'
__date__ = '2019-05-28'
__msg__ = “”“
            1. 每次得到的js动态生成的cookie在redis中保留半小时
            2. 每15s爬一次银保监的所有源
            3. 当redis中的cookie过期以后，每隔两分钟尝试获取一次js动态生成的cookie，直到取到为止
            4. 如果你看到了我写的这个脚本 自己 在装一个redis，或者加上redis_config，连远程的redis
        ”“”
"""
import re
import time
import json

import redis
import execjs
import jsbeautifier
import requests
from lxml import etree
from urllib.parse import urljoin


YINBAOJIAN_COOKIES_KEY = 'yinbaojian_cookies'

URLS = [
    'http://www.cbrc.gov.cn/chinese/zhengcefg.html',
    'http://www.cbrc.gov.cn/chinese/newListDoc/111001/1.html',
    'http://www.cbrc.gov.cn/chinese/newListDoc/111002/1.html',
    'http://www.cbrc.gov.cn/chinese/newListDoc/111003/1.html',
    'http://www.cbrc.gov.cn/chinese/newListDoc/111004/1.html',
    'http://www.cbrc.gov.cn/chinese/newListDoc/111005/1.html',
    'http://www.cbrc.gov.cn/chinese/newListDoc/111006/1.html',
]

# 获取cookie的headers必须与请求页面的headers保持一致，否则会获取不到数据，所以这里写死了
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}


class YinbaojianCookieGeter:
    def __init__(self):
        self.url = 'http://www.cbrc.gov.cn/chinese/zhengcefg.html'
        self.session = requests.session()
        self.rc = redis.Redis(db=6)
        
    def js_decode_first(self):
        try:
            resp = self.session.get(self.url, headers=HEADERS)
        except Exception as e:
            print(e)
        html_521 = resp.text
        html_521=''.join(re.findall('<script>(.*?)</script>', html_521))
        html_521 = html_521.replace('eval', 'return')
        obj_521 = execjs.compile(html_521)
        decoded_js = obj_521.call('f')
        # print(decoded_js)
        return decoded_js
    
    def js_decode_second(self, decoded_js):
        """
        第二次解码主要是为了将一些dom元素删除转换成直接执行的等价的部分。
        """
        decoded_js = decoded_js.replace('document.cookie', 'cookie')
        trash = re.search(r'setTimeout(.*?)[,]1500[)];', decoded_js)
        if trash:
            decoded_js = decoded_js.replace(trash.group(), '')

        trash = re.search(r'document.createElement(.*?)toLowerCase[(][)];', decoded_js)
        if trash:
            decoded_js = decoded_js.replace(trash.group(), "'www.cbrc.gov.cn/'")
        
        trash = re.search(r"return[(]'String.fromCharCode[(]'", decoded_js)
        if trash:
            eval_trash = trash.group().replace('return', 'eval')
            decoded_js = decoded_js.replace(trash.group(), eval_trash)
        
        trash = re.search(r"return[(]'String.fromCharCode[(]'", decoded_js)
        if trash:
            eval_trash = trash.group().replace('return', 'eval')
            decoded_js = decoded_js.replace(trash.group(), eval_trash)
        
        trash = re.search(r"if[(][(]function[(][)]{try(.*?)onreadystatechange(.*?)}", decoded_js)
        if trash:
            decoded_js = decoded_js.replace(trash.group(), '')

        trash = re.search(r"window[[](.*?)[]]", decoded_js)
        if trash:
            decoded_js = decoded_js.replace(trash.group(), "0")
        decoded_js = decoded_js.replace(r"window.headless", "0")

        # 添加上return cookie
        decoded_js = decoded_js[:-2] + ';return cookie;' + decoded_js[-2:]

        print(decoded_js)
        decoded_js = jsbeautifier.beautify(decoded_js)
        print("=========")
        # print(decoded_js)

        return decoded_js

    def generate_cookie(self):
        cookies = self.rc.get(YINBAOJIAN_COOKIES_KEY)
        if cookies:
            return json.loads(cookies)      
                                  
        decoded_js = self.js_decode_first()
        decoded_js = self.js_decode_second(decoded_js)
        fun_name = re.search(r"var(.*?)=", decoded_js).group(1)
        content = execjs.compile(decoded_js)
        __jls_clearance = content.call(fun_name)
        
        all_cookies = self.session.cookies.get_dict()
        all_cookies.update({'__jsl_clearance': __jls_clearance.replace('__jsl_clearance=', '')})
        
        self.rc.set(YINBAOJIAN_COOKIES_KEY, json.dumps(all_cookies))
        self.rc.expire(YINBAOJIAN_COOKIES_KEY, time=60*30)     
        return all_cookies


class YinbaijianSpider:
    def __init__(self, cookies):
        self.session = requests.session()
        self.cookies = cookies

    def paw(self, urls):
        for url in urls:

            try:
                resp = self.session.get(url, headers=HEADERS, cookies=self.cookies)
            except Exception as e:
                print('请求失败:', url)
            
            item_list = []
            html = resp.content.decode('utf-8')
            tree = etree.HTML(html)
            tags = tree.xpath('//td[@class="cc"]/img/ancestor::td/a')
            for tag in tags:
                item_list.append(
                    {
                        'mtime': int(time.time()),
                        'title': tag.xpath('.//text()')[0] if tag.xpath('.//text()') else '',
                        'url': urljoin(url, tag.xpath('./@href')[0] if tag.xpath('./@href') else ''),
                        'platform': 'web',
                        'source': '银保监',
                        'web_url': url,
                        'display': True
                    }
                )
            print(item_list, '\n')


if __name__ == '__main__':

    cookie_geter = YinbaojianCookieGeter()
    while(True):
        try:
            cookies = cookie_geter.generate_cookie()
            if cookies:
                break
        except Exception as e:
            print('获取cookies失败 重新获取')
            time.sleep(60*3)   

    print(cookies)
    spider = YinbaijianSpider(cookies)
    spider.paw(URLS)
    time.sleep(15)